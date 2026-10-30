import os
import random
from datetime import datetime, timedelta
from faker import Faker
import polars as pl

fake = Faker()
Faker.seed(42)
random.seed(42)

# Directory Setup
OUTPUT_DIR = "data/landing/dispatches"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_synthetic_dispatches(num_records=500):
    technicians = [f"TECH-{i:03d}" for i in range(1, 15)]
    sites = [f"SITE-{i:04d}" for i in range(1, 50)]
    hourly_rates = {tech: random.choice([45.0, 55.0, 65.0, 75.0]) for tech in technicians}

    records = []
    base_date = datetime(2026, 10, 1)

    for i in range(num_records):
        dispatch_id = f"DSP-{10000 + i}"
        site_id = random.choice(sites)
        tech_id = random.choice(technicians)
        rate = hourly_rates[tech_id]

        # Simulate job timing
        ticket_created = base_date + timedelta(
            days=random.randint(0, 14),
            hours=random.randint(6, 18),
            minutes=random.randint(0, 59),
        )

        # Travel time between 15 mins to 2 hours
        arrival = ticket_created + timedelta(minutes=random.randint(15, 120))

        # Edge Case 1: 5% of tickets are missing completion timestamps (Unclosed tickets / human error)
        if random.random() < 0.05:
            completion = None
        else:
            # Job duration between 30 mins and 6 hours
            completion = arrival + timedelta(minutes=random.randint(30, 360))

        records.append(
            {
                "dispatch_id": dispatch_id,
                "site_id": site_id,
                "tech_id": tech_id,
                "hourly_rate": rate,
                "ticket_created_at": ticket_created,
                "arrival_at": arrival,
                "completion_at": completion,
            }
        )

    # Edge Case 2: Inject duplicate records (5 intentional duplicates)
    for _ in range(5):
        records.append(random.choice(records).copy())

    # Convert to Polars DataFrame & write to Parquet
    df = pl.DataFrame(records)

    file_path = os.path.join(OUTPUT_DIR, "dispatches_raw.parquet")
    df.write_parquet(file_path)
    print(
        f" Successfully generated {len(records)} records (including duplicates/nulls) at {file_path}"
    )


if __name__ == "__main__":
    generate_synthetic_dispatches()