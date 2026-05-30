package dev.techcrafted.dotfile_server.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import dev.techcrafted.dotfile_server.dto.DiscoveryRequest;
import dev.techcrafted.dotfile_server.model.AppFileReference;
import dev.techcrafted.dotfile_server.model.CategoryApp;
import dev.techcrafted.dotfile_server.model.KnownAppReference;
import dev.techcrafted.dotfile_server.model.Task;
import dev.techcrafted.dotfile_server.repository.AppFileReferenceRepository;
import dev.techcrafted.dotfile_server.repository.TaskRepository;
import dev.techcrafted.dotfile_server.service.TaskProcessorService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(DiscoveryController.class)
class DiscoveryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TaskRepository taskRepository;

    @MockBean
    private AppFileReferenceRepository appFileRepository;

    @MockBean
    private TaskProcessorService taskProcessorService;

    @Autowired
    private ObjectMapper objectMapper;

    private KnownAppReference knownApp;
    private CategoryApp category;

    @BeforeEach
    void setUp() {
        category = new CategoryApp();
        category.setId(1);
        category.setCategory("Tools");

        knownApp = new KnownAppReference();
        knownApp.setAppId("test-app");
        knownApp.setAppName("Test App");
        knownApp.setCategory(category);
    }

    @Test
    void discoveryApps_shouldReturnJsonWithRandomTaskID() throws Exception {
        String payload = "{\"data\": {\"os\": \"linux\", \"arch\": \"x64\"}}";

        mockMvc.perform(post("/discovery")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.taskID").value(startsWith("TASK-")));
    }

    @Test
    void discoveryApps_withKnownApp_shouldReturnIdentifiedApps() throws Exception {
        Map<String, Object> data = new HashMap<>();
        Map<String, String> details = new HashMap<>();
        details.put("path", "/etc/test");
        details.put("type", "config");
        data.put("entry1", details);

        DiscoveryRequest request = new DiscoveryRequest();
        request.setData(data);

        AppFileReference fileRef = new AppFileReference("/etc/test", "config", knownApp);
        when(appFileRepository.findByPathAndType("/etc/test", "config")).thenReturn(Optional.of(fileRef));

        mockMvc.perform(post("/discovery")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.taskID").value(startsWith("TASK-")))
                .andExpect(jsonPath("$.data", hasKey("test-app")))
                .andExpect(jsonPath("$.data['test-app'].app_name").value("Test App"));
    }

    @Test
    void discoveryApps_withUnknownApp_shouldInitiateBatchProcess() throws Exception {
        Map<String, Object> data = new HashMap<>();
        Map<String, String> details = new HashMap<>();
        details.put("path", "/etc/unknown");
        details.put("type", "config");
        data.put("entry1", details);

        DiscoveryRequest request = new DiscoveryRequest();
        request.setData(data);

        when(appFileRepository.findByPathAndType(any(), any())).thenReturn(Optional.empty());

        mockMvc.perform(post("/discovery")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.taskID").value(startsWith("TASK-")))
                .andExpect(jsonPath("$.status").value("QUEUE"))
                .andExpect(jsonPath("$.data", anEmptyMap()));
    }

    @Test
    void discoveryApps_withEmptyPayload_shouldReturnErrorTask() throws Exception {
        mockMvc.perform(post("/discovery")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.taskID").value(startsWith("TASK-")))
                .andExpect(jsonPath("$.data", anEmptyMap()));
    }

    @Test
    void discoveryApps_withCircularCategory_shouldSerializeSuccessfully() throws Exception {
        // Simular circularidad (aunque ya pusimos @JsonIgnore, esto comprueba que funciona)
        category.setParent(category); 
        
        Map<String, Object> data = new HashMap<>();
        Map<String, String> details = new HashMap<>();
        details.put("path", "/etc/test");
        details.put("type", "config");
        data.put("entry1", details);

        DiscoveryRequest request = new DiscoveryRequest();
        request.setData(data);

        AppFileReference fileRef = new AppFileReference("/etc/test", "config", knownApp);
        when(appFileRepository.findByPathAndType("/etc/test", "config")).thenReturn(Optional.of(fileRef));

        mockMvc.perform(post("/discovery")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data['test-app'].category").value("Tools"));
    }
}
