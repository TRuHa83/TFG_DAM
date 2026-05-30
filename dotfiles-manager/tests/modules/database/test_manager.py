import time
import pytest
from datetime import datetime

from dotmng.modules.database.manager import DataBase
from dotmng.modules.database.models import SystemStateHashes


@pytest.fixture
def temp_db(tmp_path):
    """
    Fixture de pytest que inicializa la clase DataBase en un 
    directorio temporal para cada test. Se encarga de crear
    las tablas automáticamente por la lógica de tu __init__.
    """
    db_file = tmp_path / "test_dotfiles.sqlite"
    db = DataBase(db_file)
    yield db
    # Limpiamos las conexiones del engine tras cada test
    db.engine.dispose()


def test_set_system_state_hashes_insert(temp_db):
    """Prueba que se inserta un nuevo registro correctamente si no existe."""
    list_name = "ALL_DOTFILES"
    hashed = "abcdef123456"
    count = 10

    # Ejecutamos la función a testear
    temp_db.set_system_state_hashes(hashed, count, list_name)

    # Verificamos directamente en la base de datos
    session = temp_db.SessionLocal()
    record = session.query(SystemStateHashes).filter_by(list_name=list_name).first()
    session.close()

    assert record is not None
    assert record.list_name == list_name
    assert record.current_hash == hashed
    assert record.item_count == count
    assert isinstance(record.last_checked_at, datetime)


def test_set_system_state_hashes_update(temp_db):
    """Prueba que el upsert actualiza correctamente un registro existente."""
    list_name = "KNOWNS"
    
    # 1. Inserción inicial
    temp_db.set_system_state_hashes("hash_inicial", 5, list_name)
    
    # Pausa de una fracción de segundo para asegurar que datetime.now() da un tiempo mayor
    time.sleep(0.1) 

    # 2. Upsert (Actualización)
    temp_db.set_system_state_hashes("hash_nuevo", 15, list_name)

    # Verificamos que no hay registros duplicados y los datos son los nuevos
    session = temp_db.SessionLocal()
    records = session.query(SystemStateHashes).all()
    updated_record = session.query(SystemStateHashes).filter_by(list_name=list_name).first()
    session.close()

    assert len(records) == 1  # Confirma que On Conflict Update evitó duplicados
    assert updated_record.current_hash == "hash_nuevo"
    assert updated_record.item_count == 15


from unittest.mock import patch

def test_set_system_state_hashes_exception_handling(temp_db):
    """Prueba que se hace un rollback y se propaga la excepción en caso de error SQL."""
    # Hacemos un mock sobre el execute de la sesión para simular una caída de base de datos
    with patch('sqlalchemy.orm.Session.execute', side_effect=Exception("DB Error Simulado")):
        with patch.object(temp_db.log, 'error') as mock_log_error:
            with pytest.raises(Exception, match="DB Error Simulado"):
                temp_db.set_system_state_hashes("hash_fail", 0, "UNKNOWNS")

            # Asegura que el error ha quedado registrado en tus logs
            mock_log_error.assert_called_once()


def test_save_classified_data_empty_subcategory(temp_db):
    """Prueba que si la subcategoría está vacía se asocia con la categoría padre (Utilities en vez de None)."""
    from dotmng.modules.database.models import KnownAppsReference, CategoriesApps

    data = {
        "agents": {
            "category": "Utilities",
            "subcategory": "",
            "app_name": "AgentsApp",
            "files_info_json": [{"path": ".agents", "type": "folder"}],
            "packages_json": []
        }
    }

    # Guardar los datos clasificados con subcategoría vacía
    temp_db.save_classified_data(data)

    # Verificar que se insertó correctamente y la categoría asociada es la principal "Utilities"
    session = temp_db.SessionLocal()
    app_ref = session.query(KnownAppsReference).filter_by(app_id="agents").first()
    
    assert app_ref is not None
    assert app_ref.app_name == "AgentsApp"
    
    # Obtener la categoría del registro
    category_obj = session.query(CategoriesApps).filter_by(id_cat=app_ref.category_id).first()
    assert category_obj is not None
    assert category_obj.category == "Utilities"
    assert category_obj.parent_id is None  # Es una categoría raíz
    session.close()


def test_save_classified_data_ignored_or_unknown(temp_db):
    """Prueba que las aplicaciones marcadas como 'Unknown' o 'ignored': true se omiten y no se persisten en la base de datos."""
    from dotmng.modules.database.models import KnownAppsReference

    data = {
        "unknown_app": {
            "category": "System",
            "subcategory": "Utilities",
            "app_name": "Unknown",
            "files_info_json": [{"path": ".unknown", "type": "folder"}],
            "packages_json": []
        },
        "ignored_app": {
            "category": "Development",
            "subcategory": "IDE",
            "app_name": "MyIDE",
            "ignored": True,
            "files_info_json": [{"path": ".myide", "type": "folder"}],
            "packages_json": []
        },
        "valid_app": {
            "category": "Development",
            "subcategory": "Compiler",
            "app_name": "GCC",
            "files_info_json": [{"path": ".gcc", "type": "folder"}],
            "packages_json": []
        }
    }

    # Guardar los datos clasificados
    temp_db.save_classified_data(data)

    # Verificar en la base de datos qué se guardó
    session = temp_db.SessionLocal()
    
    # GCC (válido) debe estar guardado
    valid_ref = session.query(KnownAppsReference).filter_by(app_id="valid_app").first()
    assert valid_ref is not None
    assert valid_ref.app_name == "GCC"

    # unknown_app e ignored_app NO deben existir en la base de datos
    unknown_ref = session.query(KnownAppsReference).filter_by(app_id="unknown_app").first()
    assert unknown_ref is None

    ignored_ref = session.query(KnownAppsReference).filter_by(app_id="ignored_app").first()
    assert ignored_ref is None

    session.close()