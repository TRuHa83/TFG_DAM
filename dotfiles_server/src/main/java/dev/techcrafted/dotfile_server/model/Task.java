package dev.techcrafted.dotfile_server.model;

import jakarta.persistence.*;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;


@Entity
@Table(name = "tasks")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Task {

    @Id
    private String id;

    @Enumerated(EnumType.STRING)
    private TaskStatus status;

    @Lob
    private String inputData;

    @Lob
    private String resultData;

    private String batchId;

    private LocalDateTime createdAt;

    // Constructor para creación inicial
    public Task(String id, TaskStatus status, String inputData, String resultData, String batchId) {
        this.id = id;
        this.status = status;
        this.inputData = inputData;
        this.resultData = resultData;
        this.batchId = batchId;
    }

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
