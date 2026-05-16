El servidor expone una interfaz de programación de aplicaciones (API) basada en los principios de REST, utilizando JSON como formato de intercambio y códigos de estado HTTP estándar para la gestión de errores.

### Endpoints expuestos

##### POST /discovery

Recibe los metadatos de los dotfiles desconocidos y crea una tarea de clasificación. También identifica y devuelve instantáneamente aplicaciones conocidas si ya se encuentran en la BD.

* **Response:** 200 OK.
* **Payload:** Objeto JSON con el `taskID`, el `status` de la tarea, y opcionalmente un mapa `data` con las aplicaciones ya reconocidas.

##### GET /task/ {taskId}

Consulta el estado de una tarea previamente encolada.

* **Response:** 200 OK.
* **Payload:** Objeto JSON con el `taskId`, el `status`, el `batchId` y la clave `data` con el JSON resultante (si ha finalizado).

##### GET /health

Endpoint de comprobación de salud del sistema.

* **Response:** 200 OK.
* **Payload:** Texto plano "ok".

### Formato de peticiones y respuestas

#### Ejemplo de Petición (Discovery)

```json
{
  "data": {
    "unknown_id_1": { "path": ".config/custom_app", "type": "folder" }
  }
}
```

#### Ejemplo de Respuesta POST /discovery (con app ya conocida)

```json
{
  "taskID": "TASK-AB3CDE7F89XY",
  "status": "COMPLETE",
  "data": {
    "1password_cli": {
      "app_name": "1Password CLI",
      "category": "Security",
      "subcategory": "Password Manager",
      "files_info_json": [{ "path": ".op", "type": "folder" }],
      "packages_json": ["1password-cli"]
    }
  }
}
```

> **Nota:** Si hay entradas desconocidas, `status` será `QUEUE` y `data` estará vacío. El cliente debe entonces sondear `GET /task/{taskID}` hasta obtener `COMPLETE`.

#### Ejemplo de Respuesta GET /task/ {id} (tarea completada)

```json
{
  "id": "TASK-AB3CDE7F89XY",
  "status": "COMPLETE",
  "batchId": "batches/batch_job_XYZ123",
  "data": {
    "custom_app": {
      "app_name": "Mi Aplicación",
      "category": "Development",
      "subcategory": "Editor",
      "files_info_json": [{ "path": ".customrc", "type": "file" }],
      "packages_json": []
    }
  }
}
```


---