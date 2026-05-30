package dev.techcrafted.dotfile_server.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import dev.techcrafted.dotfile_server.dto.TaskStatusResponse;
import dev.techcrafted.dotfile_server.repository.TaskRepository;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;


@RestController
@Slf4j
public class TasksController {

    @Autowired
    private TaskRepository taskRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @GetMapping("/task/{id}")
    public ResponseEntity<TaskStatusResponse> getTaskStatus(@PathVariable("id") String id) {
        return taskRepository.findById(id)
                .map(task -> {
                    Object data = null;
                    if (task.getResultData() != null) {
                        try {
                            data = objectMapper.readValue(task.getResultData(), Object.class);
                        } catch (Exception e) {
                            log.error("Error deserializando resultData para tarea {}", id, e);
                        }
                    }
                    TaskStatusResponse response = new TaskStatusResponse(
                            task.getId(),
                            task.getStatus().name(),
                            task.getBatchId(),
                            data
                    );
                    try {
                        String responseJson = objectMapper.writeValueAsString(response);
                        if (task.getStatus() == dev.techcrafted.dotfile_server.model.TaskStatus.COMPLETE || 
                            task.getStatus() == dev.techcrafted.dotfile_server.model.TaskStatus.ERROR) {
                            log.info("Enviando respuesta final a cliente para tarea {} (Estado: {}): {}", id, task.getStatus(), responseJson);
                        } else {
                            log.debug("Enviando respuesta de polling a cliente para tarea {} (Estado: {}): {}", id, task.getStatus(), responseJson);
                        }
                    } catch (Exception e) {
                        log.error("Error serializando respuesta para logging de tarea {}", id, e);
                    }
                    return ResponseEntity.ok(response);
                })
                .orElse(ResponseEntity.notFound().build());
    }
}
