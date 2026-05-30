package dev.techcrafted.dotfile_server.repository;

import dev.techcrafted.dotfile_server.model.KnownAppReference;
import org.springframework.data.jpa.repository.JpaRepository;

public interface KnownAppReferenceRepository extends JpaRepository<KnownAppReference, String> {
}
