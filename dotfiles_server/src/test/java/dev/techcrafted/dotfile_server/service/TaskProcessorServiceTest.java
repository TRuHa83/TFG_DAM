package dev.techcrafted.dotfile_server.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.techcrafted.dotfile_server.model.AppFileReference;
import dev.techcrafted.dotfile_server.model.KnownAppReference;
import dev.techcrafted.dotfile_server.model.CategoryApp;
import dev.techcrafted.dotfile_server.repository.CategoryAppRepository;
import dev.techcrafted.dotfile_server.repository.AppFileReferenceRepository;
import dev.techcrafted.dotfile_server.repository.KnownAppReferenceRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@Transactional
public class TaskProcessorServiceTest {

    @Autowired
    private TaskProcessorService taskProcessorService;

    @Autowired
    private KnownAppReferenceRepository knownAppRepository;

    @Autowired
    private AppFileReferenceRepository appFileRepository;

    @Autowired
    private CategoryAppRepository categoryRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void testPersistAppNodeCorrectsUnknownFileTypeUsingOriginalTypes() throws Exception {
        // 1. Preparar un nodo JSON devuelto por Gemini que contenga 'Unknown' en el type
        String appNodeJson = """
            {
                "app_key": "test_app",
                "app_name": "Test Application",
                "category": "Development",
                "subcategory": "Editor",
                "packages_json": [],
                "files_info_json": [
                    {
                        "path": ".config/test_app",
                        "type": "Unknown"
                    },
                    {
                        "path": ".test_apprc",
                        "type": "file"
                    }
                ]
            }
            """;
        JsonNode appNode = objectMapper.readTree(appNodeJson);

        // 2. Preparar el mapa de tipos originales (lo que el cliente escaneó)
        Map<String, String> originalTypes = new HashMap<>();
        originalTypes.put(".config/test_app", "folder");
        originalTypes.put(".test_apprc", "file");

        // 3. Persistir usando el servicio
        KnownAppReference ref = taskProcessorService.persistAppNode(appNode, originalTypes);

        // 4. Validar que se haya corregido de "Unknown" a "folder"
        assertNotNull(ref);
        assertEquals("test_app", ref.getAppId());
        
        List<AppFileReference> fileRefs = appFileRepository.findAll().stream()
                .filter(f -> ref.getAppId().equals(f.getApp().getAppId()))
                .toList();
        assertEquals(2, fileRefs.size());

        AppFileReference folderRef = fileRefs.stream()
                .filter(f -> ".config/test_app".equals(f.getPath()))
                .findFirst()
                .orElse(null);
        
        assertNotNull(folderRef);
        assertEquals("folder", folderRef.getType()); // ¡Verificamos que se corrigió!

        AppFileReference fileRef = fileRefs.stream()
                .filter(f -> ".test_apprc".equals(f.getPath()))
                .findFirst()
                .orElse(null);
        
        assertNotNull(fileRef);
        assertEquals("file", fileRef.getType());
    }

    @Test
    public void testPersistAppNodeCleansUpPreviousUnknownType() throws Exception {
        // 1. Crear previamente en base de datos una entrada "Unknown" para el mismo path con categoría correcta
        CategoryApp cat = categoryRepository.findByCategory("Development")
                .orElseGet(() -> categoryRepository.save(new CategoryApp("Development", null)));
        CategoryApp subcat = categoryRepository.findByCategory("Editor")
                .orElseGet(() -> categoryRepository.save(new CategoryApp("Editor", cat)));

        KnownAppReference preApp = new KnownAppReference();
        preApp.setAppId("test_app");
        preApp.setAppName("Test Application");
        preApp.setPackagesJson("[]");
        preApp.setCategory(subcat);
        preApp = knownAppRepository.save(preApp);

        AppFileReference oldUnknownRef = new AppFileReference(".config/test_app", "Unknown", preApp);
        appFileRepository.save(oldUnknownRef);

        // Validamos que existe en la DB
        assertTrue(appFileRepository.findByPathAndType(".config/test_app", "Unknown").isPresent());

        // 2. Preparar un nodo JSON devuelto por Gemini ahora con tipo "folder" o "Unknown" (que se corregirá)
        String appNodeJson = """
            {
                "app_key": "test_app",
                "app_name": "Test Application",
                "category": "Development",
                "subcategory": "Editor",
                "packages_json": [],
                "files_info_json": [
                    {
                        "path": ".config/test_app",
                        "type": "folder"
                    }
                ]
            }
            """;
        JsonNode appNode = objectMapper.readTree(appNodeJson);

        // 3. Persistir usando el servicio
        taskProcessorService.persistAppNode(appNode, new HashMap<>());

        // 4. Validar que la antigua entrada "Unknown" fue eliminada y se reemplazó por "folder"
        assertTrue(appFileRepository.findByPathAndType(".config/test_app", "Unknown").isEmpty());
        assertTrue(appFileRepository.findByPathAndType(".config/test_app", "folder").isPresent());
    }
}
