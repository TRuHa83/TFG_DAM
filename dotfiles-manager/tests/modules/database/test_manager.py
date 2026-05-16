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