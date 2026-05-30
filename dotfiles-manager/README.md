# dotfiles-manager

> **Componente cliente** del sistema distribuido de gestión y clasificación de dotfiles para Linux.
> Aplicación de escritorio (PySide6) con interfaz CLI complementaria.

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.x-41CD52?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![uv](https://img.shields.io/badge/gestor-uv-7C3AED)](https://docs.astral.sh/uv/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite)](https://www.sqlite.org/)

---

## ¿Qué hace?

`dotmng` es el cliente local del sistema **Dotfiles-Manager**. Analiza el directorio `$HOME`
del usuario, clasifica los ficheros de configuración (dotfiles) encontrados, los identifica
con aplicaciones conocidas y gestiona un inventario local.

Se comunica con el [servidor Java](../dotfiles_server/README.md) para clasificar mediante
IA (Google Gemini) los dotfiles desconocidos.

→ Documentación técnica completa: [Wiki Cliente](https://truha83.github.io/TFG_DAM/cliente/01-introduccion/)
→ Memoria del TFG: [Wiki Principal](https://truha83.github.io/TFG_DAM/)

---

## Requisitos previos

| Herramienta | Versión mínima | Notas |
|---|---|---|
| Python | 3.13 | Requerido |
| [uv](https://docs.astral.sh/uv/) | última | Gestor de dependencias y entornos |
| Nerd Fonts | cualquiera | Para iconos en la CLI (recomendado) |

---

## Instalación

`dotmng` ofrece un proceso de instalación sumamente versátil y profesional gracias a su script automatizado de instalación `install.sh` y al uso del gestor de paquetes moderno **uv**.

Elige el método que mejor se adapte a tus necesidades:

### 1. Instalación Automática y Directa (Recomendado)
Es el método más rápido y limpio. Descarga y ejecuta el asistente de instalación directamente desde el repositorio oficial de GitHub sin necesidad de clonar el código fuente:

**Usando cURL:**
```bash
curl -sSL https://raw.githubusercontent.com/TRuHa83/TFG_DAM/main/dotfiles-manager/install.sh | bash
```

**Usando wget:**
```bash
wget -qO- https://raw.githubusercontent.com/TRuHa83/TFG_DAM/main/dotfiles-manager/install.sh | bash
```

> [!NOTE]
> **¿Qué hace el instalador por ti?**
> * Verifica la compatibilidad de tu entorno Linux y la disponibilidad de `uv`.
> * Instala `dotmng` de manera segura y aislada en tu entorno de usuario usando `uv tool`.
> * Descarga los recursos visuales (iconos y archivo `.desktop`) y los configura automáticamente en tu sistema de escritorio (`~/.local/share/applications` y `~/.local/share/icons`).
> * Verifica tu variable `$PATH` y te proporciona instrucciones precisas si necesitas actualizarla.

---

### 2. Instalación Directa con `uv tool` (Sin clonar repositorio)
Si prefieres saltarte la configuración visual (entrada `.desktop`) e instalar únicamente la herramienta de línea de comandos de forma rápida e independiente con `uv`:

```bash
uv tool install --force "git+https://github.com/TRuHa83/TFG_DAM.git#subdirectory=dotfiles-manager"
```

---

### 3. Instalación Local / Modo Desarrollo
Si deseas examinar el código, realizar modificaciones o utilizar el instalador interactivo de forma local:

```bash
# 1. Clonar el repositorio completo
git clone https://github.com/TRuHa83/TFG_DAM.git
cd TFG_DAM/dotfiles-manager

# 2. Ejecutar el asistente de instalación local interactivo
chmod +x install.sh
./install.sh
```

Si eres desarrollador y prefieres trabajar en un entorno virtual aislado sin registrar la herramienta de forma global en tu sistema:

```bash
# Sincronizar dependencias en el entorno virtual
uv sync

# Ejecutar en modo desarrollo
uv run dotmng
```

---

### Desinstalación Limpia
Si necesitas desinstalar completamente la aplicación y remover todos los accesos directos e iconos generados, ejecuta el comando de desinstalación integrado:

```bash
dotmng uninstall
```

---

## Uso

### Interfaz gráfica (GUI)

Si se instaló globalmente en el sistema:
```bash
dotmng
```

Si se ejecuta desde el código fuente clonado localmente:
```bash
uv run dotmng
```

En el primer arranque se abrirá un diálogo de configuración inicial (`FirstRunDialog`) donde se establece la conexión con el servidor.

### Interfaz de línea de comandos (CLI)

Puedes utilizar `dotmng` directamente (o anteponer `uv run` si estás en el directorio de desarrollo local):

```bash
# Auditar el $HOME sin guardar cambios
dotmng check

# Actualizar el inventario local
dotmng update

# Listar aplicaciones conocidas en el inventario
dotmng apps list

# Vincular una ruta manualmente a una aplicación
dotmng apps bind <ruta> <app_id>

# Gestionar dotfiles desconocidos
dotmng unknown list

# Utilidades del sistema
dotmng utils --help

# Ayuda general
dotmng --help
```

---

## Configuración

La aplicación respeta el estándar **XDG Base Directory**:

| Ruta | Contenido |
|---|---|
| `~/.local/share/dotmng/data.db` | Base de datos SQLite local |
| `~/.local/state/dotmng/` | Ficheros de log (rotación diaria, 30 días) |
| `~/.cache/dotmng/` | Caché de iconos y descargas temporales |

La URL del servidor se configura desde la GUI en `Ajustes → Servidor`.

---

## Dependencias principales

| Librería | Uso |
|---|---|
| `PySide6` | Interfaz gráfica Qt 6 |
| `SQLAlchemy` | ORM para la base de datos SQLite local |
| `Rich` | Salida enriquecida en la CLI (tablas, colores, iconos) |
| `python-dotenv` | Carga de variables de entorno desde `.env` |
| `pytest` | Framework de pruebas (en migración desde unittest) |

---

## Estructura del proyecto

```
dotfiles-manager/
├── src/dotmng/
│   ├── cli/            # Comandos, parser argparse, consola Rich
│   ├── core/           # Motor Pipeline: context, steps, reporter
│   ├── data/           # xdg_data.json y scripts de inicialización de BD
│   ├── modules/
│   │   ├── api/        # ServerPoller y TaskPoller (QThread)
│   │   └── database/   # Modelos SQLAlchemy y gestor de BD
│   ├── ui/             # Ventana principal PySide6, formularios Qt, widgets
│   ├── config.py       # Configuración global (rutas XDG)
│   ├── main.py         # Punto de entrada
│   └── version.py      # Metadatos de versión
├── tests/              # Pruebas pytest
├── pyproject.toml      # Configuración del proyecto
└── install.sh          # Script de instalación asistida
```

---

## Ejecutar pruebas

```bash
uv run pytest tests/ -v
```

---

## Documentación técnica

- [Stack tecnológico](https://truha83.github.io/TFG_DAM/cliente/02-entorno-y-dependencias/)
- [Base de datos local (SQLAlchemy)](https://truha83.github.io/TFG_DAM/cliente/04-base-de-datos-local/)
- [Interfaces CLI y GUI](https://truha83.github.io/TFG_DAM/cliente/08-interfaz-de-usuario/)
- [Implementación y estructura](https://truha83.github.io/TFG_DAM/cliente/03-arquitectura-interna/)
- [Arquitectura del sistema completo](https://truha83.github.io/TFG_DAM/memoria/07-arquitectura-del-sistema/)
