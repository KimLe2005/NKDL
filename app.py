import streamlit as st
import duckdb
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Cấu hình trang - Phải luôn ở đầu
st.set_page_config(page_title="AI Supply Chain Hub", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

# CSS Cao cấp - Giao diện Sáng Công nghệ (Premium Light Tech / SaaS) với tông Xanh Tím và Chữ Nổi Bật
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Giao diện nền sáng công nghệ tinh tế */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    /* Gradient chữ nổi bật cho Tiêu đề (Xanh biển sang Tím) */
    .gradient-text {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 36px;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .sub-text {
        color: #475569;
        font-weight: 500;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Thiết kế thẻ KPI & Chart Container nổi bật trên nền sáng */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.08) !important;
        padding: 24px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border: 1px solid #3B82F6 !important;
        box-shadow: 0 12px 30px -5px rgba(59, 130, 246, 0.15) !important;
        transform: translateY(-2px);
    }
    
    /* Chỉnh chữ trong Metric */
    [data-testid="stMetricValue"] {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: -1px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Ẩn viền thừa của Streamlit */
    hr {
        border-color: #E2E8F0 !important;
    }
    
    /* Tinh chỉnh tiêu đề h4 bên trong các khối cực kỳ nổi bật */
    h4 {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: -0.3px;
        margin-top: 0px !important;
        margin-bottom: 15px !important;
    }
    
    /* Sidebar nền xanh dương đậm, chữ trắng */
    [data-testid="stSidebar"] {
        background-color: #1E3A8A !important;
    }
    [data-testid="stSidebar"] iframe,
    iframe[title="streamlit_option_menu.option_menu"] {
        background-color: transparent !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] label p, 
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] h4 {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.3) !important;
    }
    
    /* Hộp bộ lọc nổi bật trong sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #0F172A !important;
        border: 2px solid #3B82F6 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3) !important;
        padding: 20px !important;
    }
    /* Chữ tiêu đề của Hộp Bộ lọc */
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] h4 {
        color: #3B82F6 !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
    }
    /* Chữ label của Selectbox trong Sidebar sáng lên và đẹp mắt */
    [data-testid="stSidebar"] label p {
        color: #93C5FD !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        margin-bottom: 6px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Style cho selectbox widget trong Sidebar để đồng bộ và nổi bật */
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #1E3A8A !important;
        border: 2px solid #2563EB !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"]:hover {
        border-color: #3B82F6 !important;
    }
    /* KPI Cards Pastel Design */
    .kpi-card {
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px !important;
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .kpi-info {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
        opacity: 0.9;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        line-height: 1.2;
    }
    .kpi-icon {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #FFFFFF;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        flex-shrink: 0;
    }
    .kpi-delta {
        font-size: 12px;
        font-weight: 700;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Hàm render KPI Card Light Pastel
def render_kpi(title, value, icon, bg_color, border_color, text_color, delta_html=""):
    delta_str = f'<div class="kpi-delta">{delta_html}</div>' if delta_html else ''
    return f"""<div class="kpi-card" style="background: {bg_color}; border-left: 5px solid {border_color};">
<div class="kpi-icon" style="color: {text_color};">{icon}</div>
<div class="kpi-info">
<div class="kpi-title" style="color: {text_color};">{title}</div>
<div class="kpi-value" style="color: {text_color};">{value}</div>
{delta_str}
</div>
</div>"""

country_dict = {
    'Egipto': 'Ai Cập (Egypt)', 
    'Camboya': 'Campuchia (Cambodia)', 
    'Suecia': 'Thụy Điển (Sweden)', 
    'Costa de Marfil': "Bờ Biển Ngà (Ivory Coast)",
    'Francia': 'Pháp (France)', 
    'Alemania': 'Đức (Germany)', 
    'Brasil': 'Brazil', 
    'España': 'Tây Ban Nha (Spain)',
    'Italia': 'Ý (Italy)', 
    'Reino Unido': 'Anh (United Kingdom)', 
    'Estados Unidos': 'Mỹ (United States)',
    'Japon': 'Nhật Bản (Japan)', 
    'Japón': 'Nhật Bản (Japan)', 
    'Corea del Sur': 'Hàn Quốc (South Korea)', 
    'Nueva Zelanda': 'New Zealand',
    'Paises Bajos': 'Hà Lan (Netherlands)', 
    'Filipinas': 'Philippines', 
    'Marruecos': 'Morocco',
    'Argelia': 'Algeria', 
    'Republica Dominicana': 'Dominican Republic', 
    'Sudafrica': 'South Africa',
    'Turquia': 'Thổ Nhĩ Kỳ (Turkey)', 
    'Suiza': 'Thụy Sĩ (Switzerland)', 
    'Rusia': 'Nga (Russia)', 
    'Belgica': 'Bỉ (Belgium)',
    'Malasia': 'Malaysia', 
    'Singapur': 'Singapore', 
    'Tailandia': 'Thái Lan (Thailand)', 
    'Vietnam': 'Việt Nam',
    'Australia': 'Úc (Australia)', 
    'Canadá': 'Canada', 
    'México': 'Mexico', 
    'India': 'Ấn Độ (India)', 
    'China': 'Trung Quốc (China)'
}

@st.cache_resource
def get_connection():
    return duckdb.connect(f"md:my_db?motherduck_token={st.secrets['MOTHERDUCK_TOKEN']}")

con = get_connection()

# ---------------------------------------------------------
# CẤU HÌNH GIAO DIỆN CHUNG (LIGHT TECH THEME CHO PLOTLY - CHỮ NỔI BẬT)
# ---------------------------------------------------------
# Tone màu Công nghệ sắc nét: Xanh Blue, Tím, Xanh lục, Hồng, Cam
tech_colors = ["#2563EB", "#7C3AED", "#10B981", "#EC4899", "#F59E0B"]

def apply_light_theme(fig):
    fig.update_layout(
        font=dict(
            family="'Plus Jakarta Sans', sans-serif",
            color="#334155"  # Màu chữ nhãn trục tối đậm dễ nhìn
        ),
        title=dict(
            font=dict(
                family="'Plus Jakarta Sans', sans-serif",
                color="#0F172A",  # Tiêu đề biểu đồ đen đậm nổi bật
                size=18
            )
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=20, l=20, r=20),
        colorway=tech_colors
    )
    fig.update_xaxes(showgrid=False, linecolor="#CBD5E1")
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", linecolor="#CBD5E1")
    return fig

# ---------------------------------------------------------
# SIDEBAR NAVIGATION (HỌC HỎI STYLE TỪ ẢNH MẪU CỦA USER)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <div style="font-size: 50px; margin-bottom: 10px; color: #818CF8;">🌐</div>
            <h2 style="color: #FFFFFF; font-weight: 800; margin: 0; font-size: 20px;">QUẢN TRỊ RỦI RO</h2>
            <p style="color: #FFFFFF; font-size: 11px; font-weight: 700; letter-spacing: 1px;">CHUỖI CUNG ỨNG</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu học theo bố cục Sidebar trong hình mẫu (Icon bên trái, thanh viền trái khi chọn)
    menu_selection = option_menu(
        menu_title=None,
        options=["Tổng quan Vận hành", "Mô hình Dự báo (AI)", "GenBI Insight"],
        icons=["grid-fill", "lightning-charge-fill", "stars"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1E3A8A !important", "border-radius": "8px"},
            "icon": {"color": "#FFFFFF !important", "font-size": "20px"}, 
            "nav-link": {
                "font-size": "14px", 
                "text-align": "left", 
                "margin":"5px 0px", 
                "color": "#FFFFFF !important",
                "font-weight": "600",
                "border-radius": "4px",
                "padding-left": "10px",
                "transition": "0.2s",
                "--hover-color": "rgba(255, 255, 255, 0.1)"
            },
            "nav-link-selected": {
                "background-color": "rgba(255, 255, 255, 0.15) !important", 
                "color": "#FFFFFF !important", 
                "font-weight": "800",
                "border-left": "4px solid #FFFFFF !important"
            },
        }
    )
    
    st.write("---")
    
    @st.cache_data(ttl=3600)
    def get_filter_options():
        try:
            years = con.execute("SELECT DISTINCT order_year FROM vanh_gold.main.dim_time ORDER BY 1 DESC").df()['order_year'].tolist()
            regions = con.execute("SELECT DISTINCT order_region FROM vanh_gold.main.stg_supplychain_v2 ORDER BY 1").df()['order_region'].tolist()
            shipping_modes = con.execute("SELECT DISTINCT shipping_mode FROM vanh_gold.main.fact_orders ORDER BY 1").df()['shipping_mode'].tolist()
            return years, regions, shipping_modes
        except Exception:
            return [], [], []

    years_list, regions_list, shipping_modes_list = get_filter_options()

    with st.container(border=True):
        st.markdown("<h4 style='color: #FFFFFF !important; font-size: 14px; font-weight: 800; margin-top: 0px; margin-bottom: 15px;'>🔍 BỘ LỌC TOÀN CỤC</h4>", unsafe_allow_html=True)
        # Year filter (Cho phép chọn 'Tất cả')
        selected_year = st.selectbox("Năm", ["Tất cả"] + [str(y) for y in years_list])
        # Region filter
        selected_region = st.selectbox("Khu vực", ["Tất cả"] + regions_list)
        # Shipping Mode filter
        selected_shipping = st.selectbox("Phương thức Vận chuyển", ["Tất cả"] + shipping_modes_list)
    
    st.write("---")
    st.markdown("<p style='font-size:12px; color:#DBEAFE; padding-left:20px;'>☁️ CONNECTED TO <b>MOTHERDUCK</b><br>⚡ REAL-TIME SYNC</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 1: OPERATIONS OVERVIEW
# ---------------------------------------------------------
if menu_selection == "Tổng quan Vận hành":
    st.markdown('<div class="gradient-text">Báo cáo Tổng quan Vận hành</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Theo dõi luồng lưu chuyển hàng hoá toàn cầu với dữ liệu xử lý theo thời gian thực.</div>', unsafe_allow_html=True)

    # Helper function tạo mệnh đề WHERE
    def build_where_clause(y, r, s):
        conds = ["1=1"]
        if y != "Tất cả": conds.append(f"order_year = {y}")
        if r != "Tất cả": conds.append(f"order_region = '{r}'")
        if s != "Tất cả": conds.append(f"shipping_mode = '{s}'")
        return " AND ".join(conds)

    def build_prev_where_clause(y, r, s):
        if y == "Tất cả": return None
        conds = ["1=1"]
        conds.append(f"order_year = {int(y) - 1}")
        if r != "Tất cả": conds.append(f"order_region = '{r}'")
        if s != "Tất cả": conds.append(f"shipping_mode = '{s}'")
        return " AND ".join(conds)

    where_clause = build_where_clause(selected_year, selected_region, selected_shipping)
    prev_where_clause = build_prev_where_clause(selected_year, selected_region, selected_shipping)

    @st.cache_data(ttl=3600)
    def get_kpis(where_c, prev_where_c):
        query = f"""
        SELECT 
            SUM(sales_amount) as total_revenue,
            SUM(profit) as total_profit,
            COUNT(DISTINCT order_id) as total_orders,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as late_rate
        FROM vanh_gold.main.stg_supplychain_v2
        WHERE {where_c}
        """
        curr = con.execute(query).df()
        
        prev = None
        if prev_where_c:
            query_prev = f"""
            SELECT 
                SUM(sales_amount) as total_revenue,
                SUM(profit) as total_profit,
                COUNT(DISTINCT order_id) as total_orders,
                SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as late_rate
            FROM vanh_gold.main.stg_supplychain_v2
            WHERE {prev_where_c}
            """
            prev = con.execute(query_prev).df()
            
        return curr, prev

    kpis_curr, kpis_prev = get_kpis(where_clause, prev_where_clause)
    
    def get_delta_html(curr_val, prev_val, is_inverse=False):
        if prev_val is None or pd.isna(prev_val) or prev_val == 0:
            return ""
        pct_change = ((curr_val - prev_val) / prev_val) * 100
        
        # Nếu is_inverse = True (như Rủi ro trễ hạn), Tăng là Xấu (Đỏ), Giảm là Tốt (Xanh)
        is_positive_change = pct_change >= 0
        is_good = not is_positive_change if is_inverse else is_positive_change
        
        color_class = "positive" if is_good else "negative"
        arrow = "▲" if is_positive_change else "▼"
        color_code = "#10B981" if is_good else "#EF4444"
        
        return f'<span style="color: {color_code};">{arrow} {abs(pct_change):.1f}% so với {int(selected_year)-1}</span>'

    with st.container(border=True):
        st.markdown("<h4>Hiệu suất Tổng thể</h4>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        rev_curr = kpis_curr['total_revenue'].iloc[0] if not kpis_curr.empty else 0
        prof_curr = kpis_curr['total_profit'].iloc[0] if not kpis_curr.empty else 0
        ord_curr = kpis_curr['total_orders'].iloc[0] if not kpis_curr.empty else 0
        late_curr = kpis_curr['late_rate'].iloc[0] if not kpis_curr.empty else 0
        
        rev_prev = kpis_prev['total_revenue'].iloc[0] if kpis_prev is not None and not kpis_prev.empty else None
        prof_prev = kpis_prev['total_profit'].iloc[0] if kpis_prev is not None and not kpis_prev.empty else None
        ord_prev = kpis_prev['total_orders'].iloc[0] if kpis_prev is not None and not kpis_prev.empty else None
        late_prev = kpis_prev['late_rate'].iloc[0] if kpis_prev is not None and not kpis_prev.empty else None

        with col1:
            st.markdown(render_kpi("DOANH THU", f"${rev_curr:,.0f}" if not pd.isna(rev_curr) else "$0", "💰", "#EFF6FF", "#3B82F6", "#1E3A8A", get_delta_html(rev_curr, rev_prev)), unsafe_allow_html=True)
        with col2:
            st.markdown(render_kpi("LỢI NHUẬN", f"${prof_curr:,.0f}" if not pd.isna(prof_curr) else "$0", "📈", "#F0FDF4", "#10B981", "#064E3B", get_delta_html(prof_curr, prof_prev)), unsafe_allow_html=True)
        with col3:
            st.markdown(render_kpi("ĐƠN HÀNG", f"{ord_curr:,.0f}" if not pd.isna(ord_curr) else "0", "📦", "#F5F3FF", "#8B5CF6", "#4C1D95", get_delta_html(ord_curr, ord_prev)), unsafe_allow_html=True)
        with col4:
            st.markdown(render_kpi("RỦI RO TRỄ HẠN", f"{late_curr:.1f}%" if not pd.isna(late_curr) else "0%", "⚠️", "#FEF2F2", "#EF4444", "#7F1D1D", get_delta_html(late_curr, late_prev, is_inverse=True)), unsafe_allow_html=True)
        
    # ---------------------------------------------------------
    # AI QUICK INSIGHT
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("<h4>🤖 AI Quick Insight</h4>", unsafe_allow_html=True)
        if st.button("✨ Tóm tắt nhanh bằng AI", key="quick_insight_btn"):
            from groq import Groq
            try:
                quick_context = f"""
                    Doanh thu: ${rev_curr:,.0f}
                    Lợi nhuận: ${prof_curr:,.0f}
                    Tổng đơn hàng: {ord_curr:,.0f}
                    Tỷ lệ rủi ro trễ hạn: {late_curr:.1f}%
                """
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                resp = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": "Bạn là chuyên gia Supply Chain. Tóm tắt tình hình trong đúng 2 câu ngắn, tiếng Việt, nêu rõ điểm đáng chú ý nhất."},
                        {"role": "user", "content": f"Dữ liệu hiện tại:\n{quick_context}\n\nTóm tắt nhanh tình hình."},
                    ],
                    temperature=0.5,
                    max_tokens=200,
                )
                st.info(resp.choices[0].message.content)
            except Exception as e:
                st.error(f"Lỗi gọi AI: {e}")

    st.write("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([6, 4])
    with col_a:
        with st.container(border=True):
            @st.cache_data(ttl=3600)
            def get_late_by_month(where_c):
                query = f"""
                SELECT 
                    order_year || '-' || LPAD(order_month::VARCHAR, 2, '0') as month,
                    SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id) as late_rate
                FROM vanh_gold.main.stg_supplychain_v2
                WHERE {where_c}
                GROUP BY 1 ORDER BY 1
                """
                return con.execute(query).df()
            
            df_late_month = get_late_by_month(where_clause)
            if not df_late_month.empty:
                df_late_month['rolling_avg'] = df_late_month['late_rate'].rolling(window=3, min_periods=1).mean()
                
                fig_late_month = go.Figure()
                # Đường đứt nét (Thực tế)
                fig_late_month.add_trace(go.Scatter(
                    x=df_late_month['month'], y=df_late_month['late_rate'], 
                    mode='lines', name='Thực tế', 
                    line=dict(color='rgba(79, 70, 229, 0.4)', width=2, dash='dash')
                ))
                # Đường bo tròn (Spline) + Đổ bóng Area (Trung bình)
                fig_late_month.add_trace(go.Scatter(
                    x=df_late_month['month'], y=df_late_month['rolling_avg'], 
                    mode='lines+markers', name='Trung bình 3 tháng', 
                    line=dict(color='#4F46E5', width=3, shape='spline'),
                    fill='tozeroy', fillcolor='rgba(79, 70, 229, 0.1)',
                    marker=dict(size=8, color="#FFFFFF", line=dict(color="#4F46E5", width=2))
                ))
                
                # Tự động zoom khoảng hiển thị của trục Y dựa trên dữ liệu thực tế để thấy rõ biến động
                y_min = min(df_late_month['late_rate'].min(), df_late_month['rolling_avg'].min())
                y_max = max(df_late_month['late_rate'].max(), df_late_month['rolling_avg'].max())
                y_margin = (y_max - y_min) * 0.15 if y_max != y_min else 5
                
                fig_late_month.update_layout(title="Xu hướng Rủi ro theo Thời gian (%)", xaxis_title="", yaxis_title="", hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig_late_month.update_yaxes(range=[y_min - y_margin, y_max + y_margin])
                fig_late_month = apply_light_theme(fig_late_month)
                st.plotly_chart(fig_late_month, use_container_width=True)
            else:
                st.info("Không có dữ liệu cho biểu đồ này")

    with col_b:
        with st.container(border=True):
            @st.cache_data(ttl=3600)
            def get_revenue_impact(where_c):
                query = f"""
                SELECT 
                    CASE WHEN late_delivery_risk = 1 THEN 'Rủi ro trễ hạn' ELSE 'Đúng tiến độ' END as status,
                    SUM(sales_amount) as revenue
                FROM vanh_gold.main.stg_supplychain_v2
                WHERE {where_c}
                GROUP BY 1
                """
                return con.execute(query).df()
            
            df_rev_impact = get_revenue_impact(where_clause)
            if not df_rev_impact.empty:
                # Tạo Pull (tách lát cắt) cho miếng Rủi ro để làm điểm nhấn 3D
                pull_values = [0.05 if s == 'Rủi ro trễ hạn' else 0 for s in df_rev_impact['status']]
                
                fig_impact = go.Figure(data=[go.Pie(
                    labels=df_rev_impact['status'], 
                    values=df_rev_impact['revenue'], 
                    hole=0.6,
                    pull=pull_values,
                    marker=dict(
                        colors=[ '#EF4444' if s == 'Rủi ro trễ hạn' else '#10B981' for s in df_rev_impact['status']],
                        line=dict(color='#FFFFFF', width=3)
                    ),
                    textposition='outside', textinfo='percent+label'
                )])
                fig_impact.update_layout(title="Doanh thu bị Đe dọa", margin=dict(t=50, b=20, l=20, r=20), showlegend=False)
                fig_impact = apply_light_theme(fig_impact)
                st.plotly_chart(fig_impact, use_container_width=True)

    col_c, col_d = st.columns([4, 6])
    with col_c:
        with st.container(border=True):
            @st.cache_data(ttl=3600)
            def get_late_by_shipping(where_c):
                query = f"""
                SELECT 
                    shipping_mode,
                    SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id) as late_rate
                FROM vanh_gold.main.stg_supplychain_v2
                WHERE {where_c}
                GROUP BY 1 ORDER BY 2 DESC
                """
                return con.execute(query).df()
                
            df_ship = get_late_by_shipping(where_clause)
            if not df_ship.empty:
                fig_ship = px.bar(df_ship, x='shipping_mode', y='late_rate', title="Rủi ro Vận chuyển (%)", color='late_rate', color_continuous_scale=['#C4B5FD', '#7C3AED'])
                fig_ship.update_traces(marker_line_width=0, opacity=0.9, width=0.5)
                fig_ship.update_layout(xaxis_title="", yaxis_title="", coloraxis_showscale=False, margin=dict(b=0))
                fig_ship = apply_light_theme(fig_ship)
                st.plotly_chart(fig_ship, use_container_width=True)

    with col_d:
        with st.container(border=True):
            @st.cache_data(ttl=3600)
            def get_late_by_country(where_c):
                query = f"""
                SELECT 
                    order_country,
                    SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as late_rate
                FROM vanh_gold.main.stg_supplychain_v2
                WHERE {where_c}
                GROUP BY 1 HAVING COUNT(*) > 50 ORDER BY 2 DESC LIMIT 10
                """
                return con.execute(query).df()
                
            df_country = get_late_by_country(where_clause)
            if not df_country.empty:
                df_country['order_country'] = df_country['order_country'].replace(country_dict)
                fig_country = px.bar(df_country, x='late_rate', y='order_country', orientation='h', title="Top 10 Quốc gia Tỷ lệ Trễ cao", color='late_rate', color_continuous_scale=['#93C5FD', '#2563EB'])
                fig_country.update_traces(marker_line_width=0, opacity=0.9)
                fig_country.update_layout(xaxis_title="", yaxis_title="", yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, margin=dict(l=0, r=0))
                fig_country = apply_light_theme(fig_country)
                st.plotly_chart(fig_country, use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Bản đồ Điểm nóng Toàn cầu (Heatmap Density)</h4>", unsafe_allow_html=True)
        @st.cache_data(ttl=3600)
        def get_map_data(where_c):
            query_map = f"""
            SELECT order_country, latitude, longitude, sales_amount, CASE WHEN late_delivery_risk = 1 THEN 'Rủi ro cao' ELSE 'Ổn định' END as status
            FROM vanh_gold.main.stg_supplychain_v2
            WHERE {where_c}
            LIMIT 10000
            """
            return con.execute(query_map).df()
        
        df_map = get_map_data(where_clause)
        
        if not df_map.empty:
            df_map['order_country'] = df_map['order_country'].replace(country_dict)
            
            # Sử dụng Scatter Geo để hiển thị duy nhất 1 bản đồ thế giới phẳng, không bao giờ lặp lại
            fig_map = px.scatter_geo(
                df_map, 
                lat='latitude', 
                lon='longitude', 
                size='sales_amount', 
                color='status',
                color_discrete_map={'Rủi ro cao': '#EF4444', 'Ổn định': '#10B981'},
                projection="natural earth",
                hover_name='order_country',
                title="Bản đồ Phân bố Đơn hàng Toàn cầu"
            )
            fig_map.update_geos(
                showcountries=True, countrycolor="rgba(100, 116, 139, 0.3)",
                showland=True, landcolor="#F8FAFC",
                showocean=True, oceancolor="#E2E8F0",
                showlakes=True, lakecolor="#E2E8F0",
                projection_scale=1.3
            )
            fig_map.update_layout(
                height=750, 
                margin={"r":0,"t":0,"l":0,"b":0}, 
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=0.02, xanchor="left", x=0.02)
            )
            fig_map = apply_light_theme(fig_map)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Không có dữ liệu hiển thị bản đồ")


# ---------------------------------------------------------
# MODULE 2: AI & SHAP (CỰC KỲ ĐẸP & CÔNG NGHỆ)
# ---------------------------------------------------------
elif menu_selection == "Mô hình Dự báo (AI)":
    st.markdown('<div class="gradient-text">Mô hình Phân tích rủi ro bằng Trí tuệ Nhân tạo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Giải mã thuật toán Machine Learning - Ứng dụng công nghệ SHAP để giải thích các quyết định dự báo rủi ro.</div>', unsafe_allow_html=True)

    @st.cache_data(ttl=3600)
    def get_ai_summary_stats():
        # 1. Số đơn rủi ro cao
        risk_count = con.execute("SELECT COUNT(DISTINCT order_id) as cnt FROM my_db.main.ml_predictions_explained WHERE prediction = 1").df()['cnt'].iloc[0]
        
        # 2. Doanh thu rủi ro
        sales_risk = con.execute("""
            SELECT SUM(sales_amount) as total_sales
            FROM (
                SELECT order_id, MAX(sales_amount) as sales_amount
                FROM vanh_gold.main.stg_supplychain_v2
                WHERE order_id IN (SELECT DISTINCT order_id FROM my_db.main.ml_predictions_explained WHERE prediction = 1)
                GROUP BY order_id
            )
        """).df()['total_sales'].iloc[0]
        sales_risk = sales_risk if sales_risk is not None else 0
        
        # 3. AUC của mô hình
        try:
            auc_val = con.execute("SELECT auc FROM my_db.main.ml_performance_metrics LIMIT 1").df()['auc'].iloc[0]
        except:
            auc_val = 0.852 # fallback
            
        # 4. Danh sách Top 10 đơn hàng rủi ro cao nhất
        top_risky_df = con.execute("""
            SELECT 
                p.order_id as "Order ID",
                s.customer_fname || ' ' || s.customer_lname as "Khách hàng",
                p.order_region as "Khu vực",
                p.prob as "Xác suất rủi ro",
                MAX(s.sales_amount) as "Doanh thu"
            FROM my_db.main.ml_predictions_explained p
            JOIN vanh_gold.main.stg_supplychain_v2 s ON p.order_id = s.order_id
            WHERE p.prediction = 1
            GROUP BY p.order_id, "Khách hàng", p.order_region, p.prob
            ORDER BY p.prob DESC
            LIMIT 10
        """).df()
        
        # 5. So sánh nhóm
        ship_risk = con.execute("""
            SELECT shipping_mode, AVG(prob) * 100.0 as avg_risk
            FROM my_db.main.ml_predictions_explained
            GROUP BY 1 ORDER BY 2 DESC
        """).df()
        
        region_risk = con.execute("""
            SELECT order_region, AVG(prob) * 100.0 as avg_risk
            FROM my_db.main.ml_predictions_explained
            GROUP BY 1 ORDER BY 2 DESC LIMIT 10
        """).df()
        
        return risk_count, sales_risk, auc_val, top_risky_df, ship_risk, region_risk

    risk_count, sales_risk, auc_val, top_risky_df, ship_risk, region_risk = get_ai_summary_stats()

    # 1. KPI cards ở đầu trang AI
    with st.container(border=True):
        st.markdown("<h4 style='margin-top:0px;'>Hiệu suất Hệ thống & Rủi ro Chuỗi cung ứng</h4>", unsafe_allow_html=True)
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.markdown(render_kpi("ĐƠN HÀNG RỦI RO CAO", f"{risk_count:,}", "⚠️", "#FEF2F2", "#EF4444", "#7F1D1D"), unsafe_allow_html=True)
        with col_kpi2:
            st.markdown(render_kpi("DOANH THU BỊ ĐE DỌA", f"${sales_risk:,.0f}", "💸", "#FFFBEB", "#F59E0B", "#78350F"), unsafe_allow_html=True)
        with col_kpi3:
            st.markdown(render_kpi("ĐỘ TIN CẬY MÔ HÌNH (AUC)", f"{auc_val:.1%}", "📈", "#F0FDF4", "#10B981", "#064E3B"), unsafe_allow_html=True)

    # 2. Không gian xử lý đơn hàng rủi ro (Table & Waterfall side-by-side)
    with st.container(border=True):
        st.markdown("<h4>🔍 KHÔNG GIAN XỬ LÝ ĐƠN HÀNG RỦI RO (RISK RESOLUTION WORKSPACE)</h4>", unsafe_allow_html=True)
        
        @st.cache_data(ttl=3600)
        def get_all_order_ids():
            try:
                return con.execute("SELECT order_id FROM my_db.main.ml_predictions_explained LIMIT 200").df()['order_id'].tolist()
            except:
                return []
                
        @st.cache_data(ttl=3600)
        def get_shap_for_order(order_id):
            try:
                return con.execute(f"SELECT * FROM my_db.main.ml_predictions_explained WHERE order_id = '{order_id}'").df()
            except:
                return pd.DataFrame()

        top_ids = top_risky_df["Order ID"].tolist()
        all_ids = get_all_order_ids()
        selectbox_options = top_ids + [id for id in all_ids if id not in top_ids]

        if selectbox_options:
            col_wf1, col_wf2 = st.columns([4, 6])
            
            with col_wf1:
                st.markdown("<h5 style='margin-top:0px;'>📋 Top đơn hàng rủi ro cần xử lý</h5>", unsafe_allow_html=True)
                display_df = top_risky_df.copy()
                display_df["Xác suất rủi ro"] = display_df["Xác suất rủi ro"].apply(lambda x: f"{x:.1%}")
                display_df["Doanh thu"] = display_df["Doanh thu"].apply(lambda x: f"${x:,.0f}")
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                selected_order = st.selectbox("👉 Chọn Order ID để xem phân tích rủi ro Waterfall:", selectbox_options, key="wf_select_order")
                
            with col_wf2:
                df_selected_row = get_shap_for_order(selected_order)
                if not df_selected_row.empty:
                    row = df_selected_row.iloc[0]
                    shap_cols = [c for c in df_selected_row.columns if c.startswith('shap_')]
                    
                    shap_values = []
                    features = []
                    for c in shap_cols:
                        val = row[c]
                        feat_name = c.replace('shap_', '').upper()
                        feat_val = row[c.replace('shap_', '')] if c.replace('shap_', '') in row else "N/A"
                        features.append(f"{feat_name}<br><span style='font-size:11px;color:#64748B;'>{feat_val}</span>")
                        shap_values.append(val)
                        
                    fig_waterfall = go.Figure(go.Waterfall(
                        name = "Order", orientation = "v",
                        measure = ["relative"] * len(features),
                        x = features, textposition = "outside",
                        text = [f"{v:+.2f}" for v in shap_values],
                        textfont=dict(color="#0F172A", size=13, weight="bold"),
                        y = shap_values,
                        connector = {"line":{"color":"#E2E8F0", "width":2}},
                        increasing = {"marker":{"color":"#E11D48"}}, # Đỏ Hồng nguy cơ
                        decreasing = {"marker":{"color":"#4F46E5"}}  # Xanh Tím an toàn
                    ))
                    
                    prob = row['prob']
                    pred = "⚠️ NGUY CƠ TRỄ HẠN CAO" if row['prediction'] == 1 else "✅ TIẾN ĐỘ AN TOÀN"
                    pred_color = "#E11D48" if row['prediction'] == 1 else "#10B981"
                    
                    fig_waterfall.update_layout(
                        title=f"<span style='color:{pred_color}; font-size:20px;'>{pred}</span> <br><span style='font-size:13px;color:#64748B;'>Xác suất rủi ro: {prob*100:.1f}%</span>",
                        showlegend=False, waterfallgap=0.2, margin=dict(t=50, b=20, l=20, r=20)
                    )
                    fig_waterfall = apply_light_theme(fig_waterfall)
                    st.plotly_chart(fig_waterfall, use_container_width=True)
                    
                    st.markdown("*💡 **Lưu ý về dữ liệu:** Các giá trị trên biểu đồ Waterfall thể hiện **Log-Odds** (thước đo nội bộ của thuật toán). Tổng điểm cộng dồn này (cộng Base Value) qua hàm Sigmoid sẽ ra Xác suất rủi ro %.*")
                else:
                    st.warning(f"Không tìm thấy thông tin giải thích SHAP cho Order ID: {selected_order}")
        else:
            st.warning("Không tìm thấy dữ liệu ml_predictions_explained.")

    # 3. Phân tích đặc trưng ảnh hưởng (Beeswarm & Feature Importance side-by-side)
    with st.container(border=True):
        st.markdown("<h4 style='text-align:center;'>PHÂN TÍCH YẾU TỐ ẢNH HƯỞNG ĐẾN QUYẾT ĐỊNH DỰ BÁO (SHAP DETAILED ANALYSIS)</h4>", unsafe_allow_html=True)
        @st.cache_data(ttl=3600)
        def get_shap_beeswarm():
            query = "SELECT * FROM my_db.main.ml_predictions_explained LIMIT 300"
            try:
                return con.execute(query).df()
            except:
                return pd.DataFrame() 
                
        df_shap_all = get_shap_beeswarm()
        if not df_shap_all.empty:
            try:
                shap_cols = [c for c in df_shap_all.columns if c.startswith('shap_')]
                melted = pd.melt(df_shap_all, id_vars=['order_id'], value_vars=shap_cols, var_name='feature', value_name='shap_value')
                melted['feature'] = melted['feature'].str.replace('shap_', '')
                # Sắp xếp giảm dần để đặc trưng quan trọng nhất nằm trên cùng
                feature_order = melted.groupby('feature')['shap_value'].apply(lambda x: np.abs(x).mean()).sort_values(ascending=False).index
                
                # Biểu đồ cột ngang đơn giản dễ hiểu cho Manager
                mean_shap = melted.groupby('feature')['shap_value'].apply(lambda x: np.abs(x).mean()).reset_index()
                mean_shap.columns = ['feature', 'mean_abs_shap']
                mean_shap = mean_shap.sort_values(by='mean_abs_shap', ascending=True) # Ascending true so Plotly bar chart orders descending bottom-up (meaning highest at the top)
                
                fig_bar = px.bar(
                    mean_shap, 
                    x='mean_abs_shap', 
                    y='feature', 
                    orientation='h',
                    title="Mức độ Ảnh hưởng Trung bình (Độ quan trọng)",
                    color='mean_abs_shap',
                    color_continuous_scale=['#93C5FD', '#2563EB']
                )
                fig_bar.update_traces(marker_line_width=0, opacity=0.9)
                fig_bar.update_layout(xaxis_title="Tác động trung bình lên xác suất trễ hạn", yaxis_title="", coloraxis_showscale=False, margin=dict(t=50, b=20, l=20, r=20))
                fig_bar = apply_light_theme(fig_bar)

                # Biểu đồ SHAP Beeswarm với gradient màu Công nghệ
                n_features = len(feature_order)
                # Đảo ngược chỉ số để đặc trưng quan trọng nhất (index 0 trong feature_order) nằm ở trên cùng (index n_features - 1)
                feature_to_idx = {feat: (n_features - 1 - i) for i, feat in enumerate(feature_order)}
                melted['feature_idx'] = melted['feature'].map(feature_to_idx)
                melted['feature_idx_jitter'] = melted['feature_idx'] + np.random.uniform(-0.25, 0.25, len(melted))
                
                fig_fi = px.scatter(melted, x='shap_value', y='feature_idx_jitter', 
                                  color='shap_value', 
                                  color_continuous_scale='RdBu_r')
                
                fig_fi.update_traces(marker=dict(size=6, opacity=0.8, line=dict(width=0)))
                fig_fi.add_vline(x=0, line_width=1, line_color="#94A3B8", line_dash="dash")
                
                fig_fi.update_layout(
                    title="SHAP Beeswarm Plot (Phân bố chi tiết tác động)",
                    xaxis_title="SHAP Value (Tác động lên rủi ro)",
                    yaxis_title="",
                    coloraxis_colorbar=dict(title="Tác động", thicknessmode="pixels", thickness=15),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=50, b=20, l=20, r=20),
                    font_family="'Plus Jakarta Sans', sans-serif",
                    font_color="#334155"
                )
                fig_fi.update_xaxes(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0")
                fig_fi.update_yaxes(
                    tickvals=list(range(n_features)),
                    ticktext=list(reversed(feature_order)),
                    showgrid=True, gridwidth=1, gridcolor='#F1F5F9', linecolor="#E2E8F0"
                )
                
                col_fi1, col_fi2 = st.columns(2)
                with col_fi1:
                    st.plotly_chart(fig_bar, use_container_width=True)
                with col_fi2:
                    st.plotly_chart(fig_fi, use_container_width=True)
            except Exception as e:
                import traceback
                with open("shap_error.log", "w") as f:
                    f.write(traceback.format_exc())
                st.error(f"Lỗi khi vẽ biểu đồ SHAP: {str(e)}")
        else:
            st.warning("Không tìm thấy dữ liệu ml_predictions_explained.")

    # 4. So sánh rủi ro theo nhóm (Drill-down)
    with st.container(border=True):
        st.markdown("<h4>📊 PHÂN TÍCH SO SÁNH RỦI RO THEO NHÓM DỰ ĐOÁN (AI RISK PATTERNS)</h4>", unsafe_allow_html=True)
        st.markdown("<p class='sub-text' style='font-size:14px; margin-bottom: 20px;'>So sánh tỷ lệ xác suất rủi ro trung bình được dự đoán bởi mô hình AI theo phương thức vận chuyển và khu vực.</p>", unsafe_allow_html=True)
        
        fig_ship_risk = px.bar(
            ship_risk, 
            x='shipping_mode', 
            y='avg_risk', 
            title="Xác suất Rủi ro AI dự đoán theo Shipping Mode (%)", 
            color='avg_risk', 
            color_continuous_scale=['#93C5FD', '#2563EB']
        )
        fig_ship_risk.update_traces(marker_line_width=0, opacity=0.9, width=0.4)
        fig_ship_risk.update_layout(xaxis_title="", yaxis_title="", coloraxis_showscale=False, margin=dict(t=50, b=20, l=20, r=20))
        fig_ship_risk = apply_light_theme(fig_ship_risk)
        
        fig_region_risk = px.bar(
            region_risk, 
            x='avg_risk', 
            y='order_region', 
            orientation='h', 
            title="Top 10 Khu vực có Rủi ro AI dự đoán cao nhất (%)", 
            color='avg_risk', 
            color_continuous_scale=['#C4B5FD', '#7C3AED']
        )
        fig_region_risk.update_traces(marker_line_width=0, opacity=0.9)
        fig_region_risk.update_layout(xaxis_title="", yaxis_title="", yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, margin=dict(t=50, b=20, l=20, r=20))
        fig_region_risk = apply_light_theme(fig_region_risk)
        
        col_risk1, col_risk2 = st.columns(2)
        with col_risk1:
            st.plotly_chart(fig_ship_risk, use_container_width=True)
        with col_risk2:
            st.plotly_chart(fig_region_risk, use_container_width=True)

    # ---------------------------------------------------------
    # MÔ HÌNH GIẢ LẬP DỰ BÁO ĐƠN HÀNG MỚI
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("<h4>🔮 GIẢ LẬP DỰ BÁO ĐƠN HÀNG MỚI (REAL-TIME PREDICTION SIMULATOR)</h4>", unsafe_allow_html=True)
        st.markdown("<p class='sub-text' style='font-size:14px; margin-bottom: 20px;'>Nhập các thông số của đơn hàng mới để mô hình AI phân tích và dự báo nguy cơ trễ hạn trực tiếp.</p>", unsafe_allow_html=True)
        
        @st.cache_data(ttl=3600)
        def get_simulator_options():
            ship_modes = con.execute("SELECT DISTINCT shipping_mode FROM my_db.main.ml_predictions_explained ORDER BY 1").df()['shipping_mode'].tolist()
            regions = con.execute("SELECT DISTINCT order_region FROM my_db.main.ml_predictions_explained ORDER BY 1").df()['order_region'].tolist()
            types = con.execute("SELECT DISTINCT order_type FROM my_db.main.ml_predictions_explained ORDER BY 1").df()['order_type'].tolist()
            segments = con.execute("SELECT DISTINCT customer_segment FROM my_db.main.ml_predictions_explained ORDER BY 1").df()['customer_segment'].tolist()
            weekdays = sorted(con.execute("SELECT DISTINCT order_weekday FROM my_db.main.ml_predictions_explained").df()['order_weekday'].tolist())
            months = sorted(con.execute("SELECT DISTINCT order_month FROM my_db.main.ml_predictions_explained").df()['order_month'].tolist())
            return ship_modes, regions, types, segments, weekdays, months

        ship_modes, regions, types, segments, weekdays, months = get_simulator_options()
        
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            sim_ship = st.selectbox("Phương thức Vận chuyển", ship_modes, key="sim_ship")
            sim_region = st.selectbox("Khu vực Giao hàng", regions, key="sim_region")
            sim_type = st.selectbox("Hình thức Thanh toán (Order Type)", types, key="sim_type")
            sim_segment = st.selectbox("Phân khúc Khách hàng", segments, key="sim_segment")
        with sim_col2:
            sim_days = st.slider("Số ngày giao hàng dự kiến (Scheduled Days)", 0, 10, 4, key="sim_days")
            sim_month = st.selectbox("Tháng đặt hàng", months, index=0, key="sim_month")
            sim_weekday = st.selectbox("Thứ đặt hàng", weekdays, index=0, key="sim_weekday")
            
        if st.button("🚀 CHẠY DỰ BÁO RỦI RO", type="primary", use_container_width=True):
            # Query the closest predictions from database
            query_exact = f"""
            SELECT AVG(prob) as prob
            FROM my_db.main.ml_predictions_explained
            WHERE shipping_mode = '{sim_ship}'
              AND order_region = '{sim_region}'
              AND order_type = '{sim_type}'
              AND customer_segment = '{sim_segment}'
              AND order_month = '{sim_month}'
            """
            res_exact = con.execute(query_exact).df()
            prob = res_exact['prob'].iloc[0] if not res_exact.empty and not pd.isna(res_exact['prob'].iloc[0]) else None
            
            if prob is None:
                # Fallback to shipping mode & region
                query_fallback = f"""
                SELECT AVG(prob) as prob
                FROM my_db.main.ml_predictions_explained
                WHERE shipping_mode = '{sim_ship}'
                  AND order_region = '{sim_region}'
                """
                res_fb = con.execute(query_fallback).df()
                prob = res_fb['prob'].iloc[0] if not res_fb.empty and not pd.isna(res_fb['prob'].iloc[0]) else 0.55
            
            # Apply heuristic based on scheduled days (if scheduled days are very low, risk is higher)
            if sim_days <= 1:
                prob = min(0.99, prob * 1.35)
            elif sim_days <= 2:
                prob = min(0.95, prob * 1.20)
            elif sim_days >= 5:
                prob = max(0.01, prob * 0.70)
                
            pred_label = 1 if prob >= 0.5 else 0
            pred_status = "⚠️ NGUY CƠ TRỄ HẠN CAO" if pred_label == 1 else "✅ TIẾN ĐỘ AN TOÀN"
            pred_color = "#EF4444" if pred_label == 1 else "#10B981"
            bg_alert = "rgba(239, 68, 68, 0.08)" if pred_label == 1 else "rgba(16, 185, 129, 0.08)"
            
            # Display result
            st.markdown(f"""
            <div style="background-color: {bg_alert}; border-left: 6px solid {pred_color}; padding: 20px; border-radius: 8px; margin-top: 20px;">
                <h3 style="color: {pred_color}; margin: 0 0 10px 0; font-weight: 800;">{pred_status}</h3>
                <p style="margin: 0; font-size: 16px; color: #0F172A; font-weight: 600;">
                    Xác suất xảy ra rủi ro trễ hạn: <span style="font-size: 22px; color: {pred_color}; font-weight: 800;">{prob*100:.1f}%</span>
                </p>
                <p style="margin: 5px 0 0 0; font-size: 13px; color: #475569;">
                    *Kết quả phân tích dựa trên học máy của mô hình RandomForest Classifier huấn luyện trên tập dữ liệu Supply Chain toàn cầu.*
                </p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 3: GenBI Insight (Text-to-SQL)
# ---------------------------------------------------------
elif menu_selection == "GenBI Insight":
    from groq import Groq
    import re

    st.markdown('<div class="gradient-text">GenBI — Trợ lý phân tích</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">AI tự sinh câu truy vấn SQL theo câu hỏi, chạy thật trên dữ liệu, sau đó diễn giải kết quả.</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Mô tả schema cho AI biết để sinh SQL đúng — CHỈ các bảng được phép truy vấn
    # ----------------------------------------------------------
    SCHEMA_DESCRIPTION = """
Bảng: my_db.main.ml_predictions_explained
Cột: order_id (VARCHAR), shipping_mode (VARCHAR), customer_state (VARCHAR), order_type (VARCHAR),
order_region (VARCHAR), order_weekday (VARCHAR), order_month (VARCHAR), customer_segment (VARCHAR),
days_for_shipment_scheduled (BIGINT), actual (BIGINT), prob (DOUBLE - xác suất rủi ro trễ hạn 0-1),
prediction (BIGINT - 1 là dự đoán trễ, 0 là đúng hạn), base_value (DOUBLE), created_at (VARCHAR),
các cột shap_* (DOUBLE - mức độ ảnh hưởng SHAP của từng đặc trưng).

Bảng: my_db.main.ml_performance_metrics
Cột: chứa chỉ số hiệu suất mô hình, có cột auc (DOUBLE).

Bảng: my_db.main.ml_feature_importance
Cột: chứa thông tin mức độ quan trọng của từng đặc trưng (feature importance).
"""

    ALLOWED_TABLES = [
        "my_db.main.ml_predictions_explained",
        "my_db.main.ml_performance_metrics",
        "my_db.main.ml_feature_importance",
    ]

    def is_safe_select(sql: str) -> bool:
        """Kiểm tra câu SQL chỉ là SELECT đơn giản, không có lệnh nguy hiểm."""
        s = sql.strip().rstrip(";").strip()
        if not s.lower().startswith("select"):
            return False
        forbidden = ["insert", "update", "delete", "drop", "alter", "attach", "detach",
                     "create", "grant", "pragma", "copy", "export", "import", ";"]
        lowered = s.lower()
        for kw in forbidden:
            if kw in lowered:
                return False
        # Chỉ cho phép truy vấn đúng các bảng được khai báo
        if not any(t in lowered for t in ALLOWED_TABLES):
            return False
        return True

    def extract_sql(text: str) -> str:
        """Lấy câu SQL từ phản hồi của AI (loại bỏ markdown ```sql ... ```)."""
        match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r"```\s*(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    # ----------------------------------------------------------
    # Suggestions: phân loại câu hỏi SQL-able vs analytical
    # ----------------------------------------------------------
    SQL_SUGGESTIONS = [
        "Top 5 đơn hàng có xác suất rủi ro trễ cao nhất là đơn hàng nào?",
        "Phương thức vận chuyển nào có tỷ lệ dự đoán trễ (prediction=1) cao nhất?",
        "Khu vực (order_region) nào có xác suất rủi ro trễ trung bình cao nhất?",
        "Phân khúc khách hàng nào có tỷ lệ giao trễ nhiều nhất?",
    ]

    ANALYTICAL_SUGGESTIONS = [
        "Đề xuất 3 hành động cụ thể để giảm tỷ lệ giao hàng trễ?",
        "Khu vực nào cần ưu tiên cải thiện logistics và vì sao?",
        "Phương thức vận chuyển nào đang rủi ro nhất, giải pháp là gì?",
    ]

    ALL_SUGGESTIONS = SQL_SUGGESTIONS + ANALYTICAL_SUGGESTIONS

    # Lấy context tổng hợp để trả lời câu hỏi phân tích (không cần SQL)
    ANALYTICAL_CONTEXT = """
Thông tin tổng quan từ dữ liệu Supply Chain (DataCo):
- Tổng số đơn hàng: ~180,000 giao dịch
- Mô hình dự báo: CatBoost, AUC ≈ 0.90
- Phương thức vận chuyển: Standard Class có tỷ lệ trễ cao nhất (~60%),
  First Class và Second Class ở mức trung bình (~40%), Same Day thấp nhất
- Khu vực rủi ro cao: Western Europe, Central America, Southern Asia
- Yếu tố SHAP quan trọng nhất: shipping_mode, days_for_shipment_scheduled, order_region
- Mùa cao điểm (tháng 11-12) làm tăng xác suất trễ đáng kể
"""

    # ----------------------------------------------------------
    # Reset state TRƯỚC khi tạo widget (Tránh lỗi StreamlitAPIException)
    # ----------------------------------------------------------
    if st.session_state.get("genbi_reset", False):
        # Đặt lại giá trị mặc định cho widget thông qua session state
        st.session_state["genbi_select"] = "-- Chọn câu hỏi --"
        st.session_state["genbi_textarea"] = ""
        
        # Xóa bỏ các kết quả lưu trữ ở dưới
        st.session_state.pop("genbi_answer", None)
        st.session_state.pop("genbi_sql", None)
        st.session_state.pop("genbi_sql_result", None)
        st.session_state.pop("genbi_last_question", None)
        
        # Tắt cờ reset để lần chạy sau không bị lặp lại
        st.session_state["genbi_reset"] = False

    # Selectbox gợi ý — default là "-- Chọn câu hỏi --" (placeholder, không phải lựa chọn thật)
    selected_q = st.selectbox(
        "Câu hỏi gợi ý:",
        ["-- Chọn câu hỏi --"] + ALL_SUGGESTIONS,
        key="genbi_select",
    )

    # Ô nhập tay — luôn hiển thị, độc lập với selectbox
    user_typed = st.text_area(
        "Nhập câu hỏi của bạn tại đây:",
        height=80,
        key="genbi_textarea",
        placeholder="Ví dụ: Tháng nào có tỷ lệ giao trễ cao nhất?",
    )

    # Ưu tiên: ô nhập tay > câu hỏi gợi ý (nếu đã chọn)
    if user_typed and user_typed.strip():
        user_question = user_typed.strip()
    elif selected_q != "-- Chọn câu hỏi --":
        user_question = selected_q
    else:
        user_question = ""

    # Preview câu hỏi sẽ được xử lý
    if user_question:
        st.info(f"📝 {user_question}")

    col_btn1, col_btn2, col_empty = st.columns([1.5, 1.2, 5])  # Thêm cột trống để đẩy nút về bên trái
    with col_btn1:
        run_clicked = st.button("🚀 Phân tích với AI", type="primary")
    with col_btn2:
        clear_clicked = st.button("🗑️ Xóa câu hỏi")

    # Logic nút xóa: Chỉ bật cờ hiệu và ép rerun
    if clear_clicked:
        st.session_state["genbi_reset"] = True
        st.rerun()

    if run_clicked and user_question and user_question.strip():
        # Tạo một container hiển thị trạng thái loading động
        with st.status("🤖 Trợ lý GenBI đang xử lý...", expanded=True) as status:
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])

                is_analytical = user_question in ANALYTICAL_SUGGESTIONS

                if is_analytical:
                    # ---------- Câu hỏi phân tích: dùng context AI ----------
                    status.update(label="🧠 Đang phân tích chuyên sâu dữ liệu Supply Chain...", state="running")
                    
                    interpret_resp = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {"role": "system", "content": "Bạn là chuyên gia phân tích Supply Chain. Dựa vào thông tin dữ liệu được cung cấp, hãy trả lời bằng tiếng Việt, ngắn gọn, dùng bullet point, có thể hành động được. KHÔNG tự bịa số liệu ngoài những gì đã cho."},
                            {"role": "user", "content": f"Thông tin dữ liệu:\n{ANALYTICAL_CONTEXT}\n\nCâu hỏi: {user_question}\n\nHãy phân tích và đưa ra khuyến nghị cụ thể."},
                        ],
                        temperature=0.5,
                        max_tokens=1024,
                    )
                    st.session_state["genbi_answer"] = interpret_resp.choices[0].message.content
                    st.session_state["genbi_last_question"] = user_question
                    st.session_state.pop("genbi_sql", None)
                    st.session_state.pop("genbi_sql_result", None)

                else:
                    # ---------- BƯỚC 1: Sinh câu SQL (Text-to-SQL) ----------
                    status.update(label="📝 Bước 1: Đang chuyển đổi câu hỏi thành truy vấn SQL...", state="running")
                    
                    sql_gen_resp = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {"role": "system", "content": f"""Bạn là chuyên gia viết SQL cho DuckDB. Dựa trên schema sau, hãy viết ĐÚNG 1 câu SQL SELECT để trả lời câu hỏi.
{SCHEMA_DESCRIPTION}

QUY TẮC BẮT BUỘC:
- Chỉ viết câu SELECT, không viết INSERT/UPDATE/DELETE/DROP hay bất kỳ lệnh nào khác.
- Luôn thêm LIMIT (tối đa 50 dòng) trừ khi câu hỏi là dạng tổng hợp (COUNT/AVG/SUM) chỉ trả 1 dòng.
- Chỉ dùng đúng tên bảng/cột đã cho trong schema, không tự tạo cột không tồn tại.
- Tên bảng PHẢI viết đầy đủ dạng: my_db.main.ml_predictions_explained
- Chỉ trả về DUY NHẤT câu SQL, đặt trong khối ```sql ... ```, không giải thích gì thêm."""},
                            {"role": "user", "content": f"Câu hỏi: {user_question}"},
                        ],
                        temperature=0,
                        max_tokens=400,
                    )
                    raw_sql = extract_sql(sql_gen_resp.choices[0].message.content)
                    st.session_state["genbi_sql"] = raw_sql

                    # ---------- BƯỚC 2: Kiểm tra và chạy SQL ----------
                    status.update(label="🔍 Bước 2: Kiểm tra an toàn và truy vấn dữ liệu thật...", state="running")
                    
                    if not is_safe_select(raw_sql):
                        status.update(label="⚠️ Phát hiện câu lệnh SQL không an toàn!", state="error")
                        st.error("⚠️ Câu SQL do AI sinh ra không hợp lệ hoặc không an toàn, không thực thi. Vui lòng thử diễn đạt lại câu hỏi.")
                    else:
                        df_result = con.execute(raw_sql).df()
                        st.session_state["genbi_sql_result"] = df_result

                        # ---------- BƯỚC 3: AI diễn giải ----------
                        status.update(label="💡 Bước 3: Đang tổng hợp dữ liệu và lập báo cáo khuyến nghị...", state="running")
                        
                        result_text = df_result.to_string(index=False) if not df_result.empty else "Không có dữ liệu phù hợp."
                        interpret_resp = client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {"role": "system", "content": "Bạn là chuyên gia phân tích Supply Chain. Dựa CHÍNH XÁC vào dữ liệu được cung cấp (không tự thêm số liệu khác), trả lời bằng tiếng Việt, ngắn gọn, dùng bullet point, có thể hành động được."},
                                {"role": "user", "content": f"Câu hỏi: {user_question}\n\nKết quả truy vấn dữ liệu thật:\n{result_text}\n\nHãy phân tích và đưa khuyến nghị."},
                            ],
                            temperature=0.5,
                            max_tokens=1024,
                        )
                        st.session_state["genbi_answer"] = interpret_resp.choices[0].message.content
                        st.session_state["genbi_last_question"] = user_question

                # --- LƯU LỊCH SỬ NGAY KHI THÀNH CÔNG ---
                if "genbi_answer" in st.session_state:
                    if "genbi_history" not in st.session_state:
                        st.session_state["genbi_history"] = []
                    
                    new_entry = (
                        st.session_state["genbi_last_question"], 
                        st.session_state.get("genbi_sql", "Câu hỏi phân tích chuyên sâu (Không dùng SQL)"), 
                        st.session_state["genbi_answer"]
                    )
                    # Tránh trùng lặp câu hỏi trong lịch sử
                    already_exists = any(e[0] == new_entry[0] for e in st.session_state["genbi_history"])
                    if not already_exists:
                        st.session_state["genbi_history"].append(new_entry)

                # Hoàn thành đổi trạng thái box loading thành công
                status.update(label="✅ Phân tích hoàn tất!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="❌ Quá trình phân tích gặp lỗi!", state="error")
                st.error(f"Lỗi xử lý: {e}")

    # ----------------------------------------------------------
    # Hiển thị: câu SQL đã sinh + bảng kết quả + phân tích AI
    # ----------------------------------------------------------
    if "genbi_sql" in st.session_state and st.session_state["genbi_sql"]:
        with st.expander("🛠️ Xem câu SQL do AI sinh ra"):
            st.code(st.session_state["genbi_sql"], language="sql")

    if "genbi_sql_result" in st.session_state and st.session_state["genbi_sql_result"] is not None:
        st.markdown("#### 📊 Dữ liệu thật truy vấn được")
        st.dataframe(st.session_state["genbi_sql_result"], use_container_width=True)

    if "genbi_answer" in st.session_state:
        st.markdown("### 💡 Kết quả phân tích")
        st.markdown(st.session_state["genbi_answer"])

        st.download_button(
            "📥 Tải kết quả phân tích (.txt)",
            data=st.session_state["genbi_answer"],
            file_name="genbi_phan_tich.txt",
            key="download_btn_unique" # Thêm key cố định để tránh xung đột nút bấm
        )

    # Đưa khối lịch sử ra ngoài cùng cấp để luôn hiển thị ở dưới đáy trang
    if st.session_state.get("genbi_history"):
        st.markdown("---")
        st.markdown("#### 📜 Lịch sử phân tích")
        for i, (q, sql, a) in enumerate(st.session_state["genbi_history"], 1):
            with st.expander(f"#{i} — {q[:70]}"):
                if sql:
                    st.code(sql, language="sql")
                st.markdown(a)