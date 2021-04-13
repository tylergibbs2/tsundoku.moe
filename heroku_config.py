import os

WEBHOOK_URLS = {
    "general": os.getenv("WEBHOOK_GENERAL"),
    "feature": os.getenv("WEBHOOK_FEATURE"),
    "bug": os.getenv("WEBHOOK_BUG"),
}
PSQL_DSN = os.getenv("DATABASE_URL")
