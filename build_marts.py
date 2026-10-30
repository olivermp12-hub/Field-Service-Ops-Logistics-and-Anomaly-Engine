import duckdb

DB_PATH = "data/fieldops_warehouse.duckdb"


def build_dimensional_marts():
    conn = duckdb.connect(DB_PATH)

    # Create the marts schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS marts;")

    # 1. Build dim_technicians (Unique technician dimension with hourly rates)
    conn.execute("""
        CREATE OR REPLACE TABLE marts.dim_technicians AS 
        SELECT DISTINCT 
            tech_id,
            hourly_rate
        FROM staging.stg_dispatches;
    """)

    # 2. Build dim_sites (Unique site dimension)
    conn.execute("""
        CREATE OR REPLACE TABLE marts.dim_sites AS 
        SELECT DISTINCT 
            site_id
        FROM staging.stg_dispatches;
    """)

    # 3. Build fct_dispatches (The core fact table linking back to dimensions)
    conn.execute("""
        CREATE OR REPLACE TABLE marts.fct_dispatches AS 
        SELECT 
            dispatch_id,
            site_id,
            tech_id,
            ticket_created_at,
            arrival_at,
            completion_at,
            dispatch_status,
            -- Calculate duration in hours where completion exists
            CASE 
                WHEN completion_at IS NOT NULL THEN ROUND(EXTRACT(EPOCH FROM (completion_at - arrival_at)) / 3600.0, 2)
                ELSE NULL
            END AS job_duration_hours
        FROM staging.stg_dispatches;
    """)

    # Verify our tables
    print(" Dimensional Marts Built Successfully!")
    tables = conn.execute("SHOW TABLES FROM marts;").fetchall()
    for t in tables:
        print(f"   - marts.{t[0]}")

    conn.close()


if __name__ == "__main__":
    build_dimensional_marts()