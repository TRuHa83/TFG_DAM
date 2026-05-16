## 4. Base de datos local (SQLite)

El cliente Python implementa una base de datos relacional integrada (**SQLite**) gestionada a través del ORM **SQLAlchemy**. Su función principal es actuar como una caché persistente de alto rendimiento para el inventario local, evitando lecturas redundantes en disco y permitiendo el funcionamiento offline.

### Modelo de datos

El diseño relacional se organiza en varios bloques lógicos principales:

<div align="center">
  <img src="../assets/Diagrama%20ERD%20-%20Cliente.webp" width="80%" alt="Diagrama Entidad-Relación SQLite">
</div>

#### Bloque de Inventario y Auditoría

* **`local_inventory`:** Tabla central que vincula rutas físicas de archivos/carpetas conocidas en el `$HOME`.
* **`local_unknown`:** Tabla que registra rutas de archivos/carpetas encontradas pero no reconocidas.
* **`system_state_hashes`:** Almacena firmas (hashes) del estado de los directorios para detectar cambios rápidos.

#### Bloque de Aplicaciones y Categorías

* **`known_apps_reference`:** Catálogo de aplicaciones reconocidas proveniente del servidor.
* **`categories_apps`:** Taxonomía para organizar el software.
* **`os_distro_mapping`:** Identificador de la distribución base del sistema operativo.

#### Bloque de Reglas y Configuración

* **`global_ignore_rules`:** Patrones de exclusión (Regex/Exactos) para omitir archivos temporales.
* **`ui_preferences`** y **`server_config`:** Configuración de la interfaz y parámetros de conexión.

#### Bloque de Overrides (Preferencias del Usuario)

* **`user_inventory_overrides`**, **`user_unknown_overrides`**, **`user_ignore_overrides`**: Tablas que permiten al usuario habilitar o deshabilitar elementos específicos que el sistema ha detectado o ignorado por defecto.

#### Bloque de Tareas del Servidor

* **`server_tasks`:** Gestiona el estado de las peticiones asíncronas enviadas al backend (ej: `QUEUE`, `PROCESSING`, `COMPLETE`).

### Gestión de dotfiles conocidos y desconocidos

El sistema aplica una lógica diferencial para gestionar los archivos encontrados durante el escaneo:

* **Dotfiles Conocidos:** Aquellos cuya ruta o estructura coincide con la base de datos de referencia (`known_apps_reference`). Estos se vinculan automáticamente y quedan listos para ser versionados.
* **Dotfiles Desconocidos (Huérfanos):** Archivos que no coinciden con ninguna firma conocida.
  * En modo offline, se guardan en `local_unknown`.
  * En modo online, se dispara un proceso de auditoría que crea tareas en `server_tasks` enviando metadatos al servidor Java para que intente identificar la aplicación a la que pertenecen.
  * El usuario puede habilitarlos o ignorarlos modificando las preferencias en las tablas de overrides.


