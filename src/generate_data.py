"""Creates a small messy sales CSV (with bad rows on purpose) in data/."""
import csv
import random
from datetime import date, timedelta

random.seed(42)
products = {"Laptop": 55000, "Phone": 20000, "Headphones": 2500, "Keyboard": 1200, "Monitor": 9000}
cities = ["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Delhi"]

rows = []
for i in range(1, 501):
    p = random.choice(list(products))
    rows.append([
        i,
        (date(2026, 1, 1) + timedelta(days=random.randint(0, 270))).isoformat(),
        p,
        random.choice(cities),
        random.randint(1, 5),
        products[p],
    ])

# Dirty data on purpose
rows.append(rows[10][:])            # duplicate order
rows.append(rows[20][:])            # duplicate order
rows[30][4] = -2                    # negative quantity
rows[40][3] = ""                    # missing city
rows[50][5] = ""                    # missing price
rows[60][1] = "not-a-date"          # bad date

with open("data/sales_raw.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "order_date", "product", "city", "quantity", "unit_price"])
    w.writerows(rows)
print(f"Wrote {len(rows)} rows to data/sales_raw.csv")
