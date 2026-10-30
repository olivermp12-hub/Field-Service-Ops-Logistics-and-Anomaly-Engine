import duckdb

DB_PATH = "data/fieldops_warehouse.duckdb"


def run_operational_analysis():
    conn = duckdb.connect(DB_PATH)

    print("==================================================")
    print(" 🚨 FIELD SERVICE OPERATIONAL LEAKAGE REPORT 🚨")
    print("==================================================")

    # 1. Summary of Dispatch Statuses
    status_df = conn.execute("""
        SELECT 
            dispatch_status,
            COUNT(*) AS total_dispatches
        FROM marts.fct_dispatches
        GROUP BY dispatch_status;
    """).fetchdf()
    print("\n[1] Dispatch Status Breakdown:")
    print(status_df.to_string(index=False))

    # 2. Top Sites by Total Labor Hours & Cost Exposure
    cost_df = conn.execute("""
        SELECT 
            f.site_id,
            COUNT(f.dispatch_id) AS total_jobs,
            ROUND(SUM(f.job_duration_hours), 2) AS total_labor_hours,
            ROUND(SUM(f.job_duration_hours * t.hourly_rate), 2) AS total_labor_cost
        FROM marts.fct_dispatches AS f
        JOIN marts.dim_technicians AS t
            ON f.tech_id = t.tech_id
        WHERE f.dispatch_status = 'COMPLETED'
        GROUP BY f.site_id
        ORDER BY total_labor_cost DESC
        LIMIT 5;
    """).fetchdf()
    print("\n[2] Top 5 Job Sites by Labor Cost Exposure:")
    print(cost_df.to_string(index=False))

    conn.close()


if __name__ == "__main__":
    run_operational_analysis()