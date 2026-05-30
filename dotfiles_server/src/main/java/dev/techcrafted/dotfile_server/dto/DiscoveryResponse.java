package dev.techcrafted.dotfile_server.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.Map;


@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class DiscoveryResponse {
    
    @JsonProperty("taskID")
    private String taskID;
    
    private String status;
    
    private Map<String, AppDetailDTO> data;
}
