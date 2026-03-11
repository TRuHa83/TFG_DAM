# 🗂️ Dotfiles-Manager

> **Sistema Distribuido de Gestión y Clasificación de Entornos Linux**

**Trabajo de Fin de Grado (DAM)** — Autor: *Sergio Trujillo de la Nuez*

<div align="center">

### 📖 [Consulta la Documentación Técnica Completa](https://truha83.github.io/TFG_DAM/)

</div>

---

## 📋 Descripción

**Dotfiles-Manager** es un ecosistema de software distribuido (Cliente/Servidor) para la **auditoría, clasificación inteligente y control de versiones** de archivos de configuración (*dotfiles*) en entornos UNIX/Linux.

A diferencia de los gestores tradicionales basados en *symlinks* (GNU Stow) o scripts manuales, esta herramienta:

- **Descubre automáticamente** los dotfiles del `$HOME` mediante heurística y el estándar XDG.
- **Versiona in situ** utilizando la técnica **Git Bare Repository** (*Zero-Friction*): los archivos nunca abandonan su ruta original.
- **Clasifica archivos desconocidos** conectándose a un servidor que integra **Modelos de Lenguaje (LLMs)** como Google Gemini.
- **Garantiza la privacidad**: solo se envían metadatos (hashes y firmas estructurales), nunca los archivos físicos del usuario.

---

## 🏗️ Arquitectura

Arquitectura **Cliente/Servidor** comunicada exclusivamente vía **API REST** (HTTP + JSON):

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| **Cliente Local** | Python 3.x | Auditoría del sistema de archivos, persistencia local (SQLite), GUI, ejecución de Git Bare |
| **Servidor Central** | Java 21 (LTS) | API REST *stateless*, base de conocimiento global, intermediario seguro con LLMs |

### Flujo de datos y privacidad

1. El cliente detecta un archivo desconocido y genera un **Payload JSON** con metadatos despersonalizados (hash SHA-256 de la ruta + firma estructural).
2. El servidor busca el hash en su base de datos. Si no existe, consulta al LLM.
3. La clasificación resultante se almacena en el servidor para futuras consultas comunitarias.
4. **El archivo físico nunca abandona la máquina local.**

### Patrones de diseño

- **MVC** (Modelo-Vista-Controlador) — GUI con PySide6
- **Pipeline** — Motor de escaneo: `Descubrimiento → Heurística XDG → Filtrado → Petición API → Persistencia`
- **REST** — Comunicación entre Python y Java

---

## ⚙️ Stack Tecnológico

### Cliente (Local)

| Tecnología | Uso |
|---|---|
| **Python 3.x** | Lenguaje principal del cliente |
| **PySide6 (Qt)** | Interfaz gráfica moderna (GUI) |
| **SQLite + SQLAlchemy** | Base de datos local embebida (ORM) |
| **Git (Bare Repository)** | Control de versiones transparente sin `.git` en `$HOME` |

### Servidor (Backend)

| Tecnología | Uso |
|---|---|
| **Java 21 (LTS)** | API REST central (Virtual Threads) |
| **SQLite + Hibernate (JPA)** | Persistencia del conocimiento global (preparado para migrar a PostgreSQL) |

### Servicios Externos

| Servicio | Uso |
|---|---|
| **Google Gemini API** | Motor de inferencia principal para clasificación de archivos desconocidos |
| **Ollama** *(futuro)* | Modelos locales para entornos de alta privacidad |

---

## 📁 Estructura del Proyecto (Cliente Python)

```
dotfiles-manager/
├── cli/
│   ├── commands.py       # Comandos de ejecución
│   ├── console.py        # Sistema de impresión con Rich
│   ├── create.py         # Creador menú parser
│   ├── customs.py        # Vista del menú personalizado
│   └── parser.py         # Parser de comandos
├── core/
│   ├── context.py        # Estado persistente de los steps
│   ├── pipelines.py      # Orquestador secuencial del motor
│   └── steps.py          # Nodos de ejecución del pipeline
├── modules/
│   ├── database/
│   │   ├── manager.py    # Getters y Setters de la BD
│   │   └── models.py     # Modelos de SQLAlchemy
│   └── logger.py         # Sistema de trazas y eventos
├── ui/                   # Interfaz gráfica (PySide6)
├── version.py            # Información del proyecto
├── config.py             # Configuración global del entorno
└── main.py               # Entry point de la aplicación
```

---

## 🗄️ Base de Datos

### Local (SQLite — Cliente)

Tres bloques funcionales:

- **Configuración**: `ui_preferences`, `server_config`, `os_distros_mapping`
- **Inventario relacional**: `categories_apps` → `known_apps_reference` → `local_inventory`
- **Rendimiento**: `global_ignore_rules`, `system_state_hashes` (detección de cambios en O(1))

### Central (SQLite — Servidor)

- **Diccionario Heurístico Global**: vincula hashes estructurales con identificadores de software.
- **Registro LLM**: almacena respuestas de la IA para auditoría y retroalimentación.

---

## 🖥️ Interfaz de Usuario (GUI)

Aplicación con **menú de navegación lateral (Sidebar)** y tres módulos principales:

1. **Dashboard** — Métricas de escaneo, estado de clasificación, volumen de software detectado.
2. **Gestión de Inventario** — Catálogo de aplicaciones, archivos vinculados, archivos desconocidos con opción de consulta al LLM.
3. **Ajustes** — Configuración de la app, reglas de ignorados, exportación/importación, mantenimiento de BD.

---

## 🧪 Testing

- **Cliente Python**: `unittest` + `unittest.mock` para simular sistemas de archivos sin riesgo.
- **Servidor Java**: validación de endpoints con JUnit y Postman.

---

## 🚀 Trabajo Futuro

| Funcionalidad | Descripción |
|---|---|
| **Backups Unificados** | Empaquetado en `tar.gz` para migraciones rápidas entre distribuciones |
| **IA Privada (Ollama)** | Clasificación de archivos con modelos de ejecución local |
| **Automatización (CLI + Cron)** | Modo *headless* para ejecución silenciosa con `cron` o `systemd timers` |

---

## 📄 Documentación Completa

La memoria técnica detallada se encuentra en la carpeta [`docs/`](docs/index.html), organizada en 9 secciones:

1. Introducción y Justificación
2. Objetivos del Proyecto
3. Planificación (Roadmap)
4. Arquitectura del Sistema
5. Stack Tecnológico
6. Diseño de Base de Datos
7. Interfaces UI/UX
8. Implementación y Desarrollo
9. Conclusiones y Trabajo Futuro

---

## 📝 Licencia

*Trabajo de Fin de Grado — Desarrollo de Aplicaciones Multiplataforma (DAM)*
