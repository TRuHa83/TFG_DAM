## Topología Cliente/Servidor

El diseño arquitectónico de **Dotfiles-Manager** se concibe como un sistema distribuido e híbrido que combina el procesamiento en la máquina del usuario (*Edge Computing*) con una capa de conocimiento colectivo en la nube. Los dos nodos principales son:

* **El Cliente Local (Python):** Nodo operativo que reside en el sistema Linux del usuario. Responsable de auditar el sistema de archivos, gestionar la base de datos local (SQLite), ejecutar comandos de sistema (Git Bare) y renderizar la interfaz gráfica (PySide6).
* **El Servidor Central (Java):** Actúa como un oráculo de conocimiento global. No tiene estado de sesión (*Stateless*). Su función es identificar configuraciones mediante consultas a la base de datos central o intermediar con APIs de Inteligencia Artificial (LLMs).

<br>
<div align="center">
    <a href="/assets/ArquitecturaGlobal.webp" target="_blank">
      <img src="/assets/ArquitecturaGlobal.webp" width="100%" alt="Arquitectura Global">
    </a>
</div>
<br>

## Flujo de Datos y Privacidad

La arquitectura sigue el principio de **privacidad por diseño**. Los archivos físicos del usuario **nunca abandonan la máquina local**. El intercambio de información se limita a:

* **Payloads de Metadatos (JSON):** El cliente envía hashes de rutas y firmas estructurales despersonalizadas al servidor.
* **Aprendizaje Colectivo:** Si el servidor identifica un nuevo archivo mediante IA, almacena la relación (Hash -> Aplicación) en su base de datos global, beneficiando a futuros usuarios que posean el mismo archivo.

## Patrones de Diseño Aplicados

* **Modelo-Vista-Controlador (MVC):** Implementado en el cliente Python para desacoplar la interfaz gráfica de la lógica de negocio y la persistencia.
* **Pipeline (Tubería de Datos):** Utilizado en el motor de escaneo local para procesar cada archivo en una secuencia lógica: *Descubrimiento → Heurística → Filtrado → Petición API → Persistencia*.
* **Arquitectura REST:** Define el contrato de comunicación entre el cliente y el servidor, utilizando JSON sobre HTTP con códigos de estado estándar.
* **Task Queue (Cola de Tareas):** En el servidor, las peticiones pesadas (IA) se gestionan mediante una cola asíncrona, permitiendo al cliente realizar *polling* sin bloquear la conexión.



---