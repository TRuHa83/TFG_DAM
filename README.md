<div id="dotfiles-manager" align="center">
  <h1>Dotfiles-Manager</h1>
  <p><strong>Sistema Distribuido de Gestión y Clasificación de Entornos Linux</strong></p>
  <p><em>Trabajo de Fin de Grado — DAM · Curso 2024/2026</em></p>

  <p>
    <a href="https://truha83.github.io/TFG_DAM/">
      <img src="https://img.shields.io/badge/Documentación-MkDocs-blue?style=for-the-badge&logo=markdown&logoColor=white" alt="Documentación">
    </a>
    <a href="dotfiles-manager/">
      <img src="https://img.shields.io/badge/Cliente-Python-green?style=for-the-badge&logo=python&logoColor=white" alt="Cliente">
    </a>
    <a href="dotfiles_server/">
      <img src="https://img.shields.io/badge/Servidor-Java-red?style=for-the-badge&logo=spring&logoColor=white" alt="Servidor">
    </a>
  </p>
</div>



## 📖 Acerca del Proyecto

**Dotfiles-Manager** es una solución integral para la gestión de archivos de configuración (*dotfiles*) en Linux. El sistema utiliza una arquitectura distribuida para permitir el escaneo local, la clasificación inteligente mediante Inteligencia Artificial (Google Gemini) y la gestión de estas configuraciones.

Este repositorio está estructurado como un **monorepositorio**, albergando tanto el código fuente del cliente de escritorio como del servidor en la nube, además de la documentación oficial completa.

---

## 🏗️ Estructura del Monorepo

El repositorio se divide en tres bloques principales. Cada componente de software cuenta con su propio `README.md` específico con instrucciones detalladas de instalación, configuración y uso local:

- 💻 [**Cliente (PySide6)**](dotfiles-manager/README.md): Aplicación de escritorio y CLI desarrollada en Python 3.13 con PySide6 y gestionada con `uv`. Se encarga de analizar el entorno local y comunicarse con el servidor.
- ☁️ [**Servidor (Spring Boot)**](dotfiles_server/README.md): Backend desarrollado en Java 21 con Spring Boot 3. Gestiona las colas de peticiones asíncronas y se comunica con la API de Google Gemini para clasificar dotfiles desconocidos.
- 📚 [**Documentación (MkDocs)**](docs/): Código fuente de la documentación del proyecto construida con MkDocs Material.

---

## 📚 Documentación Oficial

Toda la memoria técnica, análisis de requisitos, arquitectura y guías de uso se encuentran documentadas exhaustivamente y publicadas mediante GitHub Pages:

👉 **[Visitar la Wiki Oficial del Proyecto](https://truha83.github.io/TFG_DAM/)**

---

## 🛠️ Tecnologías Principales

- **Cliente:** Python 3.13, PySide6, SQLAlchemy, Rich, SQLite.
- **Servidor:** Java 21 (LTS), Spring Boot 3.5, Spring AI (Gemini), Hibernate, SQLite.
- **Documentación:** Markdown, MkDocs, Material for MkDocs.

---

> [!WARNING] 
> Este proyecto se encuentra en fase de desarrollo activo. Para conocer con exactitud qué características ya están implementadas y cuáles faltan, consulta la sección **[Estado del Proyecto](https://truha83.github.io/TFG_DAM/memoria/10-estado-del-proyecto/)** en nuestra Wiki.

---

<div align="center">
  <p><strong>Autor:</strong> Sergio Trujillo de la Nuez</p>
  <p><strong>Año:</strong> 2024 - 2026</p>
</div>
