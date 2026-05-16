## 2. Entorno y dependencias

Para garantizar un entorno de ejecución moderno, rápido y determinista, el cliente utiliza las siguientes herramientas y dependencias:

### Gestor de proyecto: uv

Se utiliza **uv** (un gestor de paquetes escrito en Rust) para la administración del proyecto. `uv` se encarga de:
*   Crear y gestionar el entorno virtual (venv).
*   Resolver y bloquear las versiones de las dependencias.
*   Ejecutar la aplicación de forma eficiente.

### Dependencias principales

*   **Python 3.13+:** Versión base del lenguaje.
*   **PySide6 (>=6.10.2):** Enlaces oficiales de Qt para la interfaz gráfica.
*   **SQLAlchemy (>=2.0.38):** ORM para la gestión de la base de datos local (SQLite).
*   **Requests (>=2.31.0):** Cliente HTTP para la comunicación con el servidor Java.
*   **python-dotenv (>=1.2.1):** Gestión de variables de entorno.
*   **Git:** Binario de sistema requerido para la lógica de versionado Bare.

### Requisitos del sistema

*   **Sistema Operativo:** Distribución Linux (Arch, Debian, Fedora, etc.).
*   **Binarios externos:** Git debe estar instalado y accesible en el PATH.


