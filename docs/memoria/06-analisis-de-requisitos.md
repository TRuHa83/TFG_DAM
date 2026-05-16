El análisis de requisitos define las capacidades que el sistema debe poseer para resolver el problema de la gestión de dotfiles de manera efectiva.

## Requisitos Funcionales (RF)

* **RF-1 (Auditoría):** El sistema debe ser capaz de identificar archivos de configuración en el directorio $HOME del usuario.
* **RF-2 (Clasificación):** El sistema debe categorizar los archivos encontrados (ej: Editores, Terminales, Navegadores).
* **RF-3 (Control de Versiones):** El sistema debe implementar un repositorio Git Bare para rastrear cambios en los archivos seleccionados.
* **RF-4 (Resolución Remota):** El sistema debe enviar metadatos de archivos desconocidos al servidor para su clasificación mediante IA.
* **RF-5 (Persistencia Local):** El sistema debe almacenar el inventario y el estado de los archivos en una base de datos SQLite local.
* **RF-6 (Interfaz Gráfica):** El usuario debe poder gestionar sus dotfiles a través de una ventana visual (GUI).
* **RF-7 (Interfaz de Comandos):** El sistema debe permitir la ejecución de todas sus funciones críticas vía terminal (CLI).

## Requisitos No Funcionales (RNF)

* **RNF-1 (Privacidad):** Los archivos físicos del usuario nunca deben abandonar la máquina local. Solo se transfieren metadatos (nombres, rutas, hashes).
* **RNF-2 (Rendimiento):** El escaneo del sistema de archivos debe ser eficiente y no bloquear la interfaz de usuario (uso de hilos asíncronos).
* **RNF-3 (Robustez):** El sistema debe gestionar errores de red y de permisos de archivos de forma elegante.
* **RNF-4 (Portabilidad):** La solución debe ser compatible con las principales distribuciones de Linux (Arch, Debian, Fedora).



---