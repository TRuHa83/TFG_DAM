package dev.techcrafted.dotfile_server;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.scheduling.annotation.EnableScheduling;


@SpringBootApplication
@EnableScheduling
public class DotfileServerApplication {

    public static void main(String[] args) { SpringApplication.run(DotfileServerApplication.class, args); }

}
