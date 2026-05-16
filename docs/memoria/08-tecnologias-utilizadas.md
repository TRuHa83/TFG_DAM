El proyecto se basa en un ecosistema políglota, seleccionando la herramienta más adecuada para cada dominio del problema.

## Tecnologías del Cliente (Frontend & Core)

* **Python 3.13:** Lenguaje principal debido a su versatilidad para el scripting de sistemas y su amplio ecosistema de librerías.
* **PySide6 (Qt for Python):** Framework para la creación de la interfaz gráfica de usuario profesional y multiplataforma.
* **SQLAlchemy 2.x:** ORM para la gestión de la base de datos local SQLite, facilitando el mapeo de objetos Python a tablas relacionales.
* **Git Bare:** Técnica nativa de Git utilizada para el control de versiones de archivos en el $HOME sin necesidad de moverlos de su ruta original.
* **Rich:** Librería para la creación de interfaces de línea de comandos (CLI) ricas en color y formato.

## Tecnologías del Servidor (Backend & IA)

* **Java 21 (LTS):** Lenguaje de tipado fuerte que proporciona estabilidad y alto rendimiento para la API central.
* **Spring Boot 3.5:** Framework líder para el desarrollo de microservicios y APIs RESTful.
* **Spring AI:** Módulo para la integración fluida con modelos de Inteligencia Artificial (Google Gemini).
* **Hibernate / Spring Data JPA:** Tecnologías para la persistencia de datos en el servidor, permitiendo una abstracción total del motor de base de datos.

## Infraestructura y Herramientas

* **SQLite:** Motor de base de datos relacional ligero utilizado tanto en cliente como en servidor para este proyecto.
* **Google Gemini API:** Modelo de lenguaje generativo utilizado para la clasificación heurística de archivos desconocidos.
* **JSON (JavaScript Object Notation):** Estándar de intercambio de datos entre el cliente Python y el servidor Java.



---