import os
import duckdb
import subprocess
import glob

def main():
    print("1. Download Kaggle dataset...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", "shashwatwork/dataco-smart-supply-chain-for-big-data-analysis",
        "--unzip"
    ], check=True)

    print("2. Tìm file CSV...")
    csv_file = glob.glob("*.csv")[0]
    print("Found:", csv_file)

    print("3. Connect MotherDuck...")
    md_token = os.environ.get('MOTHERDUCK_TOKEN')
    con = duckdb.connect(f'md:?motherduck_token={md_token}')

    print("4. Create Bronze table...")
    con.sql(f"""
        CREATE OR REPLACE TABLE bronze_supplychain_raw AS 
        SELECT * FROM read_csv_auto('{csv_file}', ignore_errors=true)
    """)

    print("✅ DONE")

if __name__ == "__main__":
    main()
