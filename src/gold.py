"""Gold: business-ready aggregates built with SQL (DuckDB)."""
import duckdb
from deltalake import DeltaTable, write_deltalake


def run():
    silver_sales = DeltaTable("lakehouse/silver/sales").to_pandas()  # noqa: F841 (used by SQL below)

    revenue_by_city = duckdb.sql("""
        SELECT city,
               COUNT(*)          AS orders,
               SUM(total_amount) AS revenue
        FROM silver_sales
        GROUP BY city
        ORDER BY revenue DESC
    """).df()

    monthly_by_product = duckdb.sql("""
        SELECT strftime(order_date, '%Y-%m') AS month,
               product,
               CAST(SUM(quantity) AS BIGINT) AS units_sold,
               SUM(total_amount) AS revenue
        FROM silver_sales
        GROUP BY month, product
        ORDER BY month, revenue DESC
    """).df()

    write_deltalake("lakehouse/gold/revenue_by_city", revenue_by_city, mode="overwrite")
    write_deltalake("lakehouse/gold/monthly_product_sales", monthly_by_product, mode="overwrite")

    print("[gold] revenue by city:")
    print(revenue_by_city.to_string(index=False))
    print("[gold] sample monthly product sales:")
    print(monthly_by_product.head(5).to_string(index=False))


if __name__ == "__main__":
    run()
