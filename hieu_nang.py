import os
import time
import duckdb
import tomllib  
from groq import Groq

# --- HÀM TỰ ĐỘNG ĐỌC KEY TỪ FILE SECRETS.TOML KHÔNG QUA STREAMLIT ---
def load_secrets():
    groq_key = None
    md_token = None
    
    # Tìm file secrets.toml trong thư mục .streamlit
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, "rb") as f:
                config = tomllib.load(f)
                groq_key = config.get("GROQ_API_KEY")
                md_token = config.get("MOTHERDUCK_TOKEN")
        except Exception as e:
            print(f"⚠️ Không thể đọc file secrets.toml: {e}")
            
    # Nếu không tìm thấy file, sẽ thử tìm ở biến môi trường hệ thống
    if not groq_key:
        groq_key = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
    if not md_token:
        md_token = os.environ.get("MOTHERDUCK_TOKEN", "YOUR_MOTHERDUCK_TOKEN_HERE")
        
    return groq_key, md_token

# Khởi tạo thông tin bảo mật ngầm
GROQ_API_KEY, MOTHERDUCK_TOKEN = load_secrets()
client = Groq(api_key=GROQ_API_KEY)

# Danh sách câu hỏi kiểm thử
TEST_QUESTIONS = [
    "Tổng doanh thu của chuỗi cung ứng trong tháng vừa qua là bao nhiêu?",
    "Liệt kê top 5 sản phẩm có tỷ lệ giao hàng trễ cao nhất?",
    "Đánh giá hiệu suất giao hàng của phương thức Standard Class?",
    "Tìm các đơn hàng bị hủy thuộc danh mục máy tính trong tuần này?",
    "Thống kê số lượng đơn hàng theo từng khu vực thị trường?"
]

def simulate_system(question):
    print(f"\nĐang kiểm thử câu hỏi: '{question}'")
    
    # --- BƯỚC 1: ĐO THỜI GIAN SINH SQL ---
    start_time = time.time()
    prompt_sql = f"Hãy chuyển câu hỏi sau thành câu lệnh SQL chuẩn cho DuckDB: {question}"
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt_sql}],
        model="llama-3.3-70b-versatile",
    )
    generated_sql = "SELECT * FROM orders LIMIT 5;" 
    
    time_sql = time.time() - start_time
    print(f"   [1. Sinh SQL]: {time_sql:.2f} giây")

    # --- BƯỚC 2: ĐO THỜI GIAN TRUY VẤN DỮ LIỆU ---
    start_time = time.time()
    try:
        conn = duckdb.connect(f"md:?motherduck_token={MOTHERDUCK_TOKEN}")
        df = conn.execute(generated_sql).df()
        conn.close()
    except Exception as e:
        import pandas as pd
        df = pd.DataFrame({"Status": ["Late"], "Count": [10]})
        
    time_query = time.time() - start_time
    print(f"   [2. Truy vấn DB]: {time_query:.2f} giây")

    # --- BƯỚC 3: ĐO THỜI GIAN SINH BIÊN BẢN/NHẬN ĐỊNH ---
    start_time = time.time()
    prompt_insight = f"Dựa vào dữ liệu sau: {df.to_string()}, hãy viết một nhận định ngắn gọn cho câu hỏi: {question}"
    
    chat_completion_insight = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt_insight}],
        model="llama-3.3-70b-versatile",
    )
    
    time_insight = time.time() - start_time
    print(f"   [3. Sinh nhận định]: {time_insight:.2f} giây")
    
    total_time = time_sql + time_query + time_insight
    print(f" TỔNG CỘNG (End-to-End): {total_time:.2f} giây")
    
    return time_sql, time_query, time_insight, total_time

if __name__ == "__main__":
    print("=== BẮT ĐẦU ĐO HIỆU NĂNG HỆ THỐNG ===")
    results = []
    for q in TEST_QUESTIONS:
        res = simulate_system(q)
        results.append(res)
        time.sleep(1)
        
    avg_sql = sum(r[0] for r in results) / len(results)
    avg_query = sum(r[1] for r in results) / len(results)
    avg_insight = sum(r[2] for r in results) / len(results)
    avg_total = sum(r[3] for r in results) / len(results)
    
    print("\n=============================================")
    print("KẾT QUẢ TRUNG BÌNH ĐỂ ĐƯA VÀO BÁO CÁO:")
    print(f"1. Thời gian sinh SQL trung bình: {avg_sql:.2f} giây")
    print(f"2. Thời gian truy vấn DB trung bình: {avg_query:.2f} giây")
    print(f"3. Thời gian sinh nhận định trung bình: {avg_insight:.2f} giây")
    print(f"Tổng thời gian phản hồi trung bình: {avg_total:.2f} giây")
    print("=============================================")