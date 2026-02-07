import psycopg2

PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "documents",
    "user": "app",
    "password": "app"
}

def get_pg_connection():
    return psycopg2.connect(**PG_CONFIG)
