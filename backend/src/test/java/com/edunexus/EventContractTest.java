package com.edunexus;

import static org.assertj.core.api.Assertions.assertThat;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class EventContractTest {
    @Test
    void sharedFixturesRejectUnknownVersion() throws Exception {
        var root = Path.of("../contracts/events");
        var mapper = new ObjectMapper();
        var schema =
                JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V202012)
                        .getSchema(
                                mapper.readTree(
                                        root.resolve("envelope.schema.json").toFile()));

        assertThat(schema.validate(mapper.readTree(root.resolve("valid.json").toFile())))
                .isEmpty();
        assertThat(schema.validate(mapper.readTree(root.resolve("invalid-version.json").toFile())))
                .isNotEmpty();
    }
}
