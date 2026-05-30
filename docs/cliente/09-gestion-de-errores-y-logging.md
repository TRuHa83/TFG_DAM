Para asegurar la robustez en un entorno tan crítico como el directorio $HOME, el cliente implementa una gestión de errores exhaustiva y un sistema de trazas detallado.

### Niveles de Trazas (Logging)

El sistema genera logs en diferentes niveles:
*   **DEBUG:** Información detallada de rutinas, consultas a base de datos y cambios de estado interno, utilizada para depuración sin sobrecargar el registro principal.
*   **INFO:** Registro de operaciones exitosas (ej: "Escaneo finalizado en 1.2s").
*   **WARNING:** Alertas de estado o de conexión (ej: "Archivo omitido por falta de permisos").
*   **ERROR:** Fallos críticos (ej: "Conexión perdida con el servidor", "Error al escribir en SQLite").

### Gestión de Excepciones Comunes

*   **Errores de Disco:** El sistema captura excepciones de entrada/salida (I/O) y notifica al usuario si un archivo está bloqueado o el disco está lleno.
*   **Errores de Red:** Si el servidor Java no responde, el cliente activa automáticamente el **Modo Offline**, encolando las peticiones de clasificación para más tarde.
*   **Conflictos de Git:** Si se detecta un conflicto en el repositorio Bare, el sistema detiene la operación y solicita la intervención del usuario para evitar la pérdida de datos.


---