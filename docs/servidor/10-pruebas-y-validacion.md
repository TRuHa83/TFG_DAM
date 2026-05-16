Para garantizar la fiabilidad del backend y la integridad de las respuestas entregadas a los clientes, el servidor Java cuenta con una estrategia de pruebas basada en el ecosistema de Spring Boot.

### Pruebas Unitarias con JUnit 5

Se validan de forma aislada los componentes de lógica pura:

* **Mapeo de Entidades a DTOs:** Verificación de que no se filtran datos sensibles y que los campos coinciden.
* **Lógica de Negocio:** Validación de que los estados de las tareas (`QUEUE`, `PROCESSING`, `COMPLETE`) transicionan correctamente ante diferentes escenarios.

### Pruebas de Integración con MockMvc

Se simulan peticiones HTTP reales a los controladores para validar:

* Correcto funcionamiento de los endpoints `/discovery`, `/task/{id}` y `/health`.
* Serialización y deserialización correcta del formato JSON.
* Gestión de errores y devolución de códigos de estado HTTP adecuados.

### Pruebas de Persistencia con H2 (In-Memory)

Aunque el sistema utiliza SQLite en producción, las pruebas de base de datos se realizan contra una base de datos **H2** en memoria, asegurando que las consultas JPA y las restricciones de integridad funcionan correctamente en cada compilación del proyecto.

### Validación de la API de IA

Se utilizan **Mocks** de los servicios de Spring AI para simular las respuestas de Google Gemini. Esto permite probar el comportamiento del servidor ante diferentes respuestas de la IA (clasificaciones exitosas, errores de formato, timeouts) sin incurrir en costes de API ni depender de la conectividad externa durante los tests.


---