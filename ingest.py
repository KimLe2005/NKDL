import os
import duckdb
import subprocess

def main():
    print("1. Đang tải và giải nén dữ liệu từ Kaggle...")
    # Tải dataset trực tiếp bằng Kaggle CLI với Token mới
    subprocess.run(["kaggle", "datasets", "download", "-d", "shashwatwork/dataco-smart-supply-chain-for-big-data-analysis", "--unzip"], check=True)

    print("2. Đang kết nối với MotherDuck...")
    md_token = os.environ.get('MOTHERDUCK_TOKEN')
    con = duckdb.connect(f'md:?motherduck_token={md_token}')

    print("3. Nạp dữ liệu vào tầng Bronze...")
    # Đọc chính xác file CSV dữ liệu và nạp vào bảng dữ liệu thô
    con.sql("""
        CREATE OR REPLACE TABLE bronze_supplychain_raw AS 
        SELECT * FROM read_csv_auto('DataCoSupplyChainDataset.csv', ignore_errors=true)
    """)

    print("✅ Hoàn tất nạp dữ liệu thô vào hệ thống Lakehouse!")

if __name__ == "__main__":
    main()
