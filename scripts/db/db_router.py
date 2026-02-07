from scripts.db.sqlite_db import get_sqlite_connection
from scripts.db.postgres_db import get_pg_connection

def get_connection_by_variant(mode):
    if mode == "Variant B":
        return get_pg_connection(), "postgres"
    return get_sqlite_connection(), "sqlite"
