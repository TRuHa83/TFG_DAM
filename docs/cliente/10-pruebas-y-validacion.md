## 10. Pruebas y validación

La calidad del software se garantiza mediante una estrategia de pruebas multinivel, utilizando el framework **pytest**.

### Pruebas Unitarias

Se validan de forma aislada las funciones más críticas:

* Lógica de filtrado de archivos (RegEx).
* Correcto funcionamiento del motor de hashes.
* Validación de la integridad de los modelos de base de datos local.

### Pruebas de Integración

* Simulación de flujos completos: Escaneo -> Clasificación -> Commit en Git Bare.
* Pruebas de comunicación: Verificación del intercambio de JSON con el servidor (usando mocks o servidores de prueba).

### Validación de Usuario

Pruebas manuales en diferentes distribuciones de Linux (Arch, Ubuntu) para asegurar que las rutas por defecto y el comportamiento de la interfaz son consistentes en distintos entornos de escritorio (KDE, GNOME).


