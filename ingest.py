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
    csv_file = glob.glob("*.csv")[0]
    print("Found:", csv_file)

    print("3. Connect MotherDuck...")
    md_token = os.environ.get('MOTHERDUCK_TOKEN')

    con = duckdb.connect()
    con.sql("INSTALL motherduck; LOAD motherduck;")
    con.sql(f"ATTACH 'md:' AS my_db (TOKEN '{md_token}');")
    con.sql("USE my_db;")

    print("4. Create table...")
    con.sql(f"""
        CREATE OR REPLACE TABLE my_db.bronze_supplychain_raw AS 
        SELECT * FROM read_csv_auto('{csv_file}', ignore_errors=true)
    """)

    print("DONE")

if __name__ == "__main__":
    main()
