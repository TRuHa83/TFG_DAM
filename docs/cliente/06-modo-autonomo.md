**Dotfiles-Manager** ha sido diseñado bajo la premisa de "Local First". Esto significa que la herramienta es totalmente funcional sin conexión a internet o sin acceso al servidor central Java para sus tareas críticas de gestión.

### Funcionamiento Offline

Cuando el cliente detecta que el servidor no está disponible (o si el usuario prefiere operar de forma aislada):

* **Auditoría Local:** El escaneo utiliza exclusivamente la base de datos `known_apps_reference` precargada en el SQLite local.
* **Versionado con Git Bare:** Todas las operaciones de commit, historial y recuperación de archivos ocurren localmente en la máquina del usuario.
* **Gestión de Desconocidos:** Los archivos que no pueden ser identificados localmente se almacenan en una cola de "pendientes". El usuario puede clasificarlos manualmente o esperar a recuperar la conexión para usar el servicio de clasificación remoto.

El aislamiento del cliente frente al servidor se logra mediante una arquitectura basada en caché. La tabla `server_tasks` actúa como un búfer transaccional. En el momento en que el servidor vuelve a estar en línea, el cliente puede "despachar" la cola de archivos desconocidos acumulados, recibiendo las clasificaciones de forma masiva y actualizando el inventario local retrospectivamente.


---