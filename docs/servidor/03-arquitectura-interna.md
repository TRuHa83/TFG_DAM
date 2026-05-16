El servidor sigue una arquitectura en capas tradicional, facilitando el mantenimiento y la escalabilidad de cada componente.

A continuación se presenta un resumen de la estructura de paquetes Java (`src/main/java/dev/techcrafted/dotfile_server/`), reflejando la separación por responsabilidades:

```text
dotfiles_server/ (Servidor Java)
├── src/main/
│   ├── java/dev/techcrafted/dotfile_server/
│   │   ├── config/
│   │   │   └── WebConfig.java                   # Configuración de CORS y rutas MVC
│   │   │
│   │   ├── controller/
│   │   │   ├── DiscoveryController.java         # Controlador del endpoint asíncrono /discovery
│   │   │   ├── HealthController.java            # Endpoint para monitorización de estado
│   │   │   └── TasksController.java             # Consulta de estados de tareas de IA
│   │   │
│   │   ├── dto/
│   │   │   ├── AppDetailDTO.java                # DTO estructurado de metadatos de apps
│   │   │   ├── DiscoveryRequest.java            # Payloads recibidos del cliente
│   │   │   ├── DiscoveryResponse.java           # Respuesta inmediata con identificadores
│   │   │   └── TaskStatusResponse.java          # Payload de respuesta del poller asíncrono
│   │   │
│   │   ├── model/
│   │   │   ├── AppFileReference.java            # Entidad de mapeo para rutas indexadas
│   │   │   ├── CategoryApp.java                 # Estructura de árbol de categorías de apps
│   │   │   ├── KnownAppReference.java           # Diccionario de metadatos globales
│   │   │   ├── Task.java                        # Tarea de clasificación asíncrona
│   │   │   └── TaskStatus.java                  # Enum (QUEUE, PROCESSING, COMPLETE, ERROR)
│   │   │
│   │   ├── repository/
│   │   │   ├── AppFileReferenceRepository.java  # Acceso a datos para rutas indexadas
│   │   │   ├── CategoryAppRepository.java       # Acceso a taxonomías de categorías
│   │   │   ├── KnownAppReferenceRepository.java # Consultas de catálogo global
│   │   │   └── TaskRepository.java              # Control de transacciones de tareas asíncronas
│   │   │
│   │   ├── service/
│   │   │   └── TaskProcessorService.java        # Procesador de colas e integración con Gemini Batch
│   │   │
│   │   └── DotfileServerApplication.java        # Clase principal y configurador Spring Boot
│   │
│   └── resources/
│       ├── application.properties               # Configuración del puerto de red (server.port=8080)
│       └── application.yaml                     # Configuración del datasource SQLite e Hibernate
│
├── src/test/                                    # Clases de test unitario y JUnit
│
├── mvnw                                         # Maven Wrapper para sistemas Unix
├── mvnw.cmd                                     # Maven Wrapper para sistemas Windows
└── pom.xml                                      # Archivo POM de dependencias de Maven
```

### Capas del Sistema

* **Capa de Controladores (`controller`):** Define los puntos de entrada (Endpoints) de la API REST. Valida las peticiones entrantes y las delega a los servicios correspondientes.
* **Capa de Servicios (`service`):** Contiene la lógica de negocio. Destaca el `TaskProcessorService`, que gestiona la cola de tareas asíncronas y la integración con la IA.
* **Capa de Persistencia (`repository`):** Interfaces de Spring Data JPA que abstraen las operaciones de lectura y escritura en la base de datos.
* **Capa de Modelos (`model`):** Entidades JPA que representan las tablas de la base de datos (Tasks, Apps, etc.).
* **Capa de DTOs (`dto`):** Objetos de Transferencia de Datos utilizados para desacoplar el modelo interno de la base de datos de las respuestas enviadas al cliente.
* **Capa de Configuración (`config`):** Contiene la configuración de seguridad, CORS y beans necesarios para la aplicación.

### El Modelo de Tareas Asíncronas

Dada la latencia de las respuestas de IA, el servidor implementa un modelo asíncrono:

1. El controlador recibe una petición y crea una `Task` en estado `QUEUE`.
2. Un proceso programado (`@Scheduled`) escanea la base de datos buscando tareas pendientes.
3. El servicio de IA procesa la tarea y actualiza el estado a `COMPLETE` o `ERROR`.


---