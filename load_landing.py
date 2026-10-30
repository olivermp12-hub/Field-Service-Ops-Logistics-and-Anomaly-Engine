import os
import duckdb

DB_PATH = "data/fieldops_warehouse.duckdb"
PARQUET_PATH = "data/landing/dispatches/dispatches_raw.parquet"


def load_raw_to_duckdb():
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    # Connect to DuckDB (creates the file if it doesn't exist)
    conn = duckdb.connect(DB_PATH)

    # Create the raw schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    # Ingest Parquet directly into a raw table using DuckDB's native reader
    conn.execute(f"""
        CREATE OR REPLACE TABLE raw.raw_dispatches AS 
        SELECT * FROM read_parquet('{PARQUET_PATH}');
    """)

    # Verify the row count
    result = conn.execute("SELECT COUNT(*) FROM raw.raw_dispatches;").fetchone()
    print(f"Successfully loaded {result[0]} rows into raw.raw_dispatches inside DuckDB.")

    conn.close()


if __name__ == "__main__":
    load_raw_to_duckdb()