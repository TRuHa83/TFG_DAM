package dev.techcrafted.dotfile_server.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.List;


@Entity
@Table(name = "categories_apps")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CategoryApp {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_cat")
    private Integer id;

    @Column(nullable = false, unique = true)
    private String category;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "parent_id")
    @com.fasterxml.jackson.annotation.JsonIgnore
    @lombok.EqualsAndHashCode.Exclude
    private CategoryApp parent;

    @OneToMany(mappedBy = "parent")
    @com.fasterxml.jackson.annotation.JsonIgnore
    @lombok.EqualsAndHashCode.Exclude
    private List<CategoryApp> subcategories;

    public CategoryApp(String category, CategoryApp parent) {
        this.category = category;
        this.parent = parent;
    }
}
