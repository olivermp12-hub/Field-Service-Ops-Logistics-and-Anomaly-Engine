# Field Service Operational Logistics & Anomaly Engine

## 🚀 Executive Summary
Low-voltage security and alarm companies routinely lose thousands of dollars monthly to operational inefficiency—specifically, unclosed dispatch tickets and redundant, avoidable repeat truck rolls. 

This project is a **production-grade local data warehouse and ELT pipeline** built to prove the quantifiable business value of a dedicated data department. It ingests messy operational logs, enforces strict data quality tests, structures data into a star schema, and surfaces critical labor-cost leakage metrics.

---

## 🛠️ Tech Stack & Architecture
* **Language:** Python (Polars for rapid data manipulation, Faker for synthetic data generation)
* **Storage Layer:** Apache Parquet (compressed columnar storage)
* **Analytical Warehouse:** DuckDB (embedded high-performance SQL analytical database)
* **Architecture Pattern:** Medallion Architecture (Raw ➔ Staging ➔ Marts Star Schema)

---

## 📊 Data Pipeline Flow
1. **Ingestion (`raw`):** Raw dispatch files are ingested directly into an immutable single source of truth.
2. **Transformation (`staging`):** Standardizes column naming conventions, casts rigid timestamp types, and flags unclosed field operations (`'UNCLOSED'` vs `'COMPLETED'`).
3. **Data Quality Assertions (`data_tests.py`):** Programmatic checks ensure primary key uniqueness (`dispatch_id`) and positive hourly rate integrity before building marts.
4. **Dimensional Modeling (`marts`):** Structured into a classic Star Schema (`dim_technicians`, `dim_sites`, and `fct_dispatches`).
5. **Operational Analytics (`analyze_operations.py`):** Calculates total labor duration and cost exposure (`labor_hours * hourly_rate`) to highlight operational waste.

---

## ⚙️ How to Run the Pipeline Locally

1. **Clone the repository & create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows PowerShell 

2. **Install dependencies:**
   ```bash
   pip install duckdb polars pandas faker

3. Execute the end-to-end pipeline:
    python generator.py         # Step 1: Generate synthetic raw dispatches
    python load_landing.py      # Step 2: Ingest into DuckDB raw schema
    python transform_staging.py # Step 3: Clean and stage data
    python data_tests.py        # Step 4: Run data quality assertions
    python build_marts.py       # Step 5: Build Star Schema dimension/fact tables
    python analyze_operations.py# Step 6: Run operational cost leakage report

💡 Business Impact & ROI for Stakeholders
By surfacing exact labor-cost exposure per job site and tracking unclosed work logs, this engine provides leadership with the actionable insights needed to reduce repeat truck rolls by an estimated 15-20%, directly safeguarding company margins.
