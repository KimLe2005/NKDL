NKDL - Dự án Data Pipeline
Dự án này thực hiện việc làm sạch và chuẩn hóa dữ liệu từ tầng Bronze sang tầng Silver bằng dbt.

Cách thiết lập cho thành viên trong nhóm:
Clone dự án về máy:

Bash
git clone https://github.com/KimLe2005/NKDL.git
Cài đặt dbt:

Bash
pip install dbt-duckdb
Cấu hình kết nối:

Vào thư mục transform/.

Tạo file profiles.yml (dựa trên mẫu đã thống nhất).

Điền MotherDuck Token cá nhân của bạn vào file profiles.yml.

Chạy Pipeline:

Bash
dbt run --profiles-dir .
Cấu trúc dự án:
transform/: Chứa toàn bộ code dbt để chuyển đổi dữ liệu.

ingest.py: Script dùng để nạp dữ liệu thô.
