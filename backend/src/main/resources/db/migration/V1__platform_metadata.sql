CREATE TABLE platform_metadata (
  metadata_key VARCHAR(64) PRIMARY KEY,
  metadata_value VARCHAR(255) NOT NULL
);
INSERT INTO platform_metadata(metadata_key, metadata_value) VALUES ('schema_baseline', 'phase-0');
