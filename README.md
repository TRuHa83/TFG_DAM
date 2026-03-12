# Dotfiles-Manager
> **Sistema Distribuido de Gestión y Clasificación de Entornos Linux**<br>Trabajo de Fin de Grado (DAM)

<div align="center">
  <h2>📖 <a href="https://truha83.github.io/TFG_DAM/">Consulta la Memoria Técnica Completa</a></h2>
  <p><i>Toda la información detallada sobre arquitectura, bases de datos, stack tecnológico e implementación metodológica reside en la documentación oficial.</i></p>
</div>

---

## 📌 Resumen del Proyecto

> ⚠️ **Estado del Proyecto:** Actualmente en fase de **desarrollo activo (WIP)**.

**¿Qué hace?**  
**Dotfiles-Manager** es un ecosistema cliente/servidor diseñado para descubrir, auditar, clasificar inteligentemente y versionar de forma automática los archivos de configuración (*dotfiles*) en entornos UNIX/Linux.

**¿Cómo lo hace?**  
- **Descubrimiento:** Utiliza heurística local y el estándar XDG para encontrar configuraciones en el entorno del usuario.
- **Versionado (*Zero-Friction*):** Aplica la técnica **Git Bare Repository** para versionar los archivos *in situ*, eliminando la necesidad de moverlos de su ubicación original.
- **Clasificación Inteligente:** Se apoya en una API REST (Java 21) y Modelos de Lenguaje (LLMs como Google Gemini) para identificar configuraciones desconocidas, enviando únicamente metadatos (hashes y firmas) para garantizar la **privacidad total** de los ficheros del usuario.

**¿Qué retos supera?**  
Deja atrás los problemas de los gestores tradicionales basados en enlaces simbólicos (*symlinks* como GNU Stow) o scripts manuales y complejos. Elimina la fricción organizativa, automatiza el control de versiones y aporta inteligencia para descifrar para qué sirve cada archivo de configuración oculto en el sistema.

**¿A quién va dirigido?**  
Principalmente está diseñado para **nuevos usuarios de Linux**, ayudándoles a romper la gran barrera de entrada técnica y mitigar la enorme complejidad que conlleva la gestión manual de los *dotfiles*. Adicionalmente, es una solución ideal para **administradores de sistemas, desarrolladores y entusiastas de la personalización (*ricers*)** que buscan mantener sus entornos sincronizados sin esfuerzo manual.

---

<div align="center">
  <h3>➡️ Para conocer el código, los patrones de diseño y las decisiones técnicas, accede a la <a href="https://truha83.github.io/TFG_DAM/">Documentación del Proyecto</a>.</h3>
</div>

<br>
<p align="center">
  <small><em>Trabajo de Fin de Grado — Desarrollo de Aplicaciones Multiplataforma (DAM)</em></small>
</p>
