package dev.techcrafted.dotfile_server.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor
public class TaskStatusResponse {
    private String id;
    private String status;
    private String batchId;
    private Object data;
}
