import duckdb

DB_PATH = "data/fieldops_warehouse.duckdb"


def transform_raw_to_staging():
    conn = duckdb.connect(DB_PATH)

    # Create the staging schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS staging;")

    # Create a clean staging table from raw data
    conn.execute("""
        CREATE OR REPLACE TABLE staging.stg_dispatches AS 
        SELECT 
            dispatch_id,
            site_id,
            tech_id,
            hourly_rate,
            CAST(ticket_created_at AS TIMESTAMP) AS ticket_created_at,
            CAST(arrival_at AS TIMESTAMP) AS arrival_at,
            -- Handle NULL completion times by flagging unclosed tickets or keeping NULL
            CAST(completion_at AS TIMESTAMP) AS completion_at,
            CASE 
                WHEN completion_at IS NULL THEN 'UNCLOSED'
                ELSE 'COMPLETED'
            END AS dispatch_status
        FROM raw.raw_dispatches;
    """)

    # Verify transformation
    result = conn.execute(
        "SELECT dispatch_status, COUNT(*) FROM staging.stg_dispatches GROUP BY dispatch_status;"
    ).fetchall()
    print(" Staging transform complete. Row counts by status:")
    for row in result:
        print(f"   - {row[0]}: {row[1]} rows")

    conn.close()


if __name__ == "__main__":
    transform_raw_to_staging()