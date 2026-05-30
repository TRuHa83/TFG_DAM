package dev.techcrafted.dotfile_server.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.google.common.collect.ImmutableList;
import com.google.genai.Client;
import com.google.genai.types.*;
import dev.techcrafted.dotfile_server.model.*;
import dev.techcrafted.dotfile_server.repository.AppFileReferenceRepository;
import dev.techcrafted.dotfile_server.repository.CategoryAppRepository;
import dev.techcrafted.dotfile_server.repository.KnownAppReferenceRepository;
import dev.techcrafted.dotfile_server.repository.TaskRepository;

import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import dev.techcrafted.dotfile_server.dto.AppDetailDTO;

@Service
@Slf4j
public class TaskProcessorService {

    private static final Logger geminiLogger = LoggerFactory.getLogger("gemini-logger");

    @Autowired
    private TaskRepository taskRepository;

    @Autowired
    private CategoryAppRepository categoryRepository;

    @Autowired
    private KnownAppReferenceRepository knownAppRepository;

    @Autowired
    private AppFileReferenceRepository appFileRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @Value("${spring.ai.google.genai.api-key}")
    private String apiKey;

    @Value("${spring.ai.google.genai.batch-model:gemini-3.1-pro-preview}")
    private String batchModel;

    @Value("${spring.ai.google.genai.sync-model:gemini-2.5-flash}")
    private String syncModel;

    @Value("${spring.ai.google.genai.polling-interval-ms:30000}")
    private long pollingIntervalMs;

    private static final String SYS_PROMPT = "Actúa como un experto en administración de sistemas GNU/Linux (específicamente Arch, Manjaro y Debian) y profundo conocedor del estándar XDG Base Directory. "
            +
            "Tu tarea es analizar un objeto JSON de entrada que describe la aplicación y sus archivos o directorios de configuración (dotfiles) en el directorio ~/. Debes devolver un objeto JSON corregido y completado bajo las siguientes reglas estrictas: "
            +
            "Reglas de Ejecución: " +
            "Cero Alucinaciones: Basa tus decisiones estrictamente en el comportamiento real del software en distribuciones Linux. Si desconoces la aplicación o no estás 100% seguro de si un path es un fichero o un directorio, asigna el valor \"Unknown\" en la clave \"type\" en lugar de inventarlo. "
            +
            "category: Asigna obligatoriamente UNA de las siguientes categorías principales: Development, System, Network, Multimedia, Games, Productivity, Security, Utilities. "
            +
            "subcategory: Asigna una subcategoría coherente que dependa de la categoría principal (ej. Shell, Desktop Environment, Package Management, Cloud, DevOps, Audio, Video, P2P, Browser, Database, Editor, etc.). "
            +
            "Evaluación de paths: Evalúa cada elemento dentro del array de files_info_json. Determina si el path históricamente corresponde a un archivo (\"type\": \"file\") o a un directorio (\"type\": \"folder\"). Por ejemplo: .zshrc es file, mientras que .ssh o .config son folder.";

    /**
     * Al arrancar la aplicación, recupera tareas que se quedaron en estado
     * PROCESSING
     * y retoma su polling asíncronamente.
     */
    @EventListener(ApplicationReadyEvent.class)
    public void resumeInterruptedTasks() {
        log.info("Buscando tareas interrumpidas para reanudar...");
        List<Task> pendingTasks = taskRepository.findAllByStatusAndBatchIdIsNotNull(TaskStatus.PROCESSING);

        if (pendingTasks.isEmpty()) {
            log.info("No hay tareas pendientes para reanudar.");
            return;
        }

        log.info("Reanudando {} tareas interrumpidas...", pendingTasks.size());
        for (Task task : pendingTasks) {
            new Thread(() -> resumeTaskPolling(task)).start();
        }
    }

    private void resumeTaskPolling(Task task) {
        try {
            log.info("Reanudando polling para tarea: {} (Batch ID: {})", task.getId(), task.getBatchId());
            geminiLogger.info("========================================= RESUMING BATCH TASK POLLING ==================================");
            geminiLogger.info("Task ID: {}", task.getId());
            geminiLogger.info("Batch ID: {}", task.getBatchId());
            geminiLogger.info("--------------------------------------------------------------------------------------------------------");

            Client client = Client.builder().apiKey(apiKey).build();
            String jobName = task.getBatchId();

            // Retomamos directamente el bucle de polling
            boolean completed = false;
            BatchJob batchJob = null;
            String lastState = null;

            while (!completed) {
                batchJob = client.batches.get(jobName, null);
                String state = batchJob.state().get().toString();
                if (!state.equals(lastState)) {
                    log.info("Estado reanudado para {}: {}", task.getId(), state);
                    geminiLogger.info("Resumed Batch Job status for {}: {}", jobName, state);
                    lastState = state;
                }

                if ("JOB_STATE_SUCCEEDED".equals(state)) {
                    completed = true;
                } else if ("JOB_STATE_FAILED".equals(state) || "JOB_STATE_CANCELLED".equals(state)
                        || "JOB_STATE_EXPIRED".equals(state)) {
                    throw new Exception("El Batch Job reanudado terminó con estado: " + state);
                } else {
                    Thread.sleep(pollingIntervalMs);
                }
            }

            geminiLogger.info("--------------------------------------------------------------------------------------------------------");
            geminiLogger.info("Resumed Batch Job succeeded. Retrieving and parsing results...");

            // Procesar los resultados
            Map<String, String> originalTypes = extractOriginalTypes(task.getInputData());
            List<KnownAppReference> results = processAndPersistResults(batchJob, originalTypes);
            Map<String, AppDetailDTO> resultsMap = results.stream()
                    .collect(Collectors.toMap(
                            KnownAppReference::getAppId,
                            app -> AppDetailDTO.fromKnownAppReference(app, objectMapper),
                            (existing, replacement) -> existing));
            task.setResultData(objectMapper.writeValueAsString(resultsMap));

            task.setStatus(TaskStatus.COMPLETE);
            taskRepository.save(task);
            log.info("Tarea reanudada finalizada con éxito: {}", task.getId());
            geminiLogger.info("Resumed Task {} successfully completed. Results mapped: {} apps", task.getId(), results.size());
            geminiLogger.info("========================================================================================================\n");

        } catch (Exception e) {
            handleError(task, "Fallo al reanudar tarea", e);
            geminiLogger.error("Error during resumed Batch Task processing:", e);
            geminiLogger.info("========================================================================================================\n");
        }
    }

    // Se ejecuta cada 2 segundos
    @Scheduled(fixedDelay = 2000)
    public void processNextTask() {
        Optional<Task> optionalTask = taskRepository.findFirstByStatusOrderByCreatedAtAsc(TaskStatus.QUEUE);
        if (optionalTask.isPresent()) {
            Task task = optionalTask.get();
            log.info("Tarea encontrada en cola: {}", task.getId());

            task.setStatus(TaskStatus.PROCESSING);
            taskRepository.save(task);

            // Iniciamos el procesamiento en un hilo separado o directamente aquí (al ser
            // @Scheduled)
            processTask(task);
        }
    }

    @Transactional
    public void processTask(Task task) {
        try {
            log.info("Iniciando procesamiento de tarea: {}", task.getId());
            geminiLogger.info("========================================= BATCH REQUEST STARTED ========================================");
            geminiLogger.info("Task ID: {}", task.getId());
            geminiLogger.info("Input Data Raw:\n{}", task.getInputData());
            geminiLogger.info("System Prompt:\n{}", SYS_PROMPT);
            geminiLogger.info("Model: {}", batchModel);
            geminiLogger.info("--------------------------------------------------------------------------------------------------------");

            Client client = Client.builder()
                    .apiKey(apiKey)
                    .build();

            // 1. Preparar el archivo JSONL para el Batch
            String jsonlPath = prepareJsonlFile(task);
            if (jsonlPath == null) {
                throw new Exception("Error al preparar el archivo JSONL");
            }

            // Registrar contenido de JSONL preparado para depuración
            try {
                String jsonlContent = Files.readString(Path.of(jsonlPath));
                geminiLogger.info("Prepared JSONL File Content:\n{}", jsonlContent);
                geminiLogger.info("--------------------------------------------------------------------------------------------------------");
            } catch (Exception ex) {
                geminiLogger.warn("Could not read JSONL file content for logging: {}", ex.getMessage());
            }

            // 2. Subir el archivo a Gemini
            UploadFileConfig uploadConfig = UploadFileConfig.builder()
                    .displayName("batch-" + task.getId())
                    .mimeType("application/jsonl")
                    .build();

            // Acceso directo a la propiedad 'files' (sin paréntesis)
            com.google.genai.types.File uploadedFile = client.files.upload(jsonlPath, uploadConfig);
            log.info("Archivo subido a Gemini: {}", uploadedFile.name().get());
            geminiLogger.info("Uploaded File Name in Gemini: {}", uploadedFile.name().get());

            // 3. Crear el Batch Job
            BatchJobSource source = BatchJobSource.builder()
                    .fileName(uploadedFile.name().get())
                    .build();

            CreateBatchJobConfig jobConfig = CreateBatchJobConfig.builder()
                    .displayName("job-" + task.getId())
                    .build();

            // Acceso directo a la propiedad 'batches'
            // Usamos el modelo configurado
            BatchJob batchJob = client.batches.create(batchModel, source, jobConfig);
            String jobName = batchJob.name().get();
            log.info("Batch Job creado: {}", jobName);
            geminiLogger.info("Batch Job Created. Job Name: {}", jobName);

            // GUARDAR EL BATCH ID EN LA TAREA
            task.setBatchId(jobName);
            task.setStatus(TaskStatus.PROCESSING);
            taskRepository.save(task);

            // 4. Polling del estado del Job
            boolean completed = false;
            String lastState = null;
            while (!completed) {
                Thread.sleep(pollingIntervalMs);
                batchJob = client.batches.get(jobName, null);
                String state = batchJob.state().get().toString();
                if (!state.equals(lastState)) {
                    log.info("Estado del Job {}: {}", task.getId(), state);
                    geminiLogger.info("Batch Job status for {}: {}", jobName, state);
                    lastState = state;
                }

                if ("JOB_STATE_SUCCEEDED".equals(state)) {
                    completed = true;
                } else if ("JOB_STATE_FAILED".equals(state) || "JOB_STATE_CANCELLED".equals(state)
                        || "JOB_STATE_EXPIRED".equals(state)) {
                    throw new Exception("El Batch Job terminó con estado: " + state);
                }
            }

            geminiLogger.info("--------------------------------------------------------------------------------------------------------");
            geminiLogger.info("Batch Job succeeded. Retrieving and parsing results...");

            // 5. Procesar los resultados
            Map<String, String> originalTypes = extractOriginalTypes(task.getInputData());
            List<KnownAppReference> results = processAndPersistResults(batchJob, originalTypes);
            Map<String, AppDetailDTO> resultsMap = results.stream()
                    .collect(Collectors.toMap(
                            KnownAppReference::getAppId,
                            app -> AppDetailDTO.fromKnownAppReference(app, objectMapper),
                            (existing, replacement) -> existing));
            task.setResultData(objectMapper.writeValueAsString(resultsMap));

            task.setStatus(TaskStatus.COMPLETE);
            taskRepository.save(task);

            log.info("Tarea completada con éxito: {}", task.getId());
            geminiLogger.info("Task {} successfully completed. Results mapped: {} apps", task.getId(), results.size());
            geminiLogger.info("========================================================================================================\n");

            // Limpieza
            Files.deleteIfExists(Path.of(jsonlPath));

        } catch (InterruptedException e) {
            handleError(task, "Error por interrupción", e);
            geminiLogger.error("Interrupted Exception during Batch Task processing:", e);
            geminiLogger.info("========================================================================================================\n");
            Thread.currentThread().interrupt();
        } catch (Exception e) {
            handleError(task, "Error en el procesamiento", e);
            geminiLogger.error("Error during Batch Task processing:", e);
            geminiLogger.info("========================================================================================================\n");
        }
    }

    @Transactional
    public List<KnownAppReference> processAndPersistResults(BatchJob batchJob, Map<String, String> originalTypes) throws Exception {
        log.info("Procesando resultados del Batch Job: {}", batchJob.name().get());
        List<KnownAppReference> allPersistedApps = new java.util.ArrayList<>();

        if (!batchJob.dest().isPresent()) {
            log.warn("El Job no tiene información de destino de resultados.");
            geminiLogger.warn("Batch Job has no destination info.");
            return allPersistedApps;
        }

        BatchJobDestination dest = batchJob.dest().get();
        Client client = Client.builder().apiKey(apiKey).build();

        // CASO A: Los resultados están en un archivo (Recomendado para Batch)
        if (dest.fileName().isPresent()) {
            String resultFileName = dest.fileName().get();
            log.info("Resultados encontrados en archivo: {}", resultFileName);
            geminiLogger.info("Batch results found in file: {}", resultFileName);

            // Crear un archivo temporal local para la descarga
            Path localTempFile = Files.createTempFile("gemini-results-", ".json");
            try {
                // Descargar el contenido del archivo a la ruta local
                client.files.download(resultFileName, localTempFile.toAbsolutePath().toString(), null);

                // Leer el contenido del archivo descargado
                List<String> lines = Files.readAllLines(localTempFile);

                // Cada línea en el archivo de salida suele ser un objeto JSON de respuesta
                for (String line : lines) {
                    if (line.trim().isEmpty())
                        continue;
                    log.debug("Procesando línea de archivo de resultados: {}", line);
                    geminiLogger.info("Batch response line:\n{}", sanitizeForLogging(line));
                    allPersistedApps.addAll(processRawResponseText(line, originalTypes));
                }
            } finally {
                // Limpiar el archivo temporal
                Files.deleteIfExists(localTempFile);
            }
        }
        // CASO B: Los resultados vienen inlined (Solo para batches muy pequeños)
        else if (dest.inlinedResponses().isPresent()) {
            log.info("Resultados encontrados inlined (en la respuesta)");
            geminiLogger.info("Batch results found inlined");
            for (InlinedResponse inlineResponse : dest.inlinedResponses().get()) {
                if (inlineResponse.response().isPresent()) {
                    String text = inlineResponse.response().get().text();
                    geminiLogger.info("Batch inlined response text:\n{}", sanitizeForLogging(text));
                    allPersistedApps.addAll(processRawResponseText(text, originalTypes));
                }
            }
        } else {
            log.warn("No se encontraron resultados ni en archivo ni inlined para el Job {}", batchJob.name().get());
            geminiLogger.warn("No results found in file or inlined for the Job: {}", batchJob.name().get());
        }
        return allPersistedApps;
    }

    private List<KnownAppReference> processRawResponseText(String text, Map<String, String> originalTypes) {
        List<KnownAppReference> apps = new java.util.ArrayList<>();
        try {
            // Limpiar markdown si existiera
            String cleanJson = text.replaceAll("```json", "").replaceAll("```", "").trim();
            log.info("Procesando respuesta JSON de Gemini...");
            geminiLogger.info("Extracted clean JSON from response:\n{}", sanitizeForLogging(cleanJson));

            JsonNode rootNode = objectMapper.readTree(cleanJson);

            // A veces la respuesta batch envuelve la respuesta real en un objeto {response:
            // { ... }}
            if (rootNode.has("response")) {
                rootNode = rootNode.get("response");
                // Y a veces dentro de candidates[0].content.parts[0].text
                if (rootNode.has("candidates")) {
                    JsonNode candidate = rootNode.get("candidates").get(0);
                    if (candidate.has("content")) {
                        JsonNode content = candidate.get("content");
                        if (content.has("parts")) {
                            String innerText = content.get("parts").get(0).get("text").asText();
                            rootNode = objectMapper
                                    .readTree(innerText.replaceAll("```json", "").replaceAll("```", "").trim());
                        }
                    }
                }
            }

            if (rootNode.has("apps")) {
                JsonNode appsNode = rootNode.get("apps");
                if (appsNode.isArray()) {
                    for (JsonNode appNode : appsNode) {
                        apps.add(persistAppNode(appNode, originalTypes));
                    }
                }
            } else if (rootNode.isArray()) {
                // Si devuelve directamente el array
                for (JsonNode appNode : rootNode) {
                    apps.add(persistAppNode(appNode, originalTypes));
                }
            } else {
                log.warn("El JSON no tiene el formato esperado (falta clave 'apps'). Ver detalles en gemini.log.");
                geminiLogger.warn("El JSON no tiene el formato esperado (falta clave 'apps'): {}", cleanJson);
            }
        } catch (Exception e) {
            log.error("Error al procesar texto de respuesta: {}. Ver detalles en gemini.log.", e.getMessage());
            geminiLogger.error("Error al procesar texto de respuesta: {}. Texto original: {}", e.getMessage(), text);
        }
        return apps;
    }

    @Transactional
    public KnownAppReference persistAppNode(JsonNode appNode, Map<String, String> originalTypes) {
        String appKey = appNode.get("app_key").asText();
        String appName = appNode.get("app_name").asText();
        String categoryName = appNode.get("category").asText();
        String subcategoryName = appNode.get("subcategory").asText();

        boolean isUnknown = "Unknown".equalsIgnoreCase(appName) 
                || (categoryName != null && "Unknown".equalsIgnoreCase(categoryName))
                || (subcategoryName != null && "Unknown".equalsIgnoreCase(subcategoryName));

        if (isUnknown) {
            log.info("Aplicación clasificada como Unknown: {} ({}) - Saltando persistencia en BD del servidor.", appName, appKey);
            
            CategoryApp tempCategory = new CategoryApp(categoryName, null);
            CategoryApp tempSubcategory = new CategoryApp(subcategoryName, tempCategory);
            
            KnownAppReference ref = new KnownAppReference();
            ref.setAppId(appKey);
            ref.setAppName(appName);
            ref.setCategory(tempSubcategory);
            ref.setPackagesJson(appNode.has("packages_json") ? appNode.get("packages_json").toString() : "[]");
            
            JsonNode filesNode = appNode.get("files_info_json");
            if (filesNode != null && filesNode.isArray()) {
                ref.setFileReferences(new java.util.ArrayList<>());
                for (JsonNode fileNode : filesNode) {
                    String path = fileNode.get("path").asText();
                    String type = fileNode.get("type").asText();
                    
                    if ("Unknown".equalsIgnoreCase(type) && originalTypes != null && originalTypes.containsKey(path)) {
                        type = originalTypes.get(path);
                    }
                    ref.getFileReferences().add(new AppFileReference(path, type, ref));
                }
            }
            return ref;
        }

        log.info("Persistiendo aplicación: {} ({})", appName, appKey);

        // 1. Manejar Categoría Principal
        CategoryApp category = categoryRepository.findByCategory(categoryName)
                .orElseGet(() -> categoryRepository.save(new CategoryApp(categoryName, null)));

        // 2. Manejar Subcategoría
        CategoryApp subcategory = categoryRepository.findByCategory(subcategoryName)
                .orElseGet(() -> categoryRepository.save(new CategoryApp(subcategoryName, category)));

        // 3. Crear/Actualizar Referencia de Aplicación
        KnownAppReference ref = knownAppRepository.findById(appKey)
                .orElseGet(() -> {
                    KnownAppReference newRef = new KnownAppReference();
                    newRef.setAppId(appKey);
                    return newRef;
                });
        ref.setAppName(appName);
        ref.setCategory(subcategory);
        ref.setPackagesJson(appNode.get("packages_json").toString());

        ref = knownAppRepository.save(ref);

        // 4. Guardar archivos individuales para búsquedas futuras
        JsonNode filesNode = appNode.get("files_info_json");
        if (filesNode.isArray()) {
            if (ref.getFileReferences() == null) {
                ref.setFileReferences(new java.util.ArrayList<>());
            }
            for (JsonNode fileNode : filesNode) {
                String path = fileNode.get("path").asText();
                String type = fileNode.get("type").asText();

                // Si type es Unknown, intentamos obtener el tipo original del escaneo del cliente
                if ("Unknown".equalsIgnoreCase(type) && originalTypes != null && originalTypes.containsKey(path)) {
                    String correctedType = originalTypes.get(path);
                    log.info("Corrigiendo tipo de archivo para path '{}' de 'Unknown' a '{}' usando datos originales del cliente.", path, correctedType);
                    type = correctedType;
                }

                // Evitar duplicados exactos para la misma app
                if (appFileRepository.findByPathAndType(path, type).isEmpty()) {
                    // Limpiar cualquier referencia previa del mismo path con tipo "Unknown" para evitar duplicidad obsoleta
                    appFileRepository.findByPathAndType(path, "Unknown").ifPresent(unknownRef -> {
                        log.info("Eliminando referencia previa de tipo 'Unknown' obsoleta para el path: {}", path);
                        appFileRepository.delete(unknownRef);
                    });

                    AppFileReference savedFile = appFileRepository.save(new AppFileReference(path, type, ref));
                    ref.getFileReferences().add(savedFile);
                }
            }
        }
        return ref;
    }

    private String prepareJsonlFile(Task task) throws Exception {
        String rawData = task.getInputData();

        // Si el formato es {1={path=.ai, type=folder}, ...} lo convertimos a JSON
        // válido
        if (rawData != null && rawData.contains("=") && !rawData.contains("\":")) {
            log.info("Detectado formato no estándar en inputData, intentando normalizar...");
            rawData = rawData.replace("=", ":")
                    .replaceAll("([{,])\\s*([^:{},\\s]+)", "$1\"$2\"")
                    .replaceAll(":\\s*([^:{},\\s\"]+)", ":\"$1\"");
            log.debug("Data normalizada: {}", rawData);
        }

        JsonNode inputData = objectMapper.readTree(rawData);
        Path tempFile = Files.createTempFile("batch-" + task.getId(), ".jsonl");

        try (FileWriter writer = new FileWriter(tempFile.toFile())) {
            Iterator<Map.Entry<String, JsonNode>> fields = inputData.fields();
            while (fields.hasNext()) {
                Map.Entry<String, JsonNode> field = fields.next();
                String appKey = field.getKey();
                JsonNode appData = field.getValue();

                // Construir el objeto de petición como en batch.py
                ObjectNode requestNode = objectMapper.createObjectNode();
                requestNode.put("id", "req_" + appKey);

                ObjectNode reqInner = requestNode.putObject("request");

                // Contents
                ArrayNode contents = reqInner.putArray("contents");
                ObjectNode content = contents.addObject();
                content.put("role", "user");
                ArrayNode parts = content.putArray("parts");
                ObjectNode part = parts.addObject();

                // Wrap app key and data back into a string as user text
                ObjectNode appWrap = objectMapper.createObjectNode();
                appWrap.set(appKey, appData);
                part.put("text", objectMapper.writeValueAsString(appWrap));

                // systemInstruction
                ObjectNode sysInstr = reqInner.putObject("systemInstruction");
                ArrayNode sysParts = sysInstr.putArray("parts");
                sysParts.addObject().put("text", SYS_PROMPT);

                // generationConfig
                ObjectNode genConfig = reqInner.putObject("generationConfig");
                genConfig.put("responseMimeType", "application/json");

                // Añadimos thinking_config como en batch.py
                ObjectNode thinkingConfig = genConfig.putObject("thinking_config");
                thinkingConfig.put("include_thoughts", false);
                thinkingConfig.put("thinking_budget", 4000);

                // responseSchema (siguiendo el esquema del ejemplo)
                genConfig.set("responseSchema", createSchemaNode());

                // Mostrar la petición en consola para verificación
                log.info("Verificando petición Batch para la aplicación: {}", appKey);

                writer.write(objectMapper.writeValueAsString(requestNode) + "\n");
            }
        }
        log.info("Archivo JSONL preparado en: {}", tempFile.toAbsolutePath());
        return tempFile.toAbsolutePath().toString();
    }

    private JsonNode createSchemaNode() {
        ObjectNode schema = objectMapper.createObjectNode();
        schema.put("type", "OBJECT");

        ObjectNode properties = schema.putObject("properties");
        ObjectNode apps = properties.putObject("apps");
        apps.put("type", "ARRAY");

        ObjectNode items = apps.putObject("items");
        items.put("type", "OBJECT");

        ObjectNode itemProps = items.putObject("properties");
        itemProps.putObject("app_key").put("type", "STRING");
        itemProps.putObject("app_name").put("type", "STRING");
        itemProps.putObject("category").put("type", "STRING");
        itemProps.putObject("subcategory").put("type", "STRING");

        ObjectNode filesInfo = itemProps.putObject("files_info_json");
        filesInfo.put("type", "ARRAY");
        ObjectNode fileItems = filesInfo.putObject("items");
        fileItems.put("type", "OBJECT");
        ObjectNode fileProps = fileItems.putObject("properties");
        fileProps.putObject("path").put("type", "STRING");
        fileProps.putObject("type").put("type", "STRING");
        ArrayNode fileReq = fileItems.putArray("required");
        fileReq.add("path").add("type");

        ObjectNode packages = itemProps.putObject("packages_json");
        packages.put("type", "ARRAY");
        packages.putObject("items").put("type", "STRING");

        ArrayNode required = items.putArray("required");
        required.add("app_key").add("app_name").add("category").add("subcategory").add("files_info_json")
                .add("packages_json");

        ArrayNode rootRequired = schema.putArray("required");
        rootRequired.add("apps");

        return schema;
    }

    @Transactional
    public List<KnownAppReference> resolveUnknownEntriesSynchronously(Map<String, Object> unknownEntries) {
        log.info("Resolviendo de forma síncrona {} entradas desconocidas con Gemini...", unknownEntries.size());
        List<KnownAppReference> persistedApps = new java.util.ArrayList<>();
        
        try {
            String unknownEntriesJson = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(unknownEntries);
            geminiLogger.info("========================================= SYNCHRONOUS REQUEST =========================================");
            geminiLogger.info("Unknown Entries Input:\n{}", unknownEntriesJson);
            geminiLogger.info("System Prompt:\n{}", SYS_PROMPT);
            geminiLogger.info("Model: {}", syncModel);
            geminiLogger.info("--------------------------------------------------------------------------------------------------------");
        } catch (Exception ex) {
            geminiLogger.error("Failed to serialize request for geminiLogger", ex);
        }

        try {
            Client client = Client.builder().apiKey(apiKey).build();

            // 1. Preparar la entrada para el prompt (en formato JSON)
            String unknownEntriesJson = objectMapper.writeValueAsString(unknownEntries);

            // Extraemos los tipos originales en caso síncrono para el fallback
            Map<String, String> originalTypes = new java.util.HashMap<>();
            for (Map.Entry<String, Object> entry : unknownEntries.entrySet()) {
                if (entry.getValue() instanceof Map<?, ?> details) {
                    String path = (String) details.get("path");
                    String type = (String) details.get("type");
                    if (path != null && type != null && !"Unknown".equalsIgnoreCase(type)) {
                        originalTypes.put(path, type);
                    }
                }
            }

            // 2. Construir la configuración con las instrucciones de sistema y
            // responseMimeType
            GenerateContentConfig config = GenerateContentConfig.builder()
                    .systemInstruction(Content.fromParts(Part.fromText(SYS_PROMPT)))
                    .responseMimeType("application/json")
                    .build();

            log.info("Enviando petición síncrona a Gemini con modelo {}...", syncModel);
            GenerateContentResponse response = client.models.generateContent(
                    syncModel,
                    unknownEntriesJson,
                    config);

            String responseText = response.text();
            
            geminiLogger.info("Raw Response from Gemini:\n{}", sanitizeForLogging(responseText));
            geminiLogger.info("========================================================================================================\n");

            // 3. Procesar y persistir resultados
            if (responseText != null && !responseText.isEmpty()) {
                persistedApps = processRawResponseText(responseText, originalTypes);
                log.info("Persistidas {} aplicaciones obtenidas del modelo.", persistedApps.size());
            }
        } catch (Exception e) {
            log.error("Error resolviendo de forma síncrona con Gemini", e);
            geminiLogger.error("Error in Synchronous Request to Gemini:", e);
            geminiLogger.info("========================================================================================================\n");
        }
        return persistedApps;
    }

    private void handleError(Task task, String message, Exception e) {
        task.setStatus(TaskStatus.ERROR);
        taskRepository.save(task);
        log.error("{}: {}", message, e.getMessage());
    }

    private Map<String, String> extractOriginalTypes(String rawData) {
        Map<String, String> types = new java.util.HashMap<>();
        if (rawData == null || rawData.trim().isEmpty()) {
            return types;
        }
        try {
            String normalized = rawData;
            // Si el formato es {1={path=.ai, type=folder}, ...} lo convertimos a JSON válido
            if (normalized.contains("=") && !normalized.contains("\":")) {
                normalized = normalized.replace("=", ":")
                        .replaceAll("([{,])\\s*([^:{},\\s]+)", "$1\"$2\"")
                        .replaceAll(":\\s*([^:{},\\s\"]+)", ":\"$1\"");
            }
            JsonNode root = objectMapper.readTree(normalized);
            Iterator<Map.Entry<String, JsonNode>> fields = root.fields();
            while (fields.hasNext()) {
                Map.Entry<String, JsonNode> field = fields.next();
                JsonNode appData = field.getValue();
                if (appData != null) {
                    if (appData.has("path") && appData.has("type")) {
                        String path = appData.get("path").asText();
                        String type = appData.get("type").asText();
                        if (path != null && type != null && !"Unknown".equalsIgnoreCase(type)) {
                            types.put(path, type);
                        }
                    } else if (appData.isArray()) {
                        for (JsonNode item : appData) {
                            if (item.has("path") && item.has("type")) {
                                String path = item.get("path").asText();
                                String type = item.get("type").asText();
                                if (path != null && type != null && !"Unknown".equalsIgnoreCase(type)) {
                                    types.put(path, type);
                                }
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            log.warn("No se pudo extraer tipos originales de inputData: {}", e.getMessage());
        }
        return types;
    }

    private String sanitizeForLogging(String text) {
        if (text == null) return null;
        // Reemplazar el thoughtSignature extremadamente largo para que no ensucie gemini.log
        return text.replaceAll("\"thoughtSignature\"\\s*:\\s*\"[^\"]*\"", "\"thoughtSignature\":\"[STRIPPED]\"");
    }
}