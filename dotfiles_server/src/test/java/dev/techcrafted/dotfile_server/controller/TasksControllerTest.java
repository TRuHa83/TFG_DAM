package dev.techcrafted.dotfile_server.controller;

import dev.techcrafted.dotfile_server.model.Task;
import dev.techcrafted.dotfile_server.model.TaskStatus;
import dev.techcrafted.dotfile_server.repository.TaskRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Optional;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TasksController.class)
class TasksControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TaskRepository taskRepository;

    @Test
    void getTaskStatus_shouldReturnTask_WhenTaskExists() throws Exception {
        String taskID = "TASK-123456789012";
        Task task = new Task(taskID, TaskStatus.QUEUE, null, null, null);

        when(taskRepository.findById(taskID)).thenReturn(Optional.of(task));

        mockMvc.perform(get("/task/" + taskID)
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(taskID))
                .andExpect(jsonPath("$.status").value("QUEUE"));
    }

    @Test
    void getTaskStatus_shouldReturnNotFound_WhenTaskDoesNotExist() throws Exception {
        String taskID = "NON-EXISTENT";

        when(taskRepository.findById(taskID)).thenReturn(Optional.empty());

        mockMvc.perform(get("/task/" + taskID)
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());
    }
}
