package dev.techcrafted.dotfile_server.repository;

import dev.techcrafted.dotfile_server.model.Task;
import dev.techcrafted.dotfile_server.model.TaskStatus;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;


@Repository
public interface TaskRepository extends JpaRepository<Task, String> {
    Optional<Task> findFirstByStatusOrderByCreatedAtAsc(TaskStatus status);
    List<Task> findAllByStatusAndBatchIdIsNotNull(TaskStatus status);
}
