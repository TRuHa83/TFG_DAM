# dotfile-server

> **Componente servidor** del sistema distribuido de gestión y clasificación de dotfiles.
> API REST construida con Spring Boot 3 + integración Google Gemini AI.

[![Java](https://img.shields.io/badge/Java-21_LTS-ED8B00?logo=openjdk&logoColor=white)](https://openjdk.org/projects/jdk/21/)
[![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.5-6DB33F?logo=spring&logoColor=white)](https://spring.io/projects/spring-boot)
[![Spring AI](https://img.shields.io/badge/Spring_AI-1.1.4-6DB33F?logo=spring)](https://spring.io/projects/spring-ai)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite)](https://www.sqlite.org/)

---

## ¿Qué hace?

`dotfile-server` es el backend cloud del sistema **Dotfiles-Manager**. Recibe peticiones
del cliente Python, encola tareas de clasificación IA y devuelve resultados de forma asíncrona.

El cliente ([dotfiles-manager](../dotfiles-manager/README.md)) envía datos de rutas de
dotfiles desconocidos. El servidor los procesa con **Google Gemini** y responde con
clasificaciones que el cliente persiste en su base de datos local.

→ Documentación técnica completa: [Wiki Servidor](https://truha83.github.io/TFG_DAM/servidor/01-introduccion/)
→ Memoria del TFG: [Wiki Principal](https://truha83.github.io/TFG_DAM/)

---

## Requisitos previos

| Herramienta | Versión mínima | Notas |
|---|---|---|
| Java JDK | 21 (LTS) | Recomendado: Temurin/OpenJDK |
| Maven | 3.9+ | O usar el wrapper incluido `./mvnw` |
| `GEMINI_API_KEY` | — | Variable de entorno requerida |

---

## Configuración

Copia el fichero de plantilla y añade tu API key:

```bash
cp .env.example .env
```

Edita `.env`:

```env
GEMINI_API_KEY=tu_clave_de_google_ai_aqui
```

Obtén tu API key gratuita en: [Google AI Studio](https://aistudio.google.com/apikey)

---

## Arranque en desarrollo

```bash
# Con el wrapper Maven incluido (sin instalar Maven):
GEMINI_API_KEY=tu_clave ./mvnw spring-boot:run

# O si tienes Maven instalado:
GEMINI_API_KEY=tu_clave mvn spring-boot:run
```

El servidor arranca en `http://localhost:8080` por defecto.

---

## Build y ejecución del JAR

```bash
# Compilar y empaquetar
./mvnw clean package -DskipTests

# Ejecutar el JAR generado
GEMINI_API_KEY=tu_clave java -jar target/dotfile_server-*.jar
```

---

## 🐳 Despliegue con Docker (En Desarrollo)

El objetivo principal para el entorno de producción es abstraer la aplicación mediante Docker Compose, permitiendo un despliegue con un único comando:

```bash
# Futuro comando de despliegue planificado
docker-compose up -d
```

La orquestación se encargará automáticamente de inyectar las variables de entorno (como `GEMINI_API_KEY`) y mapear el volumen local necesario para la persistencia de la base de datos SQLite.

---

## API REST — Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Comprobación de disponibilidad → `ok` |
| `POST` | `/discovery` | Enviar datos para clasificación → `{ "taskId": "TASK-..." }` |
| `GET` | `/task/{taskId}` | Consultar estado de tarea → `{ status, result }` |

### Ciclo de vida de una tarea

```
POST /discovery  →  taskId
                        ↓
                   [QUEUE]  →  [PROCESSING]  →  [COMPLETE]
                                                [ERROR]
GET /task/{id}   ←  polling cada 2s
```

### Ejemplo de uso

```bash
# 1. Verificar disponibilidad
curl http://localhost:8080/health

# 2. Enviar datos
curl -X POST http://localhost:8080/discovery \
     -H "Content-Type: application/json" \
     -d '{"data": "/home/user/.bashrc:md5hash"}'

# 3. Consultar estado
curl http://localhost:8080/task/TASK-AB3CDE7F89XY
```

---

## Estructura del proyecto

```
dotfiles_server/
├── src/
│   ├── main/
│   │   ├── java/dev/techcrafted/dotfile_server/
│   │   │   ├── config/       # WebConfig (CORS)
│   │   │   ├── controller/   # HealthController, DiscoveryController, TasksController
│   │   │   ├── dto/          # DiscoveryRequest, DiscoveryResponse, TaskStatusResponse
│   │   │   ├── model/        # Task (JPA Entity), TaskStatus (Enum)
│   │   │   ├── repository/   # TaskRepository (Spring Data JPA)
│   │   │   ├── service/      # TaskProcessorService (scheduler @2s)
│   │   │   └── DotfileServerApplication.java
│   │   └── resources/
│   │       └── application.yaml   # Config Spring: SQLite, JPA, AI key
│   └── test/
│       └── java/                  # Tests JUnit
├── .env.example                   # Plantilla de variables de entorno
├── mvnw / mvnw.cmd                # Maven wrapper
└── pom.xml                        # Dependencias del proyecto
```

---

## Dependencias principales

| Dependencia | Uso |
|---|---|
| `spring-boot-starter-web` | API REST con Spring MVC |
| `spring-boot-starter-data-jpa` | Persistencia con Hibernate ORM |
| `spring-ai-starter-model-google-genai` | Integración Google Gemini AI |
| `sqlite-jdbc` | Driver JDBC para SQLite |
| `hibernate-community-dialects` | Dialecto Hibernate para SQLite |
| `lombok` | Reducción de boilerplate (`@Data`, `@Slf4j`) |

---

## Ejecutar pruebas

```bash
./mvnw test
```

---

## Documentación técnica

- [Stack tecnológico del servidor](https://truha83.github.io/TFG_DAM/servidor/02-entorno-y-dependencias/)
- [Base de datos JPA (Task model)](https://truha83.github.io/TFG_DAM/servidor/04-modelo-de-datos-y-persistencia/)
- [API REST: endpoints y DTOs](https://truha83.github.io/TFG_DAM/servidor/05-api-rest/)
- [Implementación y estructura](https://truha83.github.io/TFG_DAM/servidor/03-arquitectura-interna/)
- [Arquitectura del sistema completo](https://truha83.github.io/TFG_DAM/memoria/07-arquitectura-del-sistema/)
