## 7. Comunicación con el servidor

El cliente se comunica con el servidor central a través de una API REST utilizando el protocolo HTTP y el intercambio de datos en formato **JSON**.

### Protocolo de Descubrimiento (Asíncrono)

Dada la naturaleza asíncrona del servidor, la comunicación no es bloqueante. Sigue este flujo:

1. **POST /discovery:** El cliente envía una lista de rutas y metadatos de archivos desconocidos.
2. **Response (Task ID):** El servidor responde inmediatamente con un identificador de tarea (`taskId`).
3. **Polling (GET /task/{id}):** El cliente consulta periódicamente el estado de la tarea hasta que el servidor marca el resultado como `COMPLETE`.

### Gestión de la Privacidad en el Payload

El payload enviado al servidor está estrictamente auditado para proteger la privacidad:

* **Rutas:** Se normalizan para eliminar nombres de usuario (ej: `/home/usuario/.bashrc` -> `$HOME/.bashrc`).
* **Contenido:** Nunca se envía el contenido de los archivos, solo nombres y extensiones.
* **Identificación:** Se utiliza un hash único por instalación para permitir que el servidor relacione tareas sin identificar al usuario real.


