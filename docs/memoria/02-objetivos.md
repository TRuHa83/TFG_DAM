## Generales

Desarrollar un ecosistema de software distribuido (arquitectura Cliente/Servidor) orientado a la auditoría, clasificación inteligente y control de versiones local de archivos de configuración (*dotfiles*) en entornos UNIX/Linux. El sistema debe eliminar la fricción de los métodos manuales, prescindir de enlaces simbólicos y apoyarse en bases de datos comunitarias e Inteligencia Artificial para resolver configuraciones huérfanas, garantizando siempre la privacidad del usuario.

## Específicos

* **Motor de Auditoría Local (Python):** Implementar un escáner nativo que utilice el patrón *Pipeline* para filtrar y clasificar archivos en `$HOME` basándose en heurística y el estándar *xdg-ninja*.
* **Persistencia y GUI (PySide6):** Integrar **SQLite** en el cliente para caché y preferencias. Desarrollar una interfaz gráfica moderna con **PySide6** siguiendo el patrón MVC.
* **API RESTful (Java Backend):** Diseñar un servidor en **Java** (Spring Boot) que actúe como cerebro central, gestionando metadatos en formato JSON y almacenando el conocimiento colectivo.
* **Integración de IA (Gemini):** Conectar el backend con modelos de lenguaje para clasificar dinámicamente estructuras de archivos no registradas previamente.
* **Control de Versiones (Git Bare):** Implementar la técnica **Git Bare Repository** para automatizar el control de versiones *in situ*, facilitando el respaldo sin alterar la ubicación física de los archivos.

## Opcionales (Extras)

* **Backups Unificados:** Módulo para comprimir configuraciones en formato `tar.gz`, facilitando migraciones rápidas entre distribuciones.
* **Modo Headless y Automatización:** Soporte para ejecución vía CLI y modo demonio, permitiendo la integración con tareas programadas (`cron` o `systemd timers`).



---