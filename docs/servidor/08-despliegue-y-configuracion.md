El servidor ha sido diseñado para ser fácilmente desplegable en cualquier entorno que soporte la Máquina Virtual de Java (JVM).

### Despliegue Contenerizado (Docker)

La idea principal para facilitar el despliegue del servidor y asegurar su portabilidad es distribuirlo mediante contenedores Docker. Esto permitirá abstraer las dependencias del sistema operativo y levantar el servicio con un único comando.

* **Dockerfile:** Empaquetará la aplicación Spring Boot utilizando una imagen base ligera de Java 21 (ej. `eclipse-temurin:21-jre-alpine`).
* **Docker Compose:** Se utilizará un archivo `docker-compose.yml` para orquestar el servidor, facilitando la inyección de variables de entorno y el mapeo de volúmenes para hacer persistente la base de datos SQLite.

### Empaquetado y Ejecución Tradicional (JAR)

El proyecto se compila mediante Maven generando un archivo **FAT JAR** que incluye todas las dependencias y el servidor embebido (Tomcat).

* **Comando de compilación:** `mvn clean package`
* **Comando de ejecución:** `java -jar dotfile-server.jar`

### Parámetros de Configuración

La configuración se externaliza a través de `application.yaml` o variables de entorno (que en el futuro se inyectarán vía Docker):

* **`GEMINI_API_KEY`:** Clave necesaria para habilitar la lógica de resolución por IA.
* **`SERVER_PORT`:** Puerto donde el servidor escuchará peticiones.
* **`SPRING_DATASOURCE_URL`:** Ubicación del archivo de base de datos SQLite.


---