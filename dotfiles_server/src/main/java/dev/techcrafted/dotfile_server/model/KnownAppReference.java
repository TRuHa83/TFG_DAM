package dev.techcrafted.dotfile_server.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;


@Entity
@Table(name = "known_apps_reference")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class KnownAppReference {

    @Id
    @Column(name = "app_id")
    private String appId;

    @Column(name = "app_name", nullable = false)
    private String appName;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "category_id", nullable = false)
    private CategoryApp category;

    @OneToMany(mappedBy = "app", fetch = FetchType.EAGER)
    private List<AppFileReference> fileReferences;

    @Lob
    @Column(name = "packages_json")
    private String packagesJson;
}
