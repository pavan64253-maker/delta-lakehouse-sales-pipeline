"""Bronze: raw data as-is (all columns as text), plus ingestion metadata."""
import pandas as pd
from deltalake import write_deltalake


def run():
    df = pd.read_csv("data/sales_raw.csv", dtype=str, keep_default_na=False)
    df["_ingested_at"] = pd.Timestamp.now()
    df["_source_file"] = "sales_raw.csv"
    write_deltalake("lakehouse/bronze/sales", df, mode="overwrite")
    print(f"[bronze] rows written: {len(df)}")


if __name__ == "__main__":
    run()
