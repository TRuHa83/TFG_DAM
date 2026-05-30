package dev.techcrafted.dotfile_server.repository;

import dev.techcrafted.dotfile_server.model.CategoryApp;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface CategoryAppRepository extends JpaRepository<CategoryApp, Integer> {
    Optional<CategoryApp> findByCategory(String category);
}
