import pytest
import requests
from unittest.mock import MagicMock, patch
from dotmng.modules.api.client import AppClient
from dotmng.modules.api.poller import ServerPoller, TaskPoller

# --- Tests for AppClient ---

def test_app_client_discovery_success():
    """Prueba el éxito de discovery_apps."""
    client = AppClient("http://localhost:8000")
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"taskID": "task-123"}
        mock_post.return_value = mock_response

        task_id = client.discovery_apps({"some": "data"})
        assert task_id == "task-123"

def test_app_client_discovery_error_404():
    """Prueba el manejo de un error 404 en discovery_apps."""
    client = AppClient("http://localhost:8000")
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        task_id = client.discovery_apps({"some": "data"})
        assert task_id is None

def test_app_client_discovery_timeout():
    """Prueba el manejo de un timeout en discovery_apps."""
    client = AppClient("http://localhost:8000")
    with patch("requests.post", side_effect=requests.exceptions.Timeout):
        task_id = client.discovery_apps({"some": "data"})
        assert task_id is None

def test_app_client_discovery_malformed_json():
    """Prueba el manejo de un JSON malformado en discovery_apps."""
    client = AppClient("http://localhost:8000")
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        task_id = client.discovery_apps({"some": "data"})
        assert task_id is None

# --- Tests for ServerPoller ---

@patch("requests.get")
@patch("time.sleep", return_value=None)  # Evitar esperas reales
def test_server_poller_success(mock_sleep, mock_get):
    """Prueba el éxito de ServerPoller."""
    poller = ServerPoller("http://localhost:8000")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "ok"
    mock_get.return_value = mock_response

    # Capturar señales
    results = []
    poller.finished_ok.connect(lambda msg: results.append(msg))

    # Ejecutar run() una vez (modificamos _is_running manualmente para detenerlo)
    def stop_poller(*args, **kwargs):
        poller.stop()

    poller.finished_ok.connect(stop_poller)
    poller.run()

    assert "ok" in results
    assert poller.last_response_ok is True

@patch("requests.get")
@patch("time.sleep", return_value=None)
def test_server_poller_error_status(mock_sleep, mock_get):
    """Prueba el error por código HTTP no esperado en ServerPoller."""
    poller = ServerPoller("http://localhost:8000")
    
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    results = []
    poller.finished_error.connect(lambda msg: results.append(msg))
    
    poller.run()

    assert any("500" in msg for msg in results)
    assert poller.last_response_ok is False
    assert poller._is_running is False

@patch("requests.get")
@patch("time.sleep", return_value=None)
def test_server_poller_connection_failure(mock_sleep, mock_get):
    """Prueba el fallo de conexión en ServerPoller."""
    poller = ServerPoller("http://localhost:8000")
    mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

    results = []
    poller.finished_error.connect(lambda msg: results.append(msg))
    
    poller.run()

    assert any("fallo de conexión" in msg for msg in results)
    assert poller.last_response_ok is False
    assert poller._is_running is False

@patch("requests.get")
@patch("time.sleep", return_value=None)
def test_server_poller_200_but_not_ok(mock_sleep, mock_get):
    """Prueba que ServerPoller falla si recibe 200 pero el cuerpo no es 'ok'."""
    poller = ServerPoller("http://localhost:8000")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "error" # No es "ok"
    mock_get.return_value = mock_response

    results = []
    poller.finished_error.connect(lambda msg: results.append(msg))
    
    poller.run()

    assert any("200" in msg for msg in results)
    assert poller.last_response_ok is False
    assert poller._is_running is False

# --- Tests for TaskPoller ---

@patch("requests.get")
@patch("time.sleep", return_value=None)
def test_task_poller_success_complete(mock_sleep, mock_get):
    """Prueba el éxito de TaskPoller cuando la tarea se completa."""
    poller = TaskPoller("http://localhost:8000", "task-123")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "COMPLETE", "data": "finished"}
    mock_get.return_value = mock_response

    results = []
    poller.finished.connect(lambda success, data: results.append((success, data)))

    poller.run()

    assert len(results) == 1
    assert results[0][0] is True
    assert results[0][1]["status"] == "COMPLETE"
    assert poller._is_running is False

@patch("requests.get")
@patch("time.sleep", return_value=None)
def test_task_poller_error_status_in_json(mock_sleep, mock_get):
    """Prueba cuando el servidor devuelve un estado 'ERROR' en el JSON."""
    poller = TaskPoller("http://localhost:8000", "task-123")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ERROR", "reason": "something went wrong"}
    mock_get.return_value = mock_response

    results = []
    poller.finished.connect(lambda success, data: results.append((success, data)))

    poller.run()

    assert len(results) == 1
    assert results[0][0] is False
    assert results[0][1]["status"] == "ERROR"
    assert poller._is_running is False

@patch("requests.get")
@patch("time.sleep", return_value=None)
def test_task_poller_http_error(mock_sleep, mock_get):
    """Prueba error HTTP en TaskPoller."""
    poller = TaskPoller("http://localhost:8000", "task-123")
    
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    results = []
    poller.finished.connect(lambda success, data: results.append((success, data)))

    poller.run()

    assert len(results) == 1
    assert results[0][0] is False
    assert "HTTP 404" in results[0][1]["error"]
    assert poller._is_running is False

@patch("requests.get")
@patch("time.sleep", return_value=None)
def test_task_poller_missing_status(mock_sleep, mock_get):
    """Prueba cuando el JSON no tiene el campo 'status'."""
    poller = TaskPoller("http://localhost:8000", "task-123")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"something": "else"}
    mock_get.return_value = mock_response

    results = []
    poller.status_changed.connect(lambda status, data: results.append((status, data)))

    # Necesitamos detenerlo manualmente ya que QUEUE es el default y no detiene el bucle
    def stop_it(status, data):
        if status == "QUEUE":
            poller.stop()

    poller.status_changed.connect(stop_it)
    poller.run()

    # Debería haber emitido QUEUE por defecto
    assert results[0][0] == "QUEUE"
