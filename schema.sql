CREATE FUNCTION now_utc() RETURNS TIMESTAMP AS $$
  SELECT NOW() AT TIME ZONE 'utc';
$$ LANGUAGE SQL;

CREATE TABLE telemetry_client (
    client_id uuid PRIMARY KEY,
    first_seen TIMESTAMP NOT NULL DEFAULT now_utc()
);

CREATE TABLE telemetry_entry (
    client_id uuid REFERENCES telemetry_client(client_id),
    received_at TIMESTAMP NOT NULL DEFAULT now_utc(),
    user_count INT,
    show_count INT,
    entry_count INT,
    entries_manually_added_count INT,
    entries_manually_deleted_count INT,
    base_wh_count INT,
    used_nyaa_count INT,
    api_header_count INT,
    popular_webhook_state TEXT,
    popular_webhook_service TEXT
);

CREATE INDEX telemetry_entry_time ON telemetry_entry(received_at);