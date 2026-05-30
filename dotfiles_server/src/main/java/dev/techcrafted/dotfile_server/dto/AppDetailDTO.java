package dev.techcrafted.dotfile_server.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import dev.techcrafted.dotfile_server.model.KnownAppReference;
import dev.techcrafted.dotfile_server.model.AppFileReference;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AppDetailDTO {
    @JsonProperty("app_name")
    private String appName;
    
    private String category;
    
    private String subcategory;
    
    @JsonProperty("files_info_json")
    private Object filesInfo;
    
    @JsonProperty("packages_json")
    private Object packages;

    @JsonProperty("ignored")
    private Boolean ignored;

    public static AppDetailDTO fromKnownAppReference(KnownAppReference app, ObjectMapper objectMapper) {
        String category = "";
        String subcategory = "";

        if (app.getCategory() != null) {
            if (app.getCategory().getParent() != null) {
                category = app.getCategory().getParent().getCategory();
                subcategory = app.getCategory().getCategory();
            } else {
                category = app.getCategory().getCategory();
            }
        }

        ArrayNode filesInfoNode = objectMapper.createArrayNode();
        if (app.getFileReferences() != null) {
            for (AppFileReference fileRef : app.getFileReferences()) {
                ObjectNode fileNode = objectMapper.createObjectNode();
                fileNode.put("path", fileRef.getPath());
                fileNode.put("type", fileRef.getType());
                filesInfoNode.add(fileNode);
            }
        }
        Object filesInfo = filesInfoNode;

        Object packages = null;
        if (app.getPackagesJson() != null && !app.getPackagesJson().isEmpty()) {
            try {
                packages = objectMapper.readTree(app.getPackagesJson());
            } catch (Exception e) {
                // fallback
            }
        }

        boolean isIgnored = (app.getAppName() != null && "Unknown".equalsIgnoreCase(app.getAppName())) 
                || "Unknown".equalsIgnoreCase(category);

        return AppDetailDTO.builder()
                .appName(app.getAppName())
                .category(category)
                .subcategory(subcategory)
                .filesInfo(filesInfo)
                .packages(packages)
                .ignored(isIgnored)
                .build();
    }
}
