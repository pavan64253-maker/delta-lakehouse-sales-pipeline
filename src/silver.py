"""Silver: cleaned, typed, de-duplicated data + rejected rows + quality checks."""
import pandas as pd
from deltalake import DeltaTable, write_deltalake


def run():
    bronze = DeltaTable("lakehouse/bronze/sales").to_pandas()

    typed = bronze.copy()
    typed["order_id"] = pd.to_numeric(typed["order_id"], errors="coerce")
    typed["order_date"] = pd.to_datetime(typed["order_date"], format="%Y-%m-%d", errors="coerce")
    typed["quantity"] = pd.to_numeric(typed["quantity"], errors="coerce")
    typed["unit_price"] = pd.to_numeric(typed["unit_price"], errors="coerce")
    typed["city"] = typed["city"].str.strip().replace("", None)

    is_valid = (
        typed["order_id"].notna()
        & typed["order_date"].notna()
        & typed["city"].notna()
        & typed["unit_price"].notna()
        & (typed["quantity"] > 0)
    )

    rejected = typed[~is_valid].copy()
    valid = typed[is_valid]
    clean = valid.drop_duplicates(subset="order_id").copy()
    clean["order_id"] = clean["order_id"].astype("int64")
    clean["quantity"] = clean["quantity"].astype("int64")
    clean["total_amount"] = clean["quantity"] * clean["unit_price"]

    # Rejected rows keep raw text so we can inspect why they failed
    rejected = bronze.loc[rejected.index]

    write_deltalake("lakehouse/silver/sales", clean, mode="overwrite")
    write_deltalake("lakehouse/silver/sales_rejected", rejected, mode="overwrite")

    # Data quality checks
    n_dupes = len(valid) - len(clean)
    assert (clean["quantity"] > 0).all(), "non-positive quantity in silver"
    assert clean["order_id"].is_unique, "duplicate order_id in silver"
    assert clean["city"].notna().all(), "null city in silver"
    print(f"[silver] bronze={len(bronze)} clean={len(clean)} rejected={len(rejected)} duplicates_removed={n_dupes}")
    print("[silver] quality checks passed")


if __name__ == "__main__":
    run()
