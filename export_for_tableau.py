import os
import duckdb

DB_PATH = "data/fieldops_warehouse.duckdb"
EXPORT_DIR = "data/tableau_exports"


def export_marts_to_csv():
    conn = duckdb.connect(DB_PATH)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    # Export dimension and fact tables to CSV for Tableau Public
    tables = ["dim_technicians", "dim_sites", "fct_dispatches"]

    for table in tables:
        file_path = os.path.join(EXPORT_DIR, f"{table}.csv")
        conn.execute(f"COPY marts.{table} TO '{file_path}' (HEADER, FORMAT CSV);")
        print(f"Exported marts.{table} -> {file_path}")

    conn.close()
    print("\n All marts successfully exported to CSV for Tableau!")


if __name__ == "__main__":
    export_marts_to_csv()