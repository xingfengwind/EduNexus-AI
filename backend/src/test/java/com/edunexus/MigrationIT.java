package com.edunexus;

import static org.assertj.core.api.Assertions.assertThat;

import org.flywaydb.core.Flyway;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.MySQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@Testcontainers
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class MigrationIT {
    @Container static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.4.8");

    @DynamicPropertySource
    static void database(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }

    @Autowired Flyway flyway;
    @Autowired JdbcTemplate jdbc;
    @Autowired TestRestTemplate client;

    @Test
    void migrationPersistsMetadataAndDoesNotRunTwice() {
        assertThat(
                        jdbc.queryForObject(
                                "SELECT metadata_value FROM platform_metadata "
                                        + "WHERE metadata_key='schema_baseline'",
                                String.class))
                .isEqualTo("phase-0");
        assertThat(flyway.migrate().migrationsExecuted).isZero();
        assertThat(flyway.validateWithResult().validationSuccessful).isTrue();
    }

    @Test
    void applicationServesHealthAndDeniesBusinessAccess() {
        assertThat(client.getForEntity("/api/v1/health", String.class).getStatusCode().value())
                .isEqualTo(200);
        assertThat(client.getForEntity("/api/v1/private", String.class).getStatusCode().value())
                .isEqualTo(401);
    }
}
