package dev.techcrafted.dotfile_server.service;

import dev.techcrafted.dotfile_server.controller.DiscoveryController;
import dev.techcrafted.dotfile_server.dto.DiscoveryRequest;
import dev.techcrafted.dotfile_server.dto.DiscoveryResponse;
import dev.techcrafted.dotfile_server.model.AppFileReference;
import dev.techcrafted.dotfile_server.model.KnownAppReference;
import dev.techcrafted.dotfile_server.model.Task;
import dev.techcrafted.dotfile_server.model.TaskStatus;
import dev.techcrafted.dotfile_server.repository.AppFileReferenceRepository;
import dev.techcrafted.dotfile_server.repository.TaskRepository;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@SpringBootTest
public class SynchronousDiscoveryTest {

    @Autowired
    private DiscoveryController discoveryController;

    @MockitoBean
    private TaskProcessorService taskProcessorService;

    @MockitoBean
    private AppFileReferenceRepository appFileRepository;

    @MockitoBean
    private TaskRepository taskRepository;

    @Test
    public void testDiscoveryFlowWithUnknownEntriesEnqueuesTask() {
        // Preparar datos de prueba
        DiscoveryRequest request = new DiscoveryRequest();
        Map<String, Object> requestData = new HashMap<>();
        
        Map<String, String> app1Details = new HashMap<>();
        app1Details.put("path", ".config/nvim");
        app1Details.put("type", "folder");
        requestData.put("1", app1Details);
        
        request.setData(requestData);

        // Simulamos que en la DB no está registrada la app (desconocida)
        when(appFileRepository.findByPathAndType(".config/nvim", "folder")).thenReturn(Optional.empty());

        // Ejecutar controlador
        DiscoveryResponse response = discoveryController.discoveryApps(request);

        // Validar que NO se llamó al antiguo método síncrono
        verify(taskProcessorService, never()).resolveUnknownEntriesSynchronously(any());

        // Capturar y validar que se guardó la tarea con estado QUEUE
        ArgumentCaptor<Task> taskCaptor = ArgumentCaptor.forClass(Task.class);
        verify(taskRepository, atLeastOnce()).save(taskCaptor.capture());
        
        Task savedTask = taskCaptor.getValue();
        assertNotNull(savedTask);
        assertEquals(TaskStatus.QUEUE, savedTask.getStatus());
        assertTrue(savedTask.getInputData().contains(".config/nvim"));

        // Validar respuesta
        assertNotNull(response);
        assertEquals(TaskStatus.QUEUE.name(), response.getStatus());
        assertTrue(response.getData().isEmpty());
    }

    @Test
    public void testDiscoveryFlowWithOnlyKnownEntriesCompletesImmediately() {
        // Preparar datos de prueba
        DiscoveryRequest request = new DiscoveryRequest();
        Map<String, Object> requestData = new HashMap<>();
        
        Map<String, String> app1Details = new HashMap<>();
        app1Details.put("path", ".config/nvim");
        app1Details.put("type", "folder");
        requestData.put("1", app1Details);
        
        request.setData(requestData);

        // Simulamos que en la DB SÍ está registrada la app (conocida)
        KnownAppReference mockApp = new KnownAppReference();
        mockApp.setAppId("nvim");
        mockApp.setAppName("NeoVim");
        AppFileReference fileRef = new AppFileReference(".config/nvim", "folder", mockApp);
        when(appFileRepository.findByPathAndType(".config/nvim", "folder")).thenReturn(Optional.of(fileRef));

        // Ejecutar controlador
        DiscoveryResponse response = discoveryController.discoveryApps(request);

        // Capturar y validar que se guardó la tarea con estado COMPLETE
        ArgumentCaptor<Task> taskCaptor = ArgumentCaptor.forClass(Task.class);
        verify(taskRepository, atLeastOnce()).save(taskCaptor.capture());
        
        Task savedTask = taskCaptor.getValue();
        assertNotNull(savedTask);
        assertEquals(TaskStatus.COMPLETE, savedTask.getStatus());

        // Validar respuesta
        assertNotNull(response);
        assertEquals(TaskStatus.COMPLETE.name(), response.getStatus());
        assertTrue(response.getData().containsKey("nvim"));
        assertEquals("NeoVim", response.getData().get("nvim").getAppName());
    }
}
