package dev.techcrafted.dotfile_server.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "app_file_references", indexes = {
    @Index(name = "idx_path_type", columnList = "file_path, file_type")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AppFileReference {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "file_path", nullable = false)
    private String path;

    @Column(name = "file_type", nullable = false)
    private String type;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "app_id", nullable = false)
    private KnownAppReference app;

    public AppFileReference(String path, String type, KnownAppReference app) {
        this.path = path;
        this.type = type;
        this.app = app;
    }
}
