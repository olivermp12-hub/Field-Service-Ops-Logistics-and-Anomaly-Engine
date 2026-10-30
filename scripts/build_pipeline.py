import os
import duckdb

os.makedirs("data/marts", exist_ok=True)
db_path = "data/marts/warehouse.duckdb"

print("Building DuckDB Medallion Pipeline & Star Schema...")
con = duckdb.connect(db_path)

# Bronze / Raw Layer
con.execute("""
    CREATE OR REPLACE TABLE raw_dispatches AS 
    SELECT * FROM read_parquet('data/raw/fct_dispatches.parquet');
""")

# Silver / Staging Layer
con.execute("""
    CREATE OR REPLACE TABLE stg_dispatches AS
    SELECT 
        dispatch_id,
        site_id,
        tech_id,
        ticket_created_at,
        arrival_at,
        completion_at,
        UPPER(dispatch_status) AS dispatch_status,
        ROUND(COALESCE(job_duration_hours, 0.0), 2) AS job_duration_hours,
        ROUND(COALESCE(total_labor_cost, 0.0), 2) AS total_labor_cost
    FROM raw_dispatches;
""")

# Gold / Marts (Star Schema)
con.execute("""
    CREATE OR REPLACE TABLE dim_sites AS
    SELECT DISTINCT site_id FROM stg_dispatches;

    CREATE OR REPLACE TABLE dim_technicians AS
    SELECT DISTINCT tech_id FROM stg_dispatches;

    CREATE OR REPLACE TABLE fct_dispatches AS
    SELECT * FROM stg_dispatches;
""")

# Export CSVs for Tableau Public
con.execute("COPY dim_sites TO 'data/marts/dim_sites.csv' (HEADER, DELIMITER ',');")
con.execute("COPY dim_technicians TO 'data/marts/dim_technicians.csv' (HEADER, DELIMITER ',');")
con.execute("COPY fct_dispatches TO 'data/marts/fct_dispatches.csv' (HEADER, DELIMITER ',');")

print("Medallion pipeline build complete. Exported CSV marts to data/marts/")
con.close()