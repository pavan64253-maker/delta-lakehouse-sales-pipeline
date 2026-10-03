# Quick reference notes

## Medallion layers
- Bronze = raw, untouched, add metadata (_ingested_at, _source_file)
- Silver = cleaned, typed, deduplicated; bad rows go to a rejected table
- Gold = aggregates ready for reports/dashboards

## Key pandas / SQL patterns used
- Read CSV as text: pd.read_csv(path, dtype=str, keep_default_na=False)
- Cast: pd.to_numeric(col, errors="coerce");  dates: pd.to_datetime(col, format="%Y-%m-%d", errors="coerce")
- Dedupe: df.drop_duplicates(subset="order_id")
- Split good/bad: df[is_valid] and df[~is_valid]
- Write Delta: write_deltalake(path, df, mode="overwrite")
- Read Delta: DeltaTable(path).to_pandas()
- SQL on a DataFrame: duckdb.sql("SELECT ... FROM df").df()

## Delta Lake
- Every write creates a new table version
- History: DeltaTable(path).history()
- Time travel: DeltaTable(path, version=0).to_pandas()

## Interview one-liners
- Why Delta over Parquet? ACID transactions, versioning/time travel, schema enforcement.
- Why medallion? Separates raw from clean from business-ready data, so you can reprocess any layer.
- Data quality: assertions in silver (no nulls, no duplicates, valid ranges); rejected rows kept for review.
