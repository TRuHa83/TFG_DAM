package dev.techcrafted.dotfile_server.repository;

import dev.techcrafted.dotfile_server.model.AppFileReference;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface AppFileReferenceRepository extends JpaRepository<AppFileReference, Long> {
    Optional<AppFileReference> findByPathAndType(String path, String type);
}
