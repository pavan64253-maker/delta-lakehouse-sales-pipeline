# Sales Lakehouse Pipeline (Python + Delta Lake)

An ETL pipeline using the **medallion architecture** (Bronze → Silver → Gold) on **Delta Lake**, built in pure **Python** (pandas, delta-rs) with **SQL** (DuckDB). No Java or Spark install needed.

## Pipeline

| Layer | What it does |
|---|---|
| Bronze | Loads the raw CSV as-is and adds ingestion metadata |
| Silver | Casts types, removes duplicates, rejects bad rows into a separate table, runs data quality checks |
| Gold | Builds business aggregates with SQL (revenue by city, monthly product sales) |

The raw data contains deliberately bad rows (duplicates, negative quantity, missing city/price, invalid date) so the cleaning and validation steps are meaningful.

## Run locally

Requires Python 3.9+.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python src/generate_data.py
python src/run_pipeline.py      # bronze -> silver -> gold
python src/delta_demo.py        # Delta history + time travel (run the pipeline twice first)
```

Expected silver output: `bronze=502 clean=496 rejected=4 duplicates_removed=2`

## Tech
Python, pandas, Delta Lake (delta-rs), SQL (DuckDB), Git/GitHub

## Next steps
Port the same pipeline to PySpark on Databricks (Workflows/Jobs, Unity Catalog).
