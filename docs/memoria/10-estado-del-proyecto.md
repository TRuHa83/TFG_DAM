# Estado Actual del Proyecto

!!! warning "Fase Activa de Desarrollo (Work in Progress)"
    Este Trabajo de Fin de Grado (TFG) se encuentra actualmente en **fase de desarrollo y construcción activa**. 
    
    Tanto el código fuente como la arquitectura evolucionan iterativamente. La información documentada a continuación detalla con precisión técnica el estado real de los componentes principales, diferenciando la funcionalidad operativa de aquella pendiente de implementación.

El propósito de esta página es ofrecer una visión clara y transparente de la madurez del software a día de hoy, focalizándose exclusivamente en el estado del código y la arquitectura de la solución.

---

## Cliente

### Funcionalidades Operativas

- **Motor de Escaneo y Descubrimiento:** La lógica central de auditoría del sistema de archivos local está finalizada. El cliente extrae configuraciones (*dotfiles*) y aplica algoritmos heurísticos para realizar una pre-clasificación de los elementos detectados.
- **Gestión de Aplicaciones:** El panel interactivo para el "Descubrimiento de Aplicaciones" se encuentra totalmente funcional, junto con la interfaz dedicada a la auditoría de "Aplicaciones Desconocidas".
- **Control de Ejecución Local:** Se ha integrado el mecanismo en la interfaz gráfica que permite activar o desactivar dinámicamente cada aplicación descubierta, habilitando o excluyendo su participación en la planificación de tareas del sistema.

### Funcionalidades Pendientes

- **Motor de Tareas Git Bare e Instantáneas:** Falta implementar la lógica de bajo nivel encargada de ejecutar la sincronización y el almacenamiento real de los *dotfiles* mediante versionado de repositorios bare y generación de backups. Tampoco se han definido las vistas de detalle para las tareas individuales.
- **Reestructuración del Dashboard:** Es necesario un rediseño de la vista principal. Actualmente muestra telemetría del hardware y del servidor que debe ser migrada al módulo de ajustes. El dashboard debe pivotar hacia la visualización exclusiva del estado de las tareas (historial, colas y fallos).
- **Módulo de Configuración Global:** Queda pendiente el diseño y construcción de la vista de ajustes generales, la cual controlará el demonio de fondo, las conexiones de red y albergará la telemetría referenciada en el punto anterior.
- **Gestión de Exclusiones (Ignore Rules):** Se requiere programar la lógica y el panel de administración que permita definir patrones o directorios excluidos durante las iteraciones del motor de escaneo.

---

## Servidor

### Funcionalidades Operativas

- **Resolución mediante IA:** El núcleo operativo se encuentra funcional. El backend recibe peticiones, procesa el contexto del sistema de archivos y se comunica con la API de Google Gemini para catalogar aplicaciones desconocidas.
- **Persistencia y Generación de Tareas:** La capa de acceso a datos está activa. El servidor estructura las resoluciones proporcionadas por la IA y las persiste localmente como tareas ejecutables.
- **Flujo End-to-End Bidireccional:** El ciclo completo de comunicación opera correctamente. El servidor ingiere peticiones del cliente, procesa la carga de trabajo con la IA y devuelve una respuesta estructurada con la nueva metadata lista para su integración local.

### Funcionalidades Pendientes

- **Empaquetado y Despliegue:** Es necesario generar el entorno de contenedores (`Dockerfile` y `docker-compose.yml`) para asegurar la portabilidad y habilitar un despliegue estandarizado en entornos productivos.
- **Seguridad y Autenticación:** Actualmente la API opera sin restricciones. Se debe implementar un sistema de registro y autenticación para que el cliente genere una cuenta de usuario y el servidor pueda validar las peticiones mediante un control de autorización.
- **Control de Concurrencia (Rate Limiting):** Requiere el desarrollo de una arquitectura de límites en el backend. Las peticiones y tareas deben asociarse a un cliente autenticado específico para prevenir la saturación por peticiones simultáneas no controladas.


---