"""Delta Lake features: table history and time travel. Run the pipeline at least twice first."""
from deltalake import DeltaTable

path = "lakehouse/silver/sales"
dt = DeltaTable(path)

print("== History (each pipeline run = one version) ==")
for h in dt.history():
    print(h.get("version"), h.get("operation"), h.get("timestamp"))

print("== Time travel: row count at version 0 ==")
print(len(DeltaTable(path, version=0).to_pandas()))
