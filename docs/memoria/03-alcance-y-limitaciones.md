## Alcance del proyecto

El proyecto **Dotfiles-Manager** se centra en la creación de una solución integral para la gestión de entornos de usuario en sistemas Linux. El alcance incluye:

*   **Auditoría del $HOME:** Identificación de archivos y directorios de configuración.
*   **Gestión de Versiones:** Implementación de flujos de trabajo con Git Bare para el seguimiento de cambios.
*   **Interfaz Dual:** Provisión de una interfaz gráfica (GUI) para usuarios finales y una interfaz de línea de comandos (CLI) para usuarios avanzados.
*   **Servicio de Clasificación:** Backend distribuido que utiliza IA para resolver dudas sobre archivos desconocidos.
*   **Persistencia:** Almacenamiento local (SQLite) y centralizado (servidor Java).

## Limitaciones

Para garantizar la viabilidad del proyecto como TFG, se han definido las siguientes limitaciones:

*   **Exclusividad de Sistema:** El proyecto está diseñado exclusivamente para sistemas operativos basados en el kernel **Linux**.
*   **Archivos de Usuario:** Solo se gestionan archivos dentro del directorio personal del usuario ($HOME). No se interviene en configuraciones de sistema a nivel de root (`/etc`).
*   **Dependencia de Red:** La clasificación mediante IA requiere conexión a internet, aunque el resto de funciones operan en modo local/offline.
*   **No es un Gestor de Paquetes:** La herramienta no instala software; solo gestiona los archivos de configuración de los programas ya instalados.



---