## 4. Modelo de datos y persistencia

La persistencia del servidor Java se basa en una base de datos relacional (**SQLite** en esta fase) gestionada mediante **Spring Data JPA** e **Hibernate**. El modelo se centra en la gestión del ciclo de vida de las peticiones y el almacenamiento del conocimiento global.

### Modelo de datos

El diseño relacional global del servidor se organiza en dos bloques lógicos principales representados en el siguiente diagrama:

<br>
<div align="center">
  <img src="../assets/Diagrama%20ERD%20-%20Servidor.webp" width="80%" alt="Diagrama Entidad-Relación Servidor">
</div>
<br>

### Bloque de Procesamiento Asíncrono (Entidad Task)

Toda la lógica asíncrona gira en torno a la entidad **`Task`**, que representa una petición de clasificación de dotfiles enviada por el cliente:

* **`id` (String, PK):** Identificador único generado aleatoriamente (ej: `TASK-X9K2...`).
* **`status` (Enum `TaskStatus`):** Estado actual del ciclo de vida de la tarea:
  * `QUEUE`: Tarea recibida en la cola y en espera de procesamiento.
  * `PROCESSING`: El sistema está realizando la inferencia con la IA (Gemini Batch).
  * `COMPLETE`: Inferencia finalizada con éxito y resultado disponible.
  * `ERROR`: Fallo en la comunicación, validación o procesamiento.
* **`inputData` (@Lob String):** Payload JSON origen recibido del cliente con las firmas y rutas a clasificar.
* **`resultData` (@Lob String):** Payload JSON clasificado generado por la IA tras procesar la cola.
* **`batchId` (String):** Identificador que agrupa tareas que pertenecen a una misma solicitud o lote de ejecución.
* **`createdAt` (LocalDateTime):** Marca de tiempo asignada automáticamente (`@PrePersist`) para garantizar el orden de entrada en cola.

### Bloque de Conocimiento Global (Catálogo de Aplicaciones)

Este bloque almacena la base de datos de conocimiento acumulativo del servidor para la resolución inteligente de dotfiles:

* **`CategoryApp` (Categorías de Aplicaciones):** Define la taxonomía jerárquica de aplicaciones.
  * `id` (Integer, PK): Identificador autoincremental (`id_cat`).
  * `category` (String, UNIQUE, NOT NULL): Nombre legible de la categoría (ej. `Development`, `Shells`, `Browsers`).
  * `parent` (CategoryApp, FK): Relación recursiva ManyToOne que apunta a la categoría padre para admitir subcategorías.
* **`KnownAppReference` (Catálogo de Aplicaciones Conocidas):** Diccionario global de aplicaciones soportadas.
  * `appId` (String, PK): Clave única identificativa de la app (`app_id`).
  * `appName` (String, NOT NULL): Nombre legible y amigable de la aplicación.
  * `category` (CategoryApp, FK): Relación ManyToOne con la categoría lógica de la aplicación.
  * `filesInfoJson` (@Lob String): Estructura en JSON que detalla configuraciones típicas asociadas.
  * `packagesJson` (@Lob String): Listado en JSON de paquetes de instalación relacionados en Linux.
* **`AppFileReference` (Índice de Rutas Conocidas):** Tabla intermedia que mapea archivos individuales con aplicaciones.
  * `id` (Long, PK): Identificador único autoincremental.
  * `path` (String, NOT NULL): Ruta del archivo físico o carpeta conocida (`file_path`).
  * `type` (String, NOT NULL): Tipo de recurso (`file_type`: "file" o "folder").
  * app` (KnownAppReference, FK): Relación ManyToOne que conecta la ruta con su aplicación propietaria.

### Estrategia de Persistencia

* **ORM Hibernate:** Permite trabajar con objetos Java sin escribir SQL manualmente, facilitando la validación de tipos y la seguridad.
* **Mapeo de DTOs:** Los datos de la base de datos se transforman en DTOs antes de ser enviados al cliente para proteger la estructura interna del servidor.
* **Escalabilidad:** El uso de JPA asegura que el sistema pueda migrar a motores de base de datos más potentes (como PostgreSQL) sin cambios en el código fuente.


