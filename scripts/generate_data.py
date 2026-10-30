import os
import random
from datetime import datetime, timedelta
import polars as pl
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

os.makedirs("data/raw", exist_ok=True)

print("Generating synthetic field service dispatch dataset...")

# Generate Dimensions
sites = [f"SITE-{i:04d}" for i in range(1, 51)]
techs = [f"TECH-{i:03d}" for i in range(1, 16)]

# Generate Fact Dispatches
n_records = 500
records = []
base_time = datetime(2024, 1, 1, 8, 0, 0)

for i in range(1, n_records + 1):
    dispatch_id = f"DSP-{i:05d}"
    site_id = random.choice(sites)
    tech_id = random.choice(techs)
    
    created_at = base_time + timedelta(hours=random.randint(1, 720))
    arrival_at = created_at + timedelta(minutes=random.randint(15, 120))
    
    # Simulate unclosed dispatches (~5% anomaly rate)
    is_completed = random.random() > 0.05
    status = "COMPLETED" if is_completed else "UNCLOSED"
    
    completion_at = arrival_at + timedelta(hours=random.uniform(1.0, 12.0)) if is_completed else None
    duration_hours = (completion_at - arrival_at).total_seconds() / 3600.0 if completion_at else None
    
    # Labor rate simulation ($45 - $85/hr)
    hourly_rate = random.choice([45.0, 55.0, 65.0, 75.0, 85.0])
    total_cost = round(duration_hours * hourly_rate, 2) if duration_hours else None
    
    records.append({
        "dispatch_id": dispatch_id,
        "site_id": site_id,
        "tech_id": tech_id,
        "ticket_created_at": created_at,
        "arrival_at": arrival_at,
        "completion_at": completion_at,
        "dispatch_status": status,
        "job_duration_hours": duration_hours,
        "total_labor_cost": total_cost
    })

df = pl.DataFrame(records)
df.write_parquet("data/raw/fct_dispatches.parquet")

print(f"Successfully generated {n_records} raw records -> data/raw/fct_dispatches.parquet")