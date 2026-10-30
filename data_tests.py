import duckdb

DB_PATH = "data/fieldops_warehouse.duckdb"


def run_data_quality_checks():
    conn = duckdb.connect(DB_PATH)

    print("==================================================")
    print(" 🔍 RUNNING DATA QUALITY & INTEGRITY TESTS 🔍")
    print("==================================================")

    tests_passed = True

    # Test 1: Check for duplicate dispatch_ids in raw data
    dup_count = conn.execute("""
        SELECT COUNT(*) FROM (
            SELECT dispatch_id, COUNT(*) as cnt
            FROM raw.raw_dispatches
            GROUP BY dispatch_id
            HAVING cnt > 1
        );
    ​""").fetchone()[0]

    if dup_count > 0:
        print(f"   [FAIL] Test 1: Found {dup_count} duplicate dispatch IDs!")
        tests_passed = False
    else:
        print("   [PASS] Test 1: Primary Key Uniqueness (dispatch_id is unique).")

    # Test 2: Check for negative or null hourly rates
    invalid_rates = conn.execute("""
        SELECT COUNT(*) 
        FROM raw.raw_dispatches 
        WHERE hourly_rate IS NULL OR hourly_rate <= 0;
    """).fetchone()[0]

    if invalid_rates > 0:
        print(f"   [FAIL] Test 2: Found {invalid_rates} records with invalid/null hourly rates!")
        tests_passed = False
    else:
        print("   [PASS] Test 2: Hourly Rate Integrity (no negative or null rates).")

    conn.close()

    if not tests_passed:
        raise ValueError("Data Quality Validation FAILED. Pipeline aborted.")
    else:
        print("\n All data quality assertions passed successfully! Pipeline is healthy.")


if __name__ == "__main__":
    run_data_quality_checks()