## Ciclo de vida del software

Para este proyecto se ha seguido una metodología **Ágil** basada en iteraciones, permitiendo una adaptación rápida a los descubrimientos técnicos realizados durante el desarrollo (especialmente en la integración de Git Bare y las APIs de IA).

## Fases del proyecto

1. **Investigación y Análisis:** Estudio de las herramientas actuales (Stow, dotdrop) y análisis de la técnica Git Bare.
2. **Diseño de Arquitectura:** Definición del contrato de la API REST y del modelo de datos local/remoto.
3. **Desarrollo del Core (Sprints):**
   * *Sprint 1:* Motor de escaneo y lógica de Git en Python.
   * *Sprint 2:* Backend Java y gestión de tareas.
   * *Sprint 3:* Integración de IA y servicios de polling.
   * *Sprint 4:* Interfaz gráfica (PySide6).
4. **Pruebas e Integración:** Validación de los flujos de datos entre cliente y servidor.
5. **Documentación:** Redacción de la memoria técnica y manuales de usuario.

## Herramientas de desarrollo

* **Control de Versiones:** Git y GitHub para el alojamiento del código.
* **Gestión de Dependencias:** `uv` para el entorno Python y `Maven` para el proyecto Java.
* **Entornos de Desarrollo (IDE):** Visual Studio Code y IntelliJ IDEA.
* **Diseño de UI:** Qt Designer para la creación de las interfaces gráficas.



---