import streamlit as st
import duckdb
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Cấu hình trang - Phải luôn ở đầu
st.set_page_config(page_title="AI Supply Chain Hub", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

# CSS Cao cấp - Giao diện Sáng (Light Tech / SaaS) với tông Xanh Tím
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
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
        color: #64748B;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Thiết kế thẻ KPI bóng bẩy, hiện đại */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border: 1px solid #A78BFA !important;
        box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.15), 0 8px 10px -6px rgba(124, 58, 237, 0.1);
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
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Ẩn viền thừa của Streamlit */
    hr {
        border-color: #F1F5F9 !important;
    }
    
    /* Tinh chỉnh tiêu đề h4 bên trong các khối */
    h4 {
        color: #1E293B !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    
    /* Giao diện Dark Sidebar thủ công (không dùng secondaryBackgroundColor để tránh lỗi ô input) */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
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

# Token MotherDuck
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFuaHBwdjIzNDA2QHN0LnVlbC5lZHUudm4iLCJtZFJlZ2lvbiI6ImF3cy11cy1lYXN0LTEiLCJzZXNzaW9uIjoiYW5ocHB2MjM0MDYuc3QudWVsLmVkdS52biIsInBhdCI6IjVFZEVSNzlZZFpjN2FST1ROSkdTTUlPOHpqTkZfcWV3MzNUaks1bXRnQ3ciLCJ1c2VySWQiOiJkZTIzN2EzMS0yMTg5LTRkNWYtYmIwYS0zZjQ5MzgzOTExOTEiLCJpc3MiOiJtZF9wYXQiLCJyZWFkT25seSI6ZmFsc2UsInRva2VuVHlwZSI6InJlYWRfd3JpdGUiLCJpYXQiOjE3ODIzMTMzNzd9.7g-rGoWNcYNXUEGU5tileJWrBtnGXDlghTtiisqY_eg"

@st.cache_resource
def get_connection():
    return duckdb.connect(f"md:my_db?motherduck_token={TOKEN}")

con = get_connection()

# ---------------------------------------------------------
# CẤU HÌNH GIAO DIỆN CHUNG (LIGHT TECH THEME CHO PLOTLY)
# ---------------------------------------------------------
# Tone màu Công nghệ Xanh Tím: Xanh Blue, Tím Purple, Đỏ Hồng (Risk), Xanh Lục (Safe)
tech_colors = ["#4F46E5", "#7C3AED", "#2563EB", "#9333EA", "#3B82F6"]

def apply_light_theme(fig):
    fig.update_layout(
        font_family="'Plus Jakarta Sans', sans-serif",
        font_color="#475569",
        title_font_color="#0F172A",
        title_font_size=18,
        title_font_weight="bold",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=20, l=20, r=20),
        colorway=tech_colors
    )
    fig.update_xaxes(showgrid=False, linecolor="#E2E8F0")
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0")
    return fig

# ---------------------------------------------------------
# SIDEBAR NAVIGATION (HỌC HỎI STYLE TỪ ẢNH MẪU CỦA USER)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <div style="font-size: 50px; margin-bottom: 10px; background: linear-gradient(135deg, #2563EB, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🌐</div>
            <h2 style="color: #FFFFFF; font-weight: 800; margin: 0; font-size: 20px;">QUẢN TRỊ RỦI RO</h2>
            <p style="color: #94A3B8; font-size: 11px; font-weight: 700; letter-spacing: 1px;">CHUỖI CUNG ỨNG</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu học theo bố cục Sidebar trong hình mẫu (Icon bên trái, thanh viền trái khi chọn)
    menu_selection = option_menu(
        menu_title=None,
        options=["Tổng quan Vận hành", "Mô hình Dự báo (AI)"],
        icons=["grid-fill", "lightning-charge-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#0F172A"},
            "icon": {"color": "#94A3B8", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "14px", 
                "text-align": "left", 
                "margin":"5px 0px", 
                "color": "#94A3B8",
                "font-weight": "600",
                "border-radius": "0px",
                "padding-left": "20px",
                "transition": "0.2s"
            },
            "nav-link-selected": {
                "background-color": "#0F172A", 
                "color": "#FFFFFF", 
                "font-weight": "800",
                "border-left": "4px solid #4F46E5"
            },
        }
    )
    
    st.write("---")
    
    st.markdown("<h4 style='color: white; font-size: 14px; margin-bottom: 10px;'>BỘ LỌC TOÀN CỤC</h4>", unsafe_allow_html=True)
    
    @st.cache_data(ttl=3600)
    def get_filter_options():
        years = con.execute("SELECT DISTINCT order_year FROM my_db.main.dim_time ORDER BY 1 DESC").df()['order_year'].tolist()
        regions = con.execute("SELECT DISTINCT order_region FROM my_db.main.stg_supplychain_v2 ORDER BY 1").df()['order_region'].tolist()
        shipping_modes = con.execute("SELECT DISTINCT shipping_mode FROM my_db.main.fact_orders ORDER BY 1").df()['shipping_mode'].tolist()
        return years, regions, shipping_modes

    years_list, regions_list, shipping_modes_list = get_filter_options()
    
    # Year filter (Cho phép chọn 'Tất cả')
    selected_year = st.selectbox("Năm", ["Tất cả"] + [str(y) for y in years_list])
    # Region filter
    selected_region = st.selectbox("Khu vực", ["Tất cả"] + regions_list)
    # Shipping Mode filter
    selected_shipping = st.selectbox("Phương thức Vận chuyển", ["Tất cả"] + shipping_modes_list)
    
    st.write("---")
    st.markdown("<p style='font-size:12px; color:#64748B; padding-left:20px;'>☁️ CONNECTED TO <b>MOTHERDUCK</b><br>⚡ REAL-TIME SYNC</p>", unsafe_allow_html=True)

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
        FROM my_db.main.stg_supplychain_v2
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
            FROM my_db.main.stg_supplychain_v2
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
                FROM my_db.main.stg_supplychain_v2
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
                
                fig_late_month.update_layout(title="Xu hướng Rủi ro theo Thời gian (%)", xaxis_title="", yaxis_title="", hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
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
                FROM my_db.main.stg_supplychain_v2
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
                    textposition='inside', textinfo='percent+label'
                )])
                fig_impact.update_layout(title="Doanh thu bị Đe dọa", margin=dict(t=50, b=20, l=20, r=20))
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
                FROM my_db.main.stg_supplychain_v2
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
                FROM my_db.main.stg_supplychain_v2
                WHERE {where_c}
                GROUP BY 1 HAVING COUNT(*) > 50 ORDER BY 2 DESC LIMIT 10
                """
                return con.execute(query).df()
                
            df_country = get_late_by_country(where_clause)
            if not df_country.empty:
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
            FROM my_db.main.stg_supplychain_v2
            WHERE {where_c}
            LIMIT 10000
            """
            return con.execute(query_map).df()
        
        df_map = get_map_data(where_clause)
        
        if not df_map.empty:
            country_dict = {
                'Egipto': 'Egypt', 'Camboya': 'Cambodia', 'Suecia': 'Sweden', 'Costa de Marfil': "Côte d'Ivoire",
                'Francia': 'France', 'Alemania': 'Germany', 'Brasil': 'Brazil', 'España': 'Spain',
                'Italia': 'Italy', 'Reino Unido': 'United Kingdom', 'Estados Unidos': 'United States',
                'Japon': 'Japan', 'Corea del Sur': 'South Korea', 'Nueva Zelanda': 'New Zealand',
                'Paises Bajos': 'Netherlands', 'Filipinas': 'Philippines', 'Marruecos': 'Morocco',
                'Argelia': 'Algeria', 'Republica Dominicana': 'Dominican Republic', 'Sudafrica': 'South Africa',
                'Turquia': 'Turkey', 'Suiza': 'Switzerland', 'Rusia': 'Russia', 'Belgica': 'Belgium'
            }
            df_map['order_country'] = df_map['order_country'].replace(country_dict)
            
            # Sử dụng Heatmap Density thay cho Scatter
            fig_map = px.density_mapbox(df_map, lat='latitude', lon='longitude', z='sales_amount', radius=10,
                                        center=dict(lat=20, lon=0), zoom=1.5,
                                        mapbox_style="carto-positron", color_continuous_scale="Inferno")
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Không có dữ liệu hiển thị bản đồ")


# ---------------------------------------------------------
# MODULE 2: AI & SHAP (CỰC KỲ ĐẸP & CÔNG NGHỆ)
# ---------------------------------------------------------
elif menu_selection == "Mô hình Dự báo (AI)":
    st.markdown('<div class="gradient-text">Mô hình Phân tích rủi ro bằng Trí tuệ Nhân tạo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Giải mã thuật toán Machine Learning - Ứng dụng công nghệ SHAP để giải thích các quyết định dự báo rủi ro.</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<h4 style='text-align:center;'>SHAP GLOBAL SUMMARY (ĐỘ BAO PHỦ TOÀN CỤC)</h4>", unsafe_allow_html=True)
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
                
                # Biểu đồ SHAP Beeswarm với gradient màu Công nghệ
                # Do px.strip không hỗ trợ color_continuous_scale, ta dùng px.scatter với manual jitter
                feature_to_idx = {feat: i for i, feat in enumerate(feature_order)}
                melted['feature_idx'] = melted['feature'].map(feature_to_idx)
                melted['feature_idx_jitter'] = melted['feature_idx'] + np.random.uniform(-0.25, 0.25, len(melted))
                
                fig_fi = px.scatter(melted, x='shap_value', y='feature_idx_jitter', 
                                  color='shap_value', 
                                  color_continuous_scale='RdBu_r')
                
                fig_fi.update_traces(marker=dict(size=6, opacity=0.8, line=dict(width=0)))
                fig_fi.add_vline(x=0, line_width=1, line_color="#94A3B8", line_dash="dash")
                
                fig_fi.update_layout(
                    xaxis_title="SHAP Value (Tác động lên rủi ro)",
                    yaxis_title="",
                    coloraxis_colorbar=dict(title="Tác động", thicknessmode="pixels", thickness=15),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=30, b=20, l=20, r=20),
                    font_family="'Plus Jakarta Sans', sans-serif",
                    font_color="#475569"
                )
                fig_fi.update_xaxes(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0")
                fig_fi.update_yaxes(
                    tickvals=list(range(len(feature_order))),
                    ticktext=list(feature_order),
                    showgrid=True, gridwidth=1, gridcolor='#F1F5F9', linecolor="#E2E8F0"
                )
                st.plotly_chart(fig_fi, use_container_width=True)
            except Exception as e:
                import traceback
                with open("shap_error.log", "w") as f:
                    f.write(traceback.format_exc())
                st.error(f"Lỗi khi vẽ biểu đồ SHAP: {str(e)}")
        else:
            st.warning("Không tìm thấy dữ liệu ml_predictions_explained.")

    with st.container(border=True):
        st.markdown("<h4>SHAP WATERFALL PLOT (GIẢI PHẪU ĐƠN HÀNG CỤ THỂ)</h4>", unsafe_allow_html=True)
        @st.cache_data(ttl=3600)
        def get_shap_predictions():
            query = "SELECT * FROM my_db.main.ml_predictions_explained LIMIT 100"
            try:
                return con.execute(query).df()
            except:
                return pd.DataFrame()
                
        df_shap = get_shap_predictions()
        
        if not df_shap.empty:
            selected_order = st.selectbox("🔍 Nhập mã Đơn hàng (Order ID) để AI phân tích:", df_shap['order_id'])
            
            row = df_shap[df_shap['order_id'] == selected_order].iloc[0]
            shap_cols = [c for c in df_shap.columns if c.startswith('shap_')]
            
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
            
            prob = row['predicted_probability']
            pred = "⚠️ NGUY CƠ TRỄ HẠN CAO" if row['predicted_label'] == 1 else "✅ TIẾN ĐỘ AN TOÀN"
            pred_color = "#E11D48" if row['predicted_label'] == 1 else "#10B981"
            
            fig_waterfall.update_layout(
                title=f"<span style='color:{pred_color}; font-size:22px;'>{pred}</span> <br><span style='font-size:14px;color:#64748B;'>Xác suất rủi ro: {prob*100:.1f}%</span>",
                showlegend=False, waterfallgap=0.2
            )
            fig_waterfall = apply_light_theme(fig_waterfall)
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
            st.markdown("*💡 **Lưu ý về dữ liệu:** Các giá trị trên biểu đồ Waterfall (trục Y) thể hiện **Log-Odds** (thước đo nội bộ của thuật toán). Tổng các điểm cộng dồn này (cộng với Base Value) sẽ được đưa qua hàm Sigmoid để tính ra tỷ lệ Xác suất rủi ro % hiển thị ở trên.*")
        else:
            st.warning("Không tìm thấy dữ liệu ml_predictions_explained.")
