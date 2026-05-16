El componente más innovador del servidor es su capacidad para deducir la identidad de aplicaciones basándose en firmas estructurales, utilizando modelos de lenguaje avanzados.

### El Procesador de Tareas (TaskProcessorService)

Este servicio es un componente programado (`@Scheduled`) que opera de forma cíclica:

1. **Sondeo:** Busca tareas en estado `QUEUE` con la fecha de creación más antigua.
2. **Bloqueo Optimista:** Cambia el estado a `PROCESSING` para evitar que otras instancias procesen la misma tarea.
3. **Delegación:** Envía los metadatos al motor de IA.

### Integración con Google Gemini (Batch API)

El servidor utiliza la SDK oficial de **Google GenAI** para procesar peticiones masivas mediante la **API Batch** de Gemini. El flujo es el siguiente:

1. **Preparación (JSONL):** Se convierte la lista de rutas desconocidas en un archivo local `.jsonl`, donde cada línea representa una petición individual con el *System Prompt* inyectado.

   *Snippet del System Prompt utilizado:*

   ```text
   Actúa como un experto en administración de sistemas GNU/Linux (específicamente Arch, Manjaro y Debian) y profundo conocedor del estándar XDG Base Directory.
   Tu tarea es analizar un objeto JSON de entrada que describe la aplicación y sus archivos o directorios de configuración (dotfiles) en el directorio ~/. Debes devolver un objeto JSON corregido y completado bajo las siguientes reglas estrictas:
   Reglas de Ejecución:
   Cero Alucinaciones: Basa tus decisiones estrictamente en el comportamiento real del software en distribuciones Linux. Si desconoces la aplicación o no estás 100% seguro de si un path es un fichero o un directorio, asigna el valor "Unknown" en la clave "type" en lugar de inventarlo.
   category: Asigna obligatoriamente UNA de las siguientes categorías principales: Development, System, Network, Multimedia, Games, Productivity, Security, Utilities.
   subcategory: Asigna una subcategoría coherente que dependa de la categoría principal...
   Evaluación de paths: Evalúa cada elemento dentro del array de files_info_json. Determina si el path históricamente corresponde a un archivo ("type": "file") o a un directorio ("type": "folder"). Por ejemplo: .zshrc es file, mientras que .ssh o .config son folder.
   ```
2. **Subida y Ejecución:** El archivo se sube a los servidores de Google y se crea un `BatchJob` asíncrono, utilizando el modelo de inferencia (ej. `gemini-3.1-flash-lite-preview`).
3. **Sondeo:** El servicio comprueba periódicamente el estado del trabajo Batch en la nube.
4. **Consolidación:** Una vez completado, se descargan los resultados estructurados (JSON), se limpian posibles alucinaciones o marcados Markdown, y se guardan las nuevas aplicaciones y rutas en la base de datos central. En este paso se persiste recursivamente la estructura del conocimiento:

   * Se crea o recupera la `CategoryApp` (ej. `Development`).
   * Se crea o recupera la subcategoría `CategoryApp` (ej. `IDEs`) asociada al padre.
   * Se registra la `KnownAppReference` con los detalles parseados.
   * Se desglosa el JSON para indexar individualmente cada ruta en la tabla `app_file_references`, garantizando búsquedas en O(1) para futuros escaneos.
     Finalmente, se marca la tarea como `COMPLETE` y se guarda el JSON final en `resultData`.


---