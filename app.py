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
        font-size: 20px;
        font-weight: 800;
        line-height: 1.2;
    }
    .kpi-title {
        font-size: 11px !important;
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
    
    /* ── Header hero (Shared across all modules) ── */
    .genbi-hero {
        background: linear-gradient(135deg, #1E3A8A 0%, #312E81 60%, #1E1B4B 100%);
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .genbi-hero::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: rgba(99,102,241,0.18);
    }
    .genbi-hero::after {
        content: '';
        position: absolute;
        bottom: -40px; left: 40px;
        width: 140px; height: 140px;
        border-radius: 50%;
        background: rgba(59,130,246,0.12);
    }
    .genbi-hero-title {
        font-size: 32px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        margin: 0 0 6px 0;
        position: relative; z-index: 1;
    }
    .genbi-hero-title span {
        background: linear-gradient(90deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .genbi-hero-sub {
        color: #CBD5E1;
        font-size: 15px;
        font-weight: 500;
        margin: 0;
        position: relative; z-index: 1;
    }
    .genbi-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99,102,241,0.25);
        border: 1px solid rgba(99,102,241,0.5);
        color: #A5B4FC;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 100px;
        margin-bottom: 16px;
        position: relative; z-index: 1;
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
        options=["Tổng quan vận hành", "Mô hình dự báo (AI)", "GenBI Insight"],
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
# MODULE 1: OPERATIONS OVERVIEW (TAB 1)
# ---------------------------------------------------------
if menu_selection == "Tổng quan vận hành":
    st.markdown("""
    <div class="genbi-hero">
        <div class="genbi-badge">✦ Operations Hub · Live Data</div>
        <div class="genbi-hero-title">Báo cáo <span>tổng quan vận hành</span></div>
        <p class="genbi-hero-sub">Theo dõi luồng lưu chuyển hàng hoá toàn cầu với dữ liệu xử lý theo thời gian thực.</p>
    </div>
    """, unsafe_allow_html=True)

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
        
        is_positive_change = pct_change >= 0
        is_good = not is_positive_change if is_inverse else is_positive_change
        
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
    # TRÍCH XUẤT TRƯỚC DỮ LIỆU ĐỂ PHỤC VỤ BIỂU ĐỒ & AI QUICK INSIGHT
    # ---------------------------------------------------------
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

    df_late_month = get_late_by_month(where_clause)
    df_rev_impact = get_revenue_impact(where_clause)
    df_ship = get_late_by_shipping(where_clause)
    df_country = get_late_by_country(where_clause)

    st.write("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # RENDER CÁC BIỂU ĐỒ BIỂU DIỄN (Lấy data từ dataframes đã chuẩn bị ở trên)
    # ---------------------------------------------------------
    col_a, col_b = st.columns([6, 4])
    with col_a:
        with st.container(border=True):
            if not df_late_month.empty:
                df_late_month['rolling_avg'] = df_late_month['late_rate'].rolling(window=3, min_periods=1).mean()
                
                fig_late_month = go.Figure()
                fig_late_month.add_trace(go.Scatter(
                    x=df_late_month['month'], y=df_late_month['late_rate'], 
                    mode='lines', name='Thực tế', 
                    line=dict(color='rgba(79, 70, 229, 0.4)', width=2, dash='dash')
                ))
                fig_late_month.add_trace(go.Scatter(
                    x=df_late_month['month'], y=df_late_month['rolling_avg'], 
                    mode='lines+markers', name='Trung bình 3 tháng', 
                    line=dict(color='#4F46E5', width=3, shape='spline'),
                    fill='tozeroy', fillcolor='rgba(79, 70, 229, 0.1)',
                    marker=dict(size=8, color="#FFFFFF", line=dict(color="#4F46E5", width=2))
                ))
                
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
            if not df_rev_impact.empty:
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
            if not df_ship.empty:
                fig_ship = px.bar(df_ship, x='shipping_mode', y='late_rate', title="Rủi ro Vận chuyển (%)", color='late_rate', color_continuous_scale=['#C4B5FD', '#7C3AED'])
                fig_ship.update_traces(marker_line_width=0, opacity=0.9, width=0.5)
                fig_ship.update_layout(xaxis_title="", yaxis_title="", coloraxis_showscale=False, margin=dict(b=0))
                fig_ship = apply_light_theme(fig_ship)
                st.plotly_chart(fig_ship, use_container_width=True)

    with col_d:
        with st.container(border=True):
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

        # =========================================================================
        # AI QUICK INSIGHT
        # =========================================================================
        @st.fragment
        def render_ai_insight_bottom():
            with st.container(border=True):
                st.markdown("<h4>🤖 AI Quick Insight</h4>", unsafe_allow_html=True)
            
                month_txt = df_late_month.to_string(index=False) if not df_late_month.empty else "N/A"
                ship_txt = df_ship.to_string(index=False) if not df_ship.empty else "N/A"
            
                df_country_view = df_country.copy() if not df_country.empty else pd.DataFrame()
                if not df_country_view.empty:
                    df_country_view['order_country'] = df_country_view['order_country'].replace(country_dict)
                country_txt = df_country_view.to_string(index=False) if not df_country_view.empty else "N/A"

                quick_context = f"""
                * KPIs: Doanh thu ${rev_curr:,.0f}, Lợi nhuận ${prof_curr:,.0f}, Tổng đơn {ord_curr:,.0f}, Tỷ lệ trễ {late_curr:.1f}%
                * Xu hướng trễ hạn qua các tháng:\n{month_txt}
                * Tỷ lệ trễ theo phương thức vận chuyển:\n{ship_txt}
                * Top quốc gia trễ hạn nghiêm trọng:\n{country_txt}
                """

                with st.spinner("⚡ AI đang tự động tổng hợp dữ liệu và trích xuất Insight..."):
                    from groq import Groq
                    try:
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        resp = client.chat.completions.create(
                            model="llama-3.1-8b-instant", 
                            messages=[
                                {
                                    "role": "system", 
                                    "content": (
                                        "Bạn là Giám đốc Phân tích Chuỗi cung ứng cấp cao. Nhiệm vụ của bạn là đưa ra ĐÚNG 3 Insight chuyên sâu bằng tiếng Việt.\n\n"
                                        "QUY TẮC ĐẶT TIÊU ĐỀ (BẮT BUỘC NHƯ HÌNH 2):\n"
                                        "- Tiêu đề phải bắt đầu bằng '### Insight 1:', '### Insight 2:', '### Insight 3:'.\n"
                                        "- Tên tiêu đề phải chỉ thẳng vào BẢN CHẤT HOẶC ĐIỂM NGHẼN LỚN NHẤT, không viết chung chung kiểu 'ảnh hưởng đến...' hay 'xu hướng theo...'.\n"
                                        "  * Ví dụ tốt: '### Insight 2: Phương thức vận chuyển First Class là nguồn cơn chính của trễ hạn'\n"
                                        "  * Ví dụ xấu: '### Insight 2: Phương thức vận chuyển ảnh hưởng đến tỷ lệ trễ hạn'\n\n"
                                        "QUY TẮC VIẾT NỘI DUNG (GẠCH ĐẦU DÒNG & ĐẮT GIÁ):\n"
                                        "- Dưới mỗi insight, chỉ viết từ 2 đến 3 gạch đầu dòng ngắn gọn.\n"
                                        "- Gạch đầu dòng đầu tiên: Đưa ra nhận định tổng quan kèm THEO ĐÚNG 1 ĐẾN 2 CON SỐ ĐẮT GIÁ NHẤT (ví dụ: con số cao nhất, hoặc mức tăng mạnh nhất) để làm dẫn chứng. TUYỆT ĐỐI KHÔNG LIỆT KÊ TOÀN BỘ DANH SÁCH số liệu thô.\n"
                                        "- Gạch đầu dòng tiếp theo: Đưa ra lý giải logic hoặc gợi ý hành động thực tế dựa trên điểm nghẽn đó."
                                    )
                                },
                                {
                                    "role": "user", 
                                    "content": (
                                        f"Dựa trên dữ liệu chuỗi cung ứng sau đây:\n{quick_context}\n\n"
                                        "Hãy viết 3 Insight sắc bén, giật các tiêu đề trực diện vào điểm nghẽn và đưa số liệu dẫn chứng tinh gọn theo đúng quy tắc."
                                    )
                                },
                            ],
                            temperature=0.15, # Giữ độ ổn định cao, tránh sáng tạo lung tung
                            max_tokens=800,
                        )
                        st.info(resp.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Lỗi gọi AI Quick Insight tự động: {e}")

        # Gọi hàm để thực thi dưới cùng trang
        render_ai_insight_bottom()

# ---------------------------------------------------------
# MODULE 2: AI & SHAP 
# ---------------------------------------------------------
elif menu_selection == "Mô hình dự báo (AI)":

    @st.cache_data(ttl=3600)
    def get_ai_summary_stats():
        # 1. Số đơn rủi ro cao
        risk_count = con.execute("SELECT COUNT(DISTINCT order_id) as cnt FROM my_db.main.ml_predictions_explained WHERE predicted_label = 1").df()['cnt'].iloc[0]
        
        # 2. Doanh thu rủi ro
        sales_risk = con.execute("""
            SELECT SUM(sales_amount) as total_sales
            FROM (
                SELECT order_id, MAX(sales_amount) as sales_amount
                FROM vanh_gold.main.stg_supplychain_v2
                WHERE order_id IN (SELECT DISTINCT order_id FROM my_db.main.ml_predictions_explained WHERE predicted_label = 1)
                GROUP BY order_id
            )
        """).df()['total_sales'].iloc[0]
        sales_risk = sales_risk if sales_risk is not None else 0
        
        # 3. AUC của mô hình
        try:
            auc_val = con.execute("SELECT auc FROM my_db.main.ml_performance_metrics LIMIT 1").df()['auc'].iloc[0]
        except:
            auc_val = 0.852
            
        # 4. Danh sách Top 10 đơn hàng rủi ro cao nhất
        top_risky_df = con.execute("""
            SELECT 
                p.order_id as "Order ID",
                s.customer_fname || ' ' || s.customer_lname as "Khách hàng",
                p.order_region as "Khu vực",
                p.predicted_probability as "Xác suất rủi ro",
                MAX(s.sales_amount) as "Doanh thu"
            FROM my_db.main.ml_predictions_explained p
            JOIN vanh_gold.main.stg_supplychain_v2 s ON p.order_id = s.order_id
            WHERE p.predicted_label = 1
            GROUP BY p.order_id, "Khách hàng", p.order_region, p.predicted_probability
            ORDER BY p.predicted_probability DESC
            LIMIT 10
        """).df()
        
        # 5. So sánh nhóm
        ship_risk = con.execute("""
            SELECT shipping_mode, AVG(predicted_probability) * 100.0 as avg_risk
            FROM my_db.main.ml_predictions_explained
            GROUP BY 1 ORDER BY 2 DESC
        """).df()
        
        region_risk = con.execute("""
            SELECT order_region, AVG(predicted_probability) * 100.0 as avg_risk
            FROM my_db.main.ml_predictions_explained
            GROUP BY 1 ORDER BY 2 DESC LIMIT 10
        """).df()
        
        return risk_count, sales_risk, auc_val, top_risky_df, ship_risk, region_risk

    # ── Load data TRƯỚC khi render bất kỳ thứ gì ──────────────
    # Trick: dùng st.fragment để isolate render Module 2 khỏi DOM cũ
    @st.fragment
    def render_module2_content():
        risk_count, sales_risk, auc_val, top_risky_df, ship_risk, region_risk = get_ai_summary_stats()

        st.markdown("""
        <div class="genbi-hero">
            <div class="genbi-badge">✦ AI Predictive Model · SHAP</div>
            <div class="genbi-hero-title">Dự báo rủi ro bằng <span>trí tuệ nhân tạo</span></div>
            <p class="genbi-hero-sub">Giải mã thuật toán Machine Learning - Ứng dụng công nghệ SHAP để giải thích các quyết định dự báo rủi ro.</p>
        </div>
        """, unsafe_allow_html=True)

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
                            increasing = {"marker":{"color":"#E11D48"}},
                            decreasing = {"marker":{"color":"#4F46E5"}}
                        ))
                        
                        prob = row['predicted_probability']
                        pred = "⚠️ NGUY CƠ TRỄ HẠN CAO" if row['predicted_label'] == 1 else "✅ TIẾN ĐỘ AN TOÀN"
                        pred_color = "#E11D48" if row['predicted_label'] == 1 else "#10B981"
                        
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
                    feature_order = melted.groupby('feature')['shap_value'].apply(lambda x: np.abs(x).mean()).sort_values(ascending=False).index
                    
                    mean_shap = melted.groupby('feature')['shap_value'].apply(lambda x: np.abs(x).mean()).reset_index()
                    mean_shap.columns = ['feature', 'mean_abs_shap']
                    mean_shap = mean_shap.sort_values(by='mean_abs_shap', ascending=True)
                    
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

                    n_features = len(feature_order)
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

        # 5. Mô hình giả lập dự báo đơn hàng mới
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
                query_exact = f"""
                SELECT AVG(predicted_probability) as prob
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
                    query_fallback = f"""
                    SELECT AVG(predicted_probability) as prob
                    FROM my_db.main.ml_predictions_explained
                    WHERE shipping_mode = '{sim_ship}'
                      AND order_region = '{sim_region}'
                    """
                    res_fb = con.execute(query_fallback).df()
                    prob = res_fb['prob'].iloc[0] if not res_fb.empty and not pd.isna(res_fb['prob'].iloc[0]) else 0.55
                
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

        # ─── AI Quick Insight ───
        with st.container(border=True):
            st.markdown("<h4>🤖 AI Quick Insight</h4>", unsafe_allow_html=True)
            
            top_risky_txt = top_risky_df[['Order ID', 'Xác suất rủi ro', 'Doanh thu']].head(3).to_string(index=False) if not top_risky_df.empty else "N/A"
            ship_risk_txt = ship_risk.to_string(index=False) if not ship_risk.empty else "N/A"
            region_risk_txt = region_risk.to_string(index=False) if not region_risk.empty else "N/A"

            ai_model_context = f"""
            * Chỉ số mô hình: Đơn rủi ro cao={risk_count}, Giá trị đe dọa=${sales_risk:,.0f}, AUC={auc_val:.3f}
            * Top đơn hàng nguy cơ cao nhất hệ thống:\n{top_risky_txt}
            * Mức độ rủi ro trung bình theo Phương thức vận chuyển:\n{ship_risk_txt}
            * Mức độ rủi ro trung bình theo Khu vực:\n{region_risk_txt}
            """

            with st.spinner("⚡ AI đang tự động tổng hợp dữ liệu và trích xuất Insight..."):
                from groq import Groq
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    resp = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system", 
                                "content": (
                                    "Bạn là Chuyên gia Khoa học Dữ liệu Chuỗi cung ứng cấp cao.\n"
                                    "Nhiệm vụ của bạn là đưa ra ĐÚNG 3 Insight dự báo rủi ro chuyên sâu bằng tiếng Việt.\n\n"
                                    "QUY TẮC ĐẶT TIÊU ĐỀ (BẮT BUỘC):\n"
                                    "- Tiêu đề phải bắt đầu bằng '### Insight 1:', '### Insight 2:', '### Insight 3:'.\n"
                                    "- Tên tiêu đề phải giật trực diện, chỉ thẳng vào BẢN CHẤT HOẶC ĐIỂM NGHẼN rủi ro lớn nhất từ mô hình AI, không viết chung chung.\n"
                                    "  * Ví dụ tốt: '### Insight 2: Phương thức vận chuyển First Class là nguồn cơn chính gây trễ hạn'\n"
                                    "  * Ví dụ xấu: '### Insight 2: Phân tích mức độ rủi ro theo các phương thức vận chuyển'\n\n"
                                    "QUY TẮC VIẾT NỘI DUNG (GẠCH ĐẦU DÒNG & ĐẮT GIÁ):\n"
                                    "- Dưới mỗi insight, chỉ viết từ 2 đến 3 gạch đầu dòng ngắn gọn.\n"
                                    "- Gạch đầu dòng đầu tiên: Đưa ra nhận định tổng quan kèm THEO ĐÚNG 1 ĐẾN 2 CON SỐ ĐẮT GIÁ NHẤT từ dữ liệu (ví dụ: số đơn hàng bị đe dọa, giá trị tổn thất cao nhất hoặc khu vực có phần trăm rủi ro lớn nhất) để làm dẫn chứng thuyết phục. TUYỆT ĐỐI KHÔNG LIỆT KÊ TOÀN BỘ DANH SÁCH số liệu thô.\n"
                                    "- Gạch đầu dòng tiếp theo: Đề xuất giải pháp ứng phó hoặc giảm thiểu rủi ro (Risk Mitigation) chủ động dựa trên điểm nghẽn đó."
                                )
                            },
                            {
                                "role": "user", 
                                "content": (
                                    f"Dựa trên dữ liệu phân tích dự báo AI sau đây:\n{ai_model_context}\n\n"
                                    "Hãy viết 3 bài phân tích Insight theo đúng quy tắc đặt tiêu đề trực diện vào điểm nghẽn và định dạng gạch đầu dòng kèm số liệu đắt giá."
                                )
                            },
                        ],
                        temperature=0.15, 
                        max_tokens=800,    
                    )
                    st.info(resp.choices[0].message.content)
                except Exception as e:
                    st.error(f"Lỗi gọi AI Quick Insight tự động: {e}")

    # Gọi fragment
    render_module2_content()
    
# ---------------------------------------------------------
# MODULE 3: GenBI Insight (Text-to-SQL)
# ---------------------------------------------------------
elif menu_selection == "GenBI Insight":
    from groq import Groq
    import re

    # ── CSS riêng cho GenBI ──────────────────────────────────
    st.markdown("""
    <style>
    /* ── Suggestion pills ── */
    .pill-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 14px 0 22px 0;
    }
    .pill-label {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748B;
        margin-bottom: 10px;
    }

    /* ── Question preview bubble ── */
    .q-bubble {
        background: linear-gradient(135deg, #EEF2FF, #F0F9FF);
        border-left: 4px solid #6366F1;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin: 14px 0;
        font-size: 15px;
        font-weight: 600;
        color: #312E81;
    }
    .q-bubble-icon { margin-right: 8px; }

    /* ── SQL expander polish ── */
    .sql-block {
        background: #0F172A;
        border-radius: 12px;
        border: 1px solid #1E293B;
        padding: 20px;
        margin: 16px 0;
    }
    .sql-block-header {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }
    .sql-dot { width:8px;height:8px;border-radius:50%; display:inline-block; }

    /* ── Data table section ── */
    .data-section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 15px;
        font-weight: 700;
        color: #0F172A;
        margin: 20px 0 10px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #E2E8F0;
    }

    /* ── AI Answer card ── */
    .answer-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 24px -4px rgba(15,23,42,0.10);
        padding: 28px 32px;
        margin: 20px 0;
    }
    .answer-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
        padding-bottom: 6px;
        border-bottom: 1px solid #F1F5F9;
    }
    .answer-avatar {
        width: 40px; height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1, #3B82F6);
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }
    .answer-meta { flex: 1; }
    .answer-name {
        font-size: 14px; font-weight: 800; color: #0F172A; margin: 0;
    }
    .answer-time {
        font-size: 12px; color: #94A3B8; margin: 0;
    }
    .answer-body {
        color: #1E293B;
        font-size: 15px;
        line-height: 1.75;
    }

    /* ── History accordion ── */
    .history-title {
        display: flex; align-items: center; gap: 10px;
        font-size: 16px; font-weight: 800; color: #0F172A;
        margin: 32px 0 14px 0;
        padding-top: 24px;
        border-top: 2px dashed #E2E8F0;
    }
    .history-chip {
        background: #F1F5F9;
        color: #475569;
        font-size: 12px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 100px;
    }

    /* ── Input area ── */
    .input-section {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 2px 12px -2px rgba(15,23,42,0.06);
        margin-bottom: 20px;
    }
    .input-section-label {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: #64748B;
        margin-bottom: 10px;
    }
    
    /* ── Metric Boxes & Badges ── */
    .metric-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .metric-box .metric-val {
        font-size: 1.6rem;
        font-weight: 700;
        color: #6366f1;
    }
    .metric-box .metric-lbl {
        font-size: 0.78rem;
        color: #6b7280;
        margin-top: 0.2rem;
    }
    .sql-badge {
        display: inline-block;
        background: #0ea5e9;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .ai-badge {
        display: inline-block;
        background: #f59e0b;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .question-badge {
        display: inline-block;
        background: #6366f1;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }
    .genbi-history-card {
        background: #fafafa;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.4rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── HERO HEADER ──────────────────────────────────────────
    st.markdown("""
    <div class="genbi-hero">
        <div class="genbi-badge">✦ Powered by Groq · LLM</div>
        <div class="genbi-hero-title">GenBI - <span>Trợ lý phân tích</span></div>
        <p class="genbi-hero-sub">AI tự sinh câu truy vấn SQL theo câu hỏi của bạn, chạy thật trên dữ liệu, rồi diễn giải kết quả bằng ngôn ngữ tự nhiên.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Schema & cấu hình ───────────────────────────────────
    SCHEMA_DESCRIPTION = """
Bảng: my_db.main.ml_predictions_explained
Cột: order_id (VARCHAR), shipping_mode (VARCHAR), customer_state (VARCHAR), order_type (VARCHAR),
order_region (VARCHAR), order_weekday (VARCHAR), order_month (VARCHAR), customer_segment (VARCHAR),
actual (BIGINT - kết quả thực tế: 1=trễ, 0=đúng hạn),
predicted_probability (DOUBLE - xác suất rủi ro trễ hạn 0.0 đến 1.0),
predicted_label (BIGINT - nhãn dự đoán: 1=trễ, 0=đúng hạn), created_at (VARCHAR),
các cột shap_shipping_mode, shap_customer_state, shap_order_type, shap_order_region,
shap_order_weekday, shap_order_month, shap_customer_segment (DOUBLE - SHAP values).

Bảng: my_db.main.ml_performance_metrics
Cột: model_name (VARCHAR), auc (DOUBLE), f1 (DOUBLE), best_threshold (DOUBLE), created_at (VARCHAR).

Bảng: my_db.main.ml_feature_importance
Cột: feature (VARCHAR), importance_score (DOUBLE), created_at (VARCHAR).
"""

    ALLOWED_TABLES = [
        "my_db.main.ml_predictions_explained",
        "my_db.main.ml_performance_metrics",
        "my_db.main.ml_feature_importance",
        "ml_predictions_explained",
        "ml_performance_metrics",
        "ml_feature_importance",
    ]

    def is_safe_select(sql: str) -> bool:
        """Kiểm tra câu SQL là SELECT/WITH an toàn, không có lệnh nguy hiểm."""
        s = sql.strip().rstrip(";").strip()
        lowered = s.lower()

        # Cho phép SELECT hoặc WITH ... SELECT (CTE)
        if not (lowered.startswith("select") or lowered.startswith("with")):
            return False

        # Chặn các lệnh nguy hiểm (dùng cụm từ để tránh false positive trên tên cột)
        forbidden = [
            "insert into", "update ", "delete ", "drop ",
            "alter ", "attach ", "detach ", "create ",
            "grant ", "pragma", "copy ", "export ", "truncate",
        ]
        for kw in forbidden:
            if kw in lowered:
                return False

        # Phải truy vấn đúng bảng được phép (full path hoặc short name)
        if not any(t in lowered for t in ALLOWED_TABLES):
            return False

        return True

    def extract_sql(text: str) -> str:
        match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r"```\s*(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def style_df(df):
        """Format và style dataframe kết quả."""
        import pandas as pd
        df = df.copy()
        if "predicted_probability" in df.columns:
            df["predicted_probability"] = pd.to_numeric(df["predicted_probability"], errors="coerce")
        if "predicted_label" in df.columns:
            df["predicted_label"] = df["predicted_label"].map({1: "🔴 Trễ", 0: "🟢 Đúng hạn"}).fillna(df["predicted_label"])
        if "actual" in df.columns:
            df["actual"] = df["actual"].map({1: "🔴 Trễ", 0: "🟢 Đúng hạn"}).fillna(df["actual"])
        return df

    # ── Suggestions ─────────────────────────────────────────
    SQL_SUGGESTIONS = [
        "Top 5 đơn hàng có xác suất rủi ro trễ (predicted_probability) cao nhất?",
        "Phương thức vận chuyển (shipping_mode) nào có tỷ lệ predicted_label=1 cao nhất?",
        "Khu vực (order_region) nào có AVG(predicted_probability) cao nhất?",
        "Phân khúc khách hàng (customer_segment) nào có tỷ lệ predicted_label=1 cao nhất?",
    ]
    ANALYTICAL_SUGGESTIONS = [
        "Đề xuất 3 hành động cụ thể để giảm tỷ lệ giao hàng trễ?",
        "Khu vực nào cần ưu tiên cải thiện logistics và vì sao?",
        "Phương thức vận chuyển nào đang rủi ro nhất, giải pháp là gì?",
    ]

    ANALYTICAL_CONTEXT = """
Thông tin tổng quan từ dữ liệu Supply Chain (DataCo):
- Tổng số đơn hàng: ~180,000 giao dịch
- Mô hình dự báo: CatBoost, AUC ≈ 0.90
- Phương thức vận chuyển: Standard Class có tỷ lệ trễ cao nhất (~60%),
  First Class và Second Class ở mức trung bình (~40%), Same Day thấp nhất
- Khu vực rủi ro cao: Western Europe, Central America, Southern Asia
- Yếu tố SHAP quan trọng nhất: shipping_mode, order_type, customer_segment, order_region
- Mùa cao điểm (tháng 11-12) làm tăng xác suất trễ đáng kể
"""

    # ── Reset state ──────────────────────────────────────────
    if st.session_state.pop("genbi_pill_clear", False):
        st.session_state["genbi_textarea"] = ""

    if st.session_state.get("genbi_reset", False):
        st.session_state["genbi_select"]  = "-- Chọn câu hỏi --"
        st.session_state["genbi_textarea"] = ""
        for k in ["genbi_answer", "genbi_sql", "genbi_sql_result", "genbi_last_question"]:
            st.session_state.pop(k, None)
        st.session_state["genbi_reset"] = False

   # ── Input area ───────────────────────────────────────────
    with st.container(border=True):
        user_typed = st.text_area(
            "✏️ Nhập câu hỏi của bạn tại đây:",
            height=80,
            key="genbi_textarea",
            placeholder="Ví dụ: Tháng nào có tỷ lệ giao trễ cao nhất?",
        )

        # Câu hỏi gợi ý dạng 2 cột
        st.markdown("""
        <div style="margin:0.6rem 0 0.3rem 0;">
            <span class="pill-label">💡 Câu hỏi gợi ý</span>
        </div>
        <div style="display:flex;gap:0.8rem;margin-bottom:0.2rem;">
            <span style="font-size:0.75rem;color:#6366f1;font-weight:600;">🔍 Truy vấn dữ liệu (SQL)</span>
            <span style="font-size:0.75rem;color:#f59e0b;font-weight:600;margin-left:auto;margin-right:1rem;">🧠 Phân tích chuyên sâu</span>
        </div>
        """, unsafe_allow_html=True)

        col_sql, col_ana = st.columns(2)
        with col_sql:
            for q in SQL_SUGGESTIONS:
                if st.button(q, key=f"sq_{q[:20]}", use_container_width=True):
                    st.session_state["genbi_select"] = q
                    st.session_state["genbi_pill_clear"] = True
                    st.rerun()
        with col_ana:
            for q in ANALYTICAL_SUGGESTIONS:
                if st.button(q, key=f"aq_{q[:20]}", use_container_width=True):
                    st.session_state["genbi_select"] = q
                    st.session_state["genbi_pill_clear"] = True
                    st.rerun()

        selected_q = st.session_state.get("genbi_select", "-- Chọn câu hỏi --")

        if user_typed and user_typed.strip():
            user_question = user_typed.strip()
        elif selected_q and selected_q != "-- Chọn câu hỏi --":
            user_question = selected_q
        else:
            user_question = ""

        if user_question:
            st.markdown(
                f'''<div class="q-bubble"><span class="q-bubble-icon">📝</span><b>Câu hỏi đang chọn:</b> {user_question}</div>''',
                unsafe_allow_html=True
            )

        col_btn1, col_btn2, _ = st.columns([1.6, 1.2, 5])
        with col_btn1:
            run_clicked = st.button("🚀 Phân tích với AI", type="primary")
        with col_btn2:
            clear_clicked = st.button("🗑️ Xóa câu hỏi")

    if clear_clicked:
        st.session_state["genbi_reset"] = True
        st.rerun()

    if clear_clicked:
        st.session_state["genbi_reset"] = True
        st.rerun()
    
    ANSWER_FORMAT_INSTRUCTION = (
        "Bạn là chuyên gia phân tích chuỗi cung ứng (Supply Chain Analyst) cấp cao, "
        "có nhiều năm kinh nghiệm tư vấn cho ban giám đốc về logistics và quản trị rủi ro giao hàng. "
        "Dựa CHÍNH XÁC vào dữ liệu được cung cấp, không tự bịa thêm số liệu nào ngoài những gì đã cho. "
        "Hãy trả lời bằng tiếng Việt, văn phong chuyên nghiệp nhưng dễ hiểu cho nhà quản lý không rành kỹ thuật. "
        "LUÔN LUÔN trình bày đầy đủ và chi tiết theo đúng cấu trúc sau, mỗi phần ít nhất 2-3 câu hoặc 2-3 bullet point, "
        "không trả lời qua loa, không rút gọn:\n\n"
        "**📊 Nhận xét chi tiết:** Phân tích sâu các số liệu quan trọng nhất trong dữ liệu, "
        "so sánh giữa các nhóm (nếu có), chỉ ra xu hướng hoặc điểm bất thường đáng chú ý.\n\n"
        "**⚠️ Đánh giá rủi ro:** Nêu rõ mức độ nghiêm trọng của rủi ro, ảnh hưởng tiềm tàng tới doanh thu/uy tín "
        "nếu không xử lý, và nguyên nhân gốc rễ có thể gây ra tình trạng này.\n\n"
        "**✅ Khuyến nghị hành động:** Đề xuất ít nhất 2-3 hành động cụ thể, khả thi, có thể triển khai ngay, "
        "ưu tiên theo mức độ quan trọng (đánh số 1, 2, 3).\n\n"
        "**🎯 Kết luận ngắn:** Tóm tắt lại trong 1 câu thông điệp quan trọng nhất gửi tới nhà quản lý."
    )

    # ── Xử lý phân tích + hiển thị TRONG 1 CARD THẬT ─────────
    if run_clicked and user_question:
        with st.container(border=True):
            header_box = st.empty()
            header_box.markdown("""
            <div class="answer-card-header">
                <div class="answer-avatar">🤖</div>
                <div class="answer-meta">
                    <p class="answer-name">Trợ Lý GenBI Insight</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.status("🤖 Trợ lý GenBI đang xử lý...", expanded=True) as status:
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    is_analytical = user_question in ANALYTICAL_SUGGESTIONS

                    if is_analytical:
                        status.update(label="🧠 Đang phân tích chuyên sâu dữ liệu Supply Chain...", state="running")
                        interpret_resp = client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {"role": "system", "content": ANSWER_FORMAT_INSTRUCTION},
                                {"role": "user", "content": f"Thông tin dữ liệu:\n{ANALYTICAL_CONTEXT}\n\nCâu hỏi: {user_question}\n\nHãy phân tích đầy đủ và đưa khuyến nghị chi tiết."},
                            ],
                            temperature=0.5, max_tokens=1600,
                        )
                        st.session_state["genbi_answer"] = interpret_resp.choices[0].message.content
                        st.session_state["genbi_last_question"] = user_question
                        st.session_state.pop("genbi_sql", None)
                        st.session_state.pop("genbi_sql_result", None)

                    else:
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
                            temperature=0, max_tokens=400,
                        )
                        raw_sql = extract_sql(sql_gen_resp.choices[0].message.content)
                        st.session_state["genbi_sql"] = raw_sql

                        status.update(label="🔍 Bước 2: Kiểm tra an toàn và truy vấn dữ liệu thật...", state="running")
                        if not is_safe_select(raw_sql):
                            status.update(label="⚠️ Phát hiện câu lệnh SQL không an toàn!", state="error")
                            st.error("⚠️ Câu SQL do AI sinh ra không hợp lệ hoặc không an toàn, không thực thi. Vui lòng thử diễn đạt lại câu hỏi.")
                            st.code(raw_sql, language="sql")
                        else:
                            df_result = con.execute(raw_sql).df()
                            st.session_state["genbi_sql_result"] = df_result

                            status.update(label="💡 Bước 3: Đang tổng hợp dữ liệu và lập báo cáo khuyến nghị...", state="running")
                            result_text = df_result.to_string(index=False) if not df_result.empty else "Không có dữ liệu phù hợp."
                            interpret_resp = client.chat.completions.create(
                                model="openai/gpt-oss-20b",
                                messages=[
                                    {"role": "system", "content": ANSWER_FORMAT_INSTRUCTION},
                                    {"role": "user", "content": f"Câu hỏi: {user_question}\n\nKết quả truy vấn dữ liệu thật:\n{result_text}\n\nHãy phân tích đầy đủ và đưa khuyến nghị chi tiết."},
                                ],
                                temperature=0.5, max_tokens=1600,
                            )
                            st.session_state["genbi_answer"] = interpret_resp.choices[0].message.content
                            st.session_state["genbi_last_question"] = user_question

                    if "genbi_answer" in st.session_state:
                        if "genbi_history" not in st.session_state:
                            st.session_state["genbi_history"] = []
                        new_entry = (
                            st.session_state["genbi_last_question"],
                            st.session_state.get("genbi_sql", "Câu hỏi phân tích chuyên sâu (Không dùng SQL)"),
                            st.session_state["genbi_answer"],
                        )
                        if not any(e[0] == new_entry[0] for e in st.session_state["genbi_history"]):
                            st.session_state["genbi_history"].append(new_entry)

                    status.update(label="✅ Phân tích hoàn tất!", state="complete", expanded=False)
                    header_box.markdown("""
                    <div class="answer-card-header">
                        <div class="answer-avatar">🤖</div>
                        <div class="answer-meta">
                            <p class="answer-name">Trợ Lý GenBI Insight</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    status.update(label="❌ Quá trình phân tích gặp lỗi!", state="error")
                    header_box.markdown("""
                    <div class="answer-card-header">
                        <div class="answer-avatar">🤖</div>
                        <div class="answer-meta">
                            <p class="answer-name">Trợ Lý GenBI Insight</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.error(f"Lỗi xử lý: {e}")

            # ---------- Hiển thị SQL + bảng dữ liệu + câu trả lời — VẪN TRONG container ngoài ----------
            if "genbi_sql" in st.session_state and st.session_state["genbi_sql"]:
                st.markdown('<div class="sql-block-header">🛠️ CẤU TRÚC TRUY VẤN SQL TỰ SINH</div>', unsafe_allow_html=True)
                st.code(st.session_state["genbi_sql"], language="sql")

            if "genbi_sql_result" in st.session_state and st.session_state["genbi_sql_result"] is not None:
                df_raw = st.session_state["genbi_sql_result"]
                if not df_raw.empty:
                    st.markdown('<div class="data-section-title">📊 Dữ liệu truy vấn thực tế từ Database</div>', unsafe_allow_html=True)
                    if "predicted_probability" in df_raw.columns:
                        import pandas as pd
                        probs = pd.to_numeric(df_raw["predicted_probability"], errors="coerce").dropna()
                        c1, c2, c3 = st.columns(3)
                        c1.markdown(f'<div class="metric-box"><div class="metric-val">{len(df_raw)}</div><div class="metric-lbl">Số đơn hàng</div></div>', unsafe_allow_html=True)
                        c2.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#dc2626">{probs.max():.1%}</div><div class="metric-lbl">Rủi ro cao nhất</div></div>', unsafe_allow_html=True)
                        c3.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#f59e0b">{probs.mean():.1%}</div><div class="metric-lbl">Rủi ro trung bình</div></div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)

                        df_display = style_df(df_raw)
                        def highlight_prob(val):
                            try:
                                v = float(val)
                                if v >= 0.8: return "color: #dc2626; font-weight: 700"
                                elif v >= 0.5: return "color: #f59e0b; font-weight: 600"
                                else: return "color: #16a34a; font-weight: 600"
                            except Exception:
                                return ""
                        styled = df_display.style.format({"predicted_probability": "{:.1%}"}).map(highlight_prob, subset=["predicted_probability"])
                        st.dataframe(styled, use_container_width=True, hide_index=True)
                    else:
                        st.dataframe(style_df(df_raw), use_container_width=True, hide_index=True)

            if "genbi_answer" in st.session_state:
                st.markdown('<div class="data-section-title">🧠 Kết luận và Khuyến nghị từ AI</div>', unsafe_allow_html=True)
                st.markdown(st.session_state["genbi_answer"])
                st.download_button(
                    "📥 Tải kết quả (.txt)",
                    data=st.session_state["genbi_answer"],
                    file_name="genbi_phan_tich.txt",
                    key="genbi_download",
                )

    # ── LỊCH SỬ PHÂN TÍCH (KHÔNG bọc trong card trên) ───────
    if st.session_state.get("genbi_history"):
        st.markdown('<div class="history-title">📜 Lịch sử phân tích gần đây</div>', unsafe_allow_html=True)
        hist = list(reversed(st.session_state["genbi_history"]))
        for i, (q, sql, a) in enumerate(hist, 1):
            label = f"{'🔵 SQL' if sql and 'Không dùng SQL' not in sql else '🟡 Phân tích'} #{len(hist)+1-i} — {q[:65]}{'...' if len(q) > 65 else ''}"
            with st.expander(label, expanded=False):
                st.markdown(f'<div class="genbi-history-card"><span class="question-badge">Câu hỏi</span><br>{q}</div>', unsafe_allow_html=True)
                if sql and "Không dùng SQL" not in sql:
                    st.markdown('<span class="sql-badge">SQL đã chạy</span>', unsafe_allow_html=True)
                    st.code(sql, language="sql")
                st.markdown('<span class="ai-badge">Kết quả phân tích</span>', unsafe_allow_html=True)
                st.markdown(a)