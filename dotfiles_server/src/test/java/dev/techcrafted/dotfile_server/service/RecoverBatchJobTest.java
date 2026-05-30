package dev.techcrafted.dotfile_server.service;

import com.google.genai.Client;
import com.google.genai.types.BatchJob;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.beans.factory.annotation.Value;

@SpringBootTest
public class RecoverBatchJobTest {

    @Autowired
    private TaskProcessorService taskProcessorService;

    @Value("${spring.ai.google.genai.api-key}")
    private String apiKey;

    @Test
    public void recoverSpecificJob() throws Exception {
        // ID completo proporcionado por el usuario
        String fullResourceName = "batches/hiq14n97n2vgwqbvsn217yshxbronpd3ozyv";

        Client client = Client.builder()
                .apiKey(apiKey)
                .build();

        System.out.println("Intentando recuperar Job con nombre completo: " + fullResourceName);
        
        try {
            BatchJob batchJob = client.batches.get(fullResourceName, null);
            String state = batchJob.state().get().toString();
            System.out.println("Estado del Job encontrado: " + state);

            if ("JOB_STATE_SUCCEEDED".equals(state)) {
                taskProcessorService.processAndPersistResults(batchJob, new java.util.HashMap<>());
                System.out.println("✅ Procesamiento completado y datos persistidos en las nuevas tablas.");
            } else {
                System.out.println("⚠️ El Job no ha finalizado con éxito (Estado: " + state + "). No se puede procesar aún.");
            }
        } catch (Exception e) {
            System.err.println("❌ Error al recuperar el Job: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
