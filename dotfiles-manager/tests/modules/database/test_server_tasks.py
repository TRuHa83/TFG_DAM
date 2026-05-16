import pytest
from datetime import datetime, timedelta
from dotmng.modules.database.manager import DataBase
from dotmng.modules.database.models import ServerTasks

@pytest.fixture
def db(tmp_path):
    db_file = tmp_path / "test_dotfiles.sqlite"
    db = DataBase(db_file)
    yield db
    db.engine.dispose()

def test_get_server_task_none(db):
    """Si no hay tareas, debe devolver None."""
    assert db.get_server_task() is None

def test_set_and_get_server_task(db):
    """Debe insertar y recuperar una tarea como diccionario."""
    db.set_server_task("task-123", "QUEUE")
    task = db.get_server_task("task-123")
    
    assert task is not None
    assert isinstance(task, dict)
    assert task["task_id"] == "task-123"
    assert task["state"] == "QUEUE"

def test_get_server_task_filtering(db):
    """Debe filtrar solo tareas que no estén COMPLETE."""
    # Insertar una completada
    db.set_server_task("task-old", "COMPLETE")
    
    # Si no hay pendientes, debe devolver None (nuevo comportamiento)
    assert db.get_server_task() is None
    
    # Insertar una pendiente
    db.set_server_task("task-new", "PROCESSING")
    
    task = db.get_server_task()
    assert task is not None
    assert task["task_id"] == "task-new"
    assert task["state"] == "PROCESSING"

def test_get_server_task_by_id_even_if_complete(db):
    """Si se pide por ID, debe devolverla aunque esté COMPLETE."""
    db.set_server_task("task-1", "COMPLETE")
    task = db.get_server_task("task-1")
    assert task is not None
    assert task["task_id"] == "task-1"
    assert task["state"] == "COMPLETE"
