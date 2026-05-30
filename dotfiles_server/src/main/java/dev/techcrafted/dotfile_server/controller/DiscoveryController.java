package dev.techcrafted.dotfile_server.controller;

import dev.techcrafted.dotfile_server.model.KnownAppReference;
import dev.techcrafted.dotfile_server.model.Task;
import dev.techcrafted.dotfile_server.model.TaskStatus;
import dev.techcrafted.dotfile_server.dto.AppDetailDTO;
import dev.techcrafted.dotfile_server.dto.DiscoveryRequest;
import dev.techcrafted.dotfile_server.dto.DiscoveryResponse;
import dev.techcrafted.dotfile_server.model.AppFileReference;
import dev.techcrafted.dotfile_server.repository.AppFileReferenceRepository;
import dev.techcrafted.dotfile_server.repository.TaskRepository;
import dev.techcrafted.dotfile_server.service.TaskProcessorService;

import lombok.extern.slf4j.Slf4j;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;

import java.security.SecureRandom;
import java.util.*;
import java.util.stream.Collectors;


@RestController
@Slf4j
public class DiscoveryController {

    private static final String CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    private final SecureRandom random = new SecureRandom();

    @Autowired
    private TaskRepository taskRepository;

    @Autowired
    private AppFileReferenceRepository appFileRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private TaskProcessorService taskProcessorService;

    @PostMapping("/discovery")
    public DiscoveryResponse discoveryApps(@RequestBody(required = false) DiscoveryRequest request) {
        String taskID = generateTaskID();
        Task task;
        Map<String, Object> incomingData = (request != null) ? request.getData() : null;

        if (incomingData != null) {
            try {
                log.debug("JSON recibido de cliente en /discovery: {}", objectMapper.writeValueAsString(request));
            } catch (Exception e) {
                log.error("Error serializando petición discovery para logging", e);
            }
            log.info("Recibida petición /discovery con {} entradas.", incomingData.size());

            // 1. Filtrar entradas y recoger apps ya conocidas
            Set<KnownAppReference> uniqueApps = new HashSet<>();
            Map<String, Object> unknownEntries = new HashMap<>();

            for (Map.Entry<String, Object> entry : incomingData.entrySet()) {
                if (entry.getValue() instanceof Map<?, ?> details) {
                    String path = (String) details.get("path");
                    String type = (String) details.get("type");

                    if (path != null && type != null) {
                        Optional<AppFileReference> fileRef = appFileRepository.findByPathAndType(path, type);
                        if (fileRef.isPresent()) {
                            uniqueApps.add(fileRef.get().getApp());
                            log.debug("Entrada conocida: {} -> {}", path, fileRef.get().getApp().getAppName());
                        } else {
                            unknownEntries.put(entry.getKey(), entry.getValue());
                        }
                    } else {
                        unknownEntries.put(entry.getKey(), entry.getValue());
                    }
                }
            }

            String incomingDataJson = null;
            try {
                incomingDataJson = objectMapper.writeValueAsString(incomingData);
            } catch (Exception e) {
                log.error("Error serializando incomingData", e);
                incomingDataJson = incomingData.toString();
            }

            if (!unknownEntries.isEmpty()) {
                log.info("Entradas desconocidas encontradas: {}. Iniciando flujo por lotes (Batch)...", unknownEntries.size());
                try {
                    String unknownEntriesJson = objectMapper.writeValueAsString(unknownEntries);
                    task = new Task(taskID, TaskStatus.QUEUE, unknownEntriesJson, null, null);
                } catch (Exception e) {
                    log.error("Error serializando unknownEntries", e);
                    task = new Task(taskID, TaskStatus.ERROR, incomingDataJson, null, null);
                }
            } else {
                log.info("Todas las entradas son conocidas. Marcando tarea como COMPLETE.");
                task = new Task(taskID, TaskStatus.COMPLETE, incomingDataJson, null, null);
            }
            taskRepository.save(task);

        } else {
            log.warn("Recibida petición /discovery sin payload válido.");
            task = new Task(taskID, TaskStatus.ERROR, "No payload", null, null);
            taskRepository.save(task);
        }

        // 2. Paso de Recuperación Final: Recorremos los paths originales y volvemos a consultar en la DB
        // Esto garantiza que respondamos al cliente con todo lo que sí esté en la DB (indistintamente de si la llamada falló o no)
        Set<KnownAppReference> identifiedApps = new HashSet<>();
        if (incomingData != null) {
            for (Map.Entry<String, Object> entry : incomingData.entrySet()) {
                if (entry.getValue() instanceof Map<?, ?> details) {
                    String path = (String) details.get("path");
                    String type = (String) details.get("type");

                    if (path != null && type != null) {
                        Optional<AppFileReference> fileRef = appFileRepository.findByPathAndType(path, type);
                        fileRef.ifPresent(appFileReference -> identifiedApps.add(appFileReference.getApp()));
                    }
                }
            }
        }

        // 3. Mapear apps identificadas y guardar el resultDataJson en la tarea para coherencia histórica si está en estado COMPLETE
        Map<String, AppDetailDTO> appsMap = identifiedApps.stream()
                .collect(Collectors.toMap(
                        KnownAppReference::getAppId,
                        app -> AppDetailDTO.fromKnownAppReference(app, objectMapper),
                        (existing, replacement) -> existing
                ));

        if (task.getStatus() == TaskStatus.COMPLETE && incomingData != null) {
            try {
                String resultDataJson = objectMapper.writeValueAsString(appsMap);
                task.setResultData(resultDataJson);
                taskRepository.save(task);
            } catch (Exception e) {
                log.error("Error guardando resultData en task", e);
            }
        }

        return new DiscoveryResponse(taskID, task.getStatus().name(), appsMap);
    }

    private String generateTaskID() {
        String randomPart = random.ints(12, 0, CHARACTERS.length())
                .mapToObj(CHARACTERS::charAt)
                .map(Object::toString)
                .collect(Collectors.joining());
        return "TASK-" + randomPart;
    }
}
