## 7. Seguridad y autenticación

Dada la naturaleza de este proyecto como Producto Mínimo Viable (MVP) y su enfoque en la **privacidad por diseño**, la seguridad se aborda desde varios niveles.

### Privacidad de los Datos

La principal medida de seguridad es la **anonimización de los datos**:

* El servidor nunca recibe el contenido de los archivos de configuración del usuario.
* Las rutas se normalizan para eliminar cualquier rastro de la identidad del usuario local ($HOME).
* Se utilizan hashes para identificar archivos sin necesidad de almacenar rutas de texto plano legibles si no es estrictamente necesario.

### Acceso a la API

* La API es pública para facilitar las pruebas de integración entre cliente y servidor.
* **Protección de la IA:** El servidor actúa como un "proxy" seguro, evitando que el cliente local tenga que almacenar las API Keys de Google Gemini. Solo el servidor conoce estas credenciales.
* **CORS:** Se han configurado políticas de *Cross-Origin Resource Sharing* flexibles (`allowedOrigins("*")`) para permitir peticiones desde cualquier origen, dado que la herramienta de cliente podría ejecutarse en diversos entornos sin un dominio fijo.


