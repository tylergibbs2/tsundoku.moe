from quart import current_app as app


METRICS = (
    "user_count",
    "show_count",
    "entry_count",
    "entries_manually_added_count",
    "entries_manually_deleted_count",
    "base_wh_count",
    "used_nyaa_count",
    "api_header_count",
    "popular_webhook_state",
    "popular_webhook_service"
)

async def ensure_client(client: str) -> None:
    async with app.db.acquire() as con:
        await con.execute("""
            INSERT INTO
                telemetry_client (
                    client_id
                )
            VALUES
                ($1)
            ON CONFLICT (client_id) DO NOTHING;
        """, client)

async def handle(client: str, data: dict) -> dict:
    if not data or any(key not in METRICS for key in data):
        return {}

    # At this point, there is at least one key and it is
    # also a valid key.

    cols = ",".join(data.keys())
    values = ", ".join(f"${n}" for n, _ in enumerate(data, start=2))

    query = f"""
        INSERT INTO
            telemetry_entry
            (client_id, {cols})
        VALUES
            ($1, {values})
    """

    await ensure_client(client)
    async with app.db.acquire() as con:
        await con.execute(query, client, *data.values())

    return data
