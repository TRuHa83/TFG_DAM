## 9. Gestión de errores y logging

El servidor implementa un sistema de control de errores centralizado para garantizar la disponibilidad del servicio y facilitar el diagnóstico de problemas en la red o en la IA.

### Control de Excepciones

El servidor responde con códigos HTTP apropiados según la validación en los controladores:

* **404 Not Found:** Cuando se consulta una tarea que no existe en la base de datos (gestionado en el `TasksController`).
* **500 Internal Server Error:** Cuando ocurre un fallo inesperado en el procesamiento de JSON o base de datos.
* **Respuestas en la carga útil:** Si una petición llega mal formada o sin payload, la tarea se crea pero se marca de forma interna con estado `ERROR`.

### Gestión de Fallos en la IA

Dada la dependencia de servicios externos (Google), el servidor gestiona específicamente los fallos del Batch API de Gemini:

* **Timeouts e Interrupciones:** Si ocurre un error de interrupción o fallo de red, la tarea se marca como `ERROR` en base de datos.
* **Reanudación Automática:** Si el servidor se apaga mientras una tarea estaba `PROCESSING`, al arrancar de nuevo recupera esas tareas y reanuda el sondeo (polling) del trabajo Batch asíncrono para asegurar que no se pierde el progreso.

### Logging del Sistema

Utiliza **SLF4J** con **Logback** para generar trazas en consola y archivos, registrando cada petición recibida y el estado detallado de los procesos de subida, creación de Batch Jobs y parsing de los resultados de Gemini.

*Ejemplo de flujo de logs durante una inferencia asíncrona exitosa:*

```text
2026-05-09 10:15:32 INFO  [TaskProcessorService] Tarea encontrada en cola: TASK-9A2X8L
2026-05-09 10:15:34 INFO  [TaskProcessorService] Archivo JSONL preparado en: /tmp/batch-TASK-9A2X8L.jsonl
2026-05-09 10:15:35 INFO  [TaskProcessorService] Batch Job creado: batch_job_XYZ123
2026-05-09 10:16:05 INFO  [TaskProcessorService] Estado del Job TASK-9A2X8L: JOB_STATE_RUNNING
2026-05-09 10:16:35 INFO  [TaskProcessorService] Estado del Job TASK-9A2X8L: JOB_STATE_SUCCEEDED
2026-05-09 10:16:36 INFO  [TaskProcessorService] Tarea completada con éxito: TASK-9A2X8L
```


