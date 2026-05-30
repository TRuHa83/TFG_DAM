package dev.techcrafted.dotfile_server.dto;

import lombok.Getter;
import lombok.Setter;

import java.util.Map;


@Setter
@Getter
public class DiscoveryRequest {
    private Map<String, Object> data;

    /*
    Puedes añadir campos específicos aquí más adelante, por ejemplo:
    private String os;
    private String arch;
    */
}
