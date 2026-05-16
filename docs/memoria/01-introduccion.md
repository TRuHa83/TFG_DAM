## Contexto y el problema del directorio `$HOME`

En el ecosistema Linux, la inmensa mayoría de las aplicaciones (desde editores de texto y terminales, hasta entornos de escritorio completos) almacenan sus preferencias en archivos y directorios ocultos, comúnmente conocidos como **dotfiles** (debido a que su nomenclatura comienza con un punto, ej. `.bashrc`, `.vimrc`, `.config/`).

Históricamente, estos archivos se han depositado directamente en la raíz del directorio personal del usuario (`$HOME` o `~/`). A medida que se instalan más herramientas, el directorio se satura, generando un nivel de "entropía" que dificulta enormemente la auditoría de qué archivo pertenece a qué aplicación.

Aunque existe la especificación **XDG Base Directory** —un estándar diseñado para unificar y categorizar estas rutas en directorios limpios como `~/.config` o `~/.local/share`—, una gran cantidad de software *legacy* y aplicaciones modernas continúan ignorando el estándar, perpetuando el caos organizativo.

## Soluciones actuales y sus limitaciones

La necesidad de migrar estas configuraciones entre diferentes equipos o distribuciones ha impulsado la creación de múltiples herramientas de gestión. No obstante, las aproximaciones tradicionales presentan fallas arquitectónicas:

* **Scripts personalizados (Bash/Python):** Requieren un mantenimiento manual exhaustivo. El usuario debe conocer de antemano la ubicación exacta de cada archivo para programar su copia. No hay inteligencia ni descubrimiento automático.
* **Gestores basados en Symlinks (ej. GNU Stow):** Son el estándar de facto actual. Su funcionamiento consiste en mover físicamente el archivo original a una carpeta centralizada y dejar un enlace simbólico (*symlink*) en su lugar original. Esto genera un alto riesgo de enlaces rotos, duplicidad de datos y problemas de permisos si el enlace se corrompe.

## Motivación del proyecto

La motivación principal de **Dotfiles-Manager** nace de la necesidad personal y profesional de contar con una herramienta automatizada, transparente y sin fricciones para la gestión de entornos de trabajo en Linux.

El proyecto busca abandonar el enfoque de "copia manual" para implementar una **arquitectura de software avanzada** que aporta las siguientes innovaciones:

* **Descubrimiento Inteligente:** Auditar el sistema basándose en heurística y el estándar XDG para separar la configuración útil de la "basura" o caché.
* **Control de Versiones Transparente (Técnica Git Bare):** Erradicar el frágil enfoque de los enlaces simbólicos adoptando la estrategia **Git Bare Repository**. Al desacoplar el directorio de control de Git (`--git-dir`) del árbol de trabajo (asignado a la raíz del `$HOME`), se logra rastrear los archivos *in situ* sin moverlos de su ruta original.
* **Resolución Asistida (IA):** Implementar una arquitectura distribuida (Cliente/Servidor) integrando un servicio backend que, mediante Modelos de Lenguaje (LLMs), clasifica archivos de configuración desconocidos.

En conclusión, este proyecto resuelve un problema operativo real y sirve como vehículo para aplicar competencias avanzadas en POO, bases de datos relacionales, interfaces gráficas (PySide6) y desarrollo de APIs REST (Spring Boot).


---