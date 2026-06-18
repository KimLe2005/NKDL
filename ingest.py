import os
import duckdb
import subprocess
import glob

def main():
    print("1. Download dataset...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", "shashwatwork/dataco-smart-supply-chain-for-big-data-analysis",
        "--unzip"
    ], check=True)

    print("2. Find CSV...")
    csv_files = glob.glob("DataCoSupplyChainDataset.csv")
    if not csv_files:
        csv_files = [f for f in glob.glob("*.csv") if "Description" not in f]
    if not csv_files:
        raise FileNotFoundError("Could not find the DataCoSupplyChainDataset.csv file.")
    csv_file = csv_files[0]
    print("Found:", csv_file)

    print("3. Connect MotherDuck...")
    md_token = os.environ.get('MOTHERDUCK_TOKEN')
    if not md_token:
        raise ValueError("MOTHERDUCK_TOKEN environment variable is not set. Please set it before running the script.")

    con = duckdb.connect(f"md:my_db?motherduck_token={md_token}")

    print("4. Create table...")
    con.sql(f"""
        CREATE OR REPLACE TABLE bronze_supplychain_raw AS 
        SELECT * FROM read_csv_auto('{csv_file}', ignore_errors=true)
    """)

    print("DONE")

if __name__ == "__main__":
    main()
