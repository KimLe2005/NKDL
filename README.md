# Supply Chain Lakehouse AI

Ứng dụng web phân tích và giám sát chuỗi cung ứng, kết hợp Data Lakehouse, dashboard Streamlit, MotherDuck, dbt và Machine Learning để hỗ trợ phát hiện rủi ro giao hàng trễ.

## Demo

Ứng dụng đã deploy tại:

https://supplychain-lakehouse-ai.streamlit.app

## Mục tiêu dự án

Dự án mô phỏng một hệ thống hỗ trợ quản lý logistics, giúp người dùng:

- Theo dõi doanh thu, lợi nhuận, đơn hàng và trạng thái giao hàng.
- Phát hiện nhóm đơn hàng có nguy cơ giao trễ.
- Phân tích rủi ro theo khu vực, sản phẩm và phương thức vận chuyển.
- Dự báo khả năng giao trễ bằng mô hình Machine Learning.
- Hỏi dữ liệu bằng tiếng Việt và nhận kết quả phân tích trực tiếp trên dashboard.

## Kiến trúc hệ thống

```text
Kaggle Dataset
    -> ingest.py
    -> MotherDuck / DuckDB
    -> dbt Transform
    -> Machine Learning Notebook
    -> Streamlit Dashboard
```

Các tầng dữ liệu chính:

- Bronze: dữ liệu thô từ file CSV được nạp vào MotherDuck.
- Silver/Gold: dữ liệu được làm sạch, chuẩn hóa và dùng cho phân tích.
- ML: bảng dự báo rủi ro giao hàng trễ và bảng giải thích mô hình.

## Chức năng chính

- Dashboard KPI tổng quan về vận hành chuỗi cung ứng.
- Bộ lọc theo thời gian, khu vực, phương thức vận chuyển và danh mục sản phẩm.
- Phân tích đơn hàng rủi ro, doanh thu bị ảnh hưởng và tình trạng giao hàng.
- Mô phỏng phương án điều phối, ví dụ nâng cấp phương thức vận chuyển.
- Tích hợp Groq API để hỏi dữ liệu bằng ngôn ngữ tự nhiên.
- Tự sinh SQL, hiển thị bảng kết quả, biểu đồ và nhận định vận hành.

## Machine Learning

Notebook `NKDL____ML.ipynb` dùng dữ liệu Gold từ MotherDuck để huấn luyện mô hình dự báo giao hàng trễ. Kết quả được ghi lại vào MotherDuck để ứng dụng Streamlit sử dụng cho:

- Xác suất một đơn hàng có thể giao trễ.
- Danh sách đơn hàng rủi ro cao.
- Giải thích các yếu tố ảnh hưởng đến dự báo bằng SHAP/feature importance.

## Công nghệ sử dụng

- Python
- Streamlit
- DuckDB / MotherDuck
- dbt
- pandas, numpy
- Plotly
- Groq API
- scikit-learn, CatBoost, SHAP
- Kaggle API

## Cấu trúc thư mục

```text
.
├── app.py                    # Ứng dụng Streamlit
├── ingest.py                 # Nạp dữ liệu từ Kaggle vào MotherDuck
├── NKDL____ML.ipynb          # Notebook Machine Learning
├── EDA_Bronze                # Phân tích dữ liệu tầng Bronze
├── EDA_GOLD.ipynb            # Phân tích dữ liệu tầng Gold
├── check_md.py               # Kiểm tra kết nối/truy vấn MotherDuck
├── requirements.txt          # Thư viện cần cài đặt
└── transform/                # Project dbt
    ├── dbt_project.yml
    ├── profiles.yml
    └── models/
        ├── sources.yml
        ├── schema.yml
        └── stg_supplychain.sql
```

## Cách chạy local

Cài thư viện:

```bash
pip install -r requirements.txt
pip install dbt-duckdb
```

Cấu hình biến môi trường:

```bash
MOTHERDUCK_TOKEN=your_motherduck_token
GROQ_API_KEY=your_groq_api_key
```

Chạy ứng dụng:

```bash
streamlit run app.py
```

## Chạy pipeline dữ liệu

Nạp dữ liệu thô:

```bash
python ingest.py
```

Chạy dbt transform:

```bash
cd transform
dbt run --profiles-dir .
dbt test --profiles-dir .
```

## Ghi chú

Dữ liệu trong dự án lấy từ Kaggle và được dùng cho mục đích học tập, mô phỏng bài toán phân tích chuỗi cung ứng. Một số chức năng cần token MotherDuck và Groq API để chạy đầy đủ.
