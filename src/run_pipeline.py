"""Runs bronze -> silver -> gold in order."""
import bronze
import silver
import gold

if __name__ == "__main__":
    bronze.run()
    silver.run()
    gold.run()
    print("Pipeline finished.")
