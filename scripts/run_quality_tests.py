import duckdb

def run_tests():
    print("Running Data Quality Assertion Tests...")
    con = duckdb.connect("data/marts/warehouse.duckdb")
    
    # Assertion 1: Zero Null Keys
    null_keys = con.execute("SELECT COUNT(*) FROM fct_dispatches WHERE dispatch_id IS NULL OR site_id IS NULL OR tech_id IS NULL;").fetchone()[0]
    assert null_keys == 0, f"Data Quality Failure: Found {null_keys} null keys in fct_dispatches!"
    
    # Assertion 2: Referential Integrity Check
    orphan_sites = con.execute("SELECT COUNT(*) FROM fct_dispatches f LEFT JOIN dim_sites s ON f.site_id = s.site_id WHERE s.site_id IS NULL;").fetchone()[0]
    assert orphan_sites == 0, f"Data Quality Failure: Found {orphan_sites} foreign key breaks!"

    # Assertion 3: Status Consistency Check
    unclosed_with_cost = con.execute("SELECT COUNT(*) FROM fct_dispatches WHERE dispatch_status = 'UNCLOSED' AND total_labor_cost > 0;").fetchone()[0]
    assert unclosed_with_cost == 0, f"Data Quality Failure: Found {unclosed_with_cost} unclosed tickets with labor cost attached!"

    print("✅ ALL DATA QUALITY ASSERTION TESTS PASSED (0 Key Breaks, 0 Financial Drift).")
    con.close()

if __name__ == "__main__":
    run_tests()