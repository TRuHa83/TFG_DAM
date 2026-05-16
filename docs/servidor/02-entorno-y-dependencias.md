## 2. Entorno y dependencias

El backend ha sido construido utilizando el stack tecnológico estándar de la industria para aplicaciones empresariales robustas y escalables.

### Tecnologías Base

* **Java 21 (LTS):** Versión de soporte extendido que permite el uso de características modernas como registros (Records) y hilos virtuales.
* **Spring Boot 3.5:** Framework principal para la orquestación de la aplicación, inyección de dependencias y gestión del ciclo de vida.
* **Maven:** Gestor de proyectos y dependencias.

### Dependencias Críticas

* **Spring Web:** Para la creación de los controladores REST y la gestión de peticiones HTTP.
* **Spring Data JPA:** Para la abstracción de la capa de persistencia mediante Hibernate.
* **Google GenAI Java SDK (`com.google.genai`):** SDK oficial de Google utilizado directamente en el `TaskProcessorService` para la gestión de Batch Jobs de Gemini (subida de archivos JSONL, creación y sondeo de trabajos asíncronos).
* **Spring AI (`spring-ai-starter-model-google-genai`):** Declarado como dependencia para posibles integraciones futuras con el ecosistema Spring; en la versión actual, la lógica de Batch utiliza el SDK directo de Google.
* **SQLite JDBC:** Driver para la conexión con el motor de base de datos ligero.
* **Hibernate Community Dialects:** Dialecto Hibernate necesario para el soporte de SQLite.
* **Lombok:** Librería para reducir el código repetitivo (Boilerplate) en las entidades y DTOs.

### Configuración del Entorno

El servidor se configura a través del archivo `application.yaml`, donde se definen:

* Puerto de escucha (por defecto 8080).
* Ruta de la base de datos SQLite.
* API Key de Google Gemini (inyectada de forma segura mediante variables de entorno).


