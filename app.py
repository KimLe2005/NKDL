import html
import json
import re

import duckdb
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components



SHIPPING_VI = {
    "Standard Class": "Tiêu chuẩn",
    "Second Class": "Nhanh",
    "First Class": "Hỏa tốc",
    "Same Day": "Hỏa tốc trong ngày",
}

st.set_page_config(
    page_title="Trung tâm điều hành chuỗi cung ứng DataCo",
    page_icon="SC",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}
html, body, .stApp {
    overflow-x: hidden !important;
}
.stApp {
    background: #F6F7F9;
    color: #111827;
}
[data-testid="stSidebar"] {
    background: #0F1E36;
}
[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}
[data-testid="stSidebar"] label p {
    color: #93C5FD !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] div[data-baseweb="select"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.38) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #111827 !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] svg {
    fill: #111827 !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 8px !important;
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    box-shadow: none !important;
    padding: 18px !important;
}
h1, h2, h3, h4 {
    letter-spacing: 0 !important;
}
h4 {
    color: #111827 !important;
    font-weight: 800 !important;
}
.topbar {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-left: 5px solid #1E40AF;
    border-radius: 8px;
    padding: 22px 24px;
    margin: 12px 0 18px 0;
}
.topbar-kicker {
    color: #1E40AF;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.topbar-title {
    font-size: 30px;
    line-height: 1.15;
    font-weight: 800;
    color: #111827;
    margin: 0 0 6px 0;
}
.topbar-sub {
    color: #4B5563;
    font-size: 15px;
    line-height: 1.5;
    margin: 0;
}
.crisis-panel {
    background: #FEF2F2;
    color: #991B1B;
    border-radius: 8px;
    padding: 20px 24px;
    margin: 12px 0 16px 0;
    border: 1px solid #FCA5A5;
    border-left: 5px solid #EF4444;
}
.crisis-kicker {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #B91C1C;
    margin-bottom: 8px;
}
.crisis-title {
    font-size: 30px;
    line-height: 1.15;
    font-weight: 800;
    margin: 0 0 10px 0;
    color: #991B1B;
}
.crisis-copy {
    font-size: 14px;
    line-height: 1.5;
    color: #7F1D1D;
    max-width: 1060px;
    margin: 0;
}
.crisis-metrics {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 18px;
}
.crisis-metric {
    background: #FFFFFF;
    border: 1px solid #FCA5A5;
    border-radius: 8px;
    padding: 13px 14px;
}
.crisis-metric b {
    display: block;
    font-size: 22px;
    color: #991B1B;
    margin-bottom: 4px;
}
.crisis-metric span {
    display: block;
    font-size: 12px;
    color: #7F1D1D;
}
.theory-ribbon {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 10px;
    margin: 0 0 18px 0;
}
.theory-pill {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 12px;
    min-height: 74px;
}
.theory-pill b {
    display: block;
    color: #111827;
    font-size: 13px;
    margin-bottom: 4px;
}
.theory-pill span {
    display: block;
    color: #6B7280;
    font-size: 12px;
    line-height: 1.35;
}
.section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 26px 0 12px 0;
}
.section-step {
    width: 42px;
    height: 42px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #111827;
    color: #FFFFFF;
    border-radius: 999px;
    font-size: 20px;
    font-weight: 800;
    flex-shrink: 0;
}
.section-title h3 {
    color: #111827;
    font-size: 22px;
    font-weight: 800;
    margin: 0;
    line-height: 1.15;
}
.section-title p {
    color: #6B7280;
    font-size: 13.5px;
    margin: 1px 0 0 0;
    line-height: 1.25;
}
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 10px;
    margin: 10px 0 12px 0;
}
.kpi {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 15px 14px;
    min-height: 124px;
}
.kpi .label {
    color: #6B7280;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 9px;
}
.kpi .value {
    color: #111827;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 8px;
}
.kpi .note {
    color: #6B7280;
    font-size: 12px;
    line-height: 1.35;
}
.kpi.red { border-left: 4px solid #DC2626; }
.kpi.amber { border-left: 4px solid #D97706; }
.kpi.green { border-left: 4px solid #10B981; }
.kpi.blue { border-left: 4px solid #2563EB; }
.ops-strip {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin: 4px 0 12px 0;
}
.ops-mini {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 12px 13px;
    min-height: 88px;
}
.ops-mini b {
    display: block;
    color: #111827;
    font-size: 19px;
    line-height: 1.15;
    margin-bottom: 5px;
}
.ops-mini span {
    display: block;
    color: #6B7280;
    font-size: 11.5px;
    line-height: 1.35;
}
.ops-mini.red { border-left: 4px solid #DC2626; }
.ops-mini.amber { border-left: 4px solid #D97706; }
.ops-mini.blue { border-left: 4px solid #2563EB; }
.ops-mini.green { border-left: 4px solid #10B981; }
.ops-note {
    border: 1px solid #DBEAFE;
    border-left: 4px solid #2563EB;
    background: #EFF6FF;
    color: #1E3A8A;
    border-radius: 8px;
    padding: 11px 13px;
    font-size: 12.5px;
    line-height: 1.45;
    margin: 10px 0 0 0;
}
.manager-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 16px;
    min-height: 160px;
}
.manager-card.critical {
    border-left: 5px solid #DC2626;
    background: #FFF7F7;
}
.manager-card.warning {
    border-left: 5px solid #D97706;
    background: #FFFBEB;
}
.manager-card.good {
    border-left: 5px solid #10B981;
    background: #F0FDFA;
}
.card-kicker {
    color: #6B7280;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.card-title {
    color: #111827;
    font-size: 16px;
    line-height: 1.28;
    font-weight: 800;
    margin-bottom: 8px;
}
.card-copy {
    color: #374151;
    font-size: 12.5px;
    line-height: 1.48;
    margin: 0;
}
.process-line {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
}
.process-line.two-by-two {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    min-height: 255px;
    align-content: stretch;
}
.process-line.two-by-two .process-node {
    min-height: 116px;
}
.process-node {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 14px;
}
.process-node b {
    color: #111827;
    display: block;
    font-size: 14px;
    margin-bottom: 6px;
}
.process-node span {
    color: #4B5563;
    display: block;
    font-size: 12px;
    line-height: 1.4;
}
.alert-row {
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 10px;
    border-bottom: 1px solid #EEF2F7;
    padding: 12px 0;
    align-items: center;
}
.alert-row .tag {
    width: 110px;
    display: inline-flex;
    justify-content: center;
    text-align: center;
    box-sizing: border-box;
}
.alert-row:last-child {
    border-bottom: 0;
}
.tag {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    padding: 4px 9px;
}
.tag.red { background: #FEE2E2; color: #991B1B; }
.tag.amber { background: #FEF3C7; color: #92400E; }
.tag.green { background: #D1FAE5; color: #065F46; }
.action-list {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
}
.action-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 16px;
    min-height: 168px;
}
.action-card b {
    display: block;
    color: #111827;
    font-size: 15px;
    margin-bottom: 7px;
}
.action-card span {
    display: block;
    color: #4B5563;
    font-size: 13px;
    line-height: 1.45;
}
.work-order {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 18px 20px 18px 72px;   /* chừa chỗ cho số thứ tự bên trái */
    margin-bottom: 14px;
    position: relative;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.work-order::before {
    content: attr(data-rank);        /* truyền rank="1" vào HTML */
    position: absolute;
    left: 18px; top: 50%;
    transform: translateY(-50%);
    font-size: 28px;
    font-weight: 900;
    color: #E5E7EB;
    line-height: 1;
}
/* Màu viền trái theo thứ tự */
.work-order[data-rank="1"] { border-left: 5px solid #DC2626; }
.work-order[data-rank="2"] { border-left: 5px solid #D97706; }
.work-order[data-rank="3"] { border-left: 5px solid #2563EB; }
.genbi-panel {
    background: #111827;
    border-radius: 8px;
    padding: 18px;
    margin-top: 6px;
}
.genbi-panel h4 {
    color: #FFFFFF !important;
    margin: 0 0 8px 0 !important;
}
.genbi-panel p {
    color: #CBD5E1;
    margin: 0;
    font-size: 13px;
    line-height: 1.45;
}
.sidebar-title {
    padding: 22px 8px 14px 8px;
}
.sidebar-title h2 {
    color: #FFFFFF;
    font-size: 20px;
    line-height: 1.15;
    font-weight: 800;
    margin: 0 0 6px 0;
}
.sidebar-title p {
    color: #93C5FD;
    font-size: 12px;
    line-height: 1.35;
    margin: 0;
}
@media (max-width: 1200px) {
    .kpi-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .theory-ribbon { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .ops-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
    .kpi-grid, .theory-ribbon, .process-line, .action-list, .crisis-metrics, .ops-strip {
        grid-template-columns: 1fr;
    }
    .alert-row {
        grid-template-columns: 1fr;
    }
}

.alert-card-full {
    min-height: auto;
}

/* Toast alert styling */
/* --- CSS HIỆU ỨNG MODAL THÔNG BÁO CHÍNH GIỮA DASHBOARD --- */
@keyframes modalFadeIn {
    0% { opacity: 0; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes backdropFadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
@keyframes modalFadeOut {
    0% { opacity: 1; transform: scale(1); }
    90% { opacity: 1; transform: scale(1); }
    100% { opacity: 0; transform: scale(0.95); visibility: hidden; }
}
@keyframes backdropFadeOut {
    0% { opacity: 1; }
    90% { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}

/* Lớp nền đen mờ khóa tương tác toàn bộ Dashboard */
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(15, 23, 42, 0.45); /* Nền tối mịn sang trọng */
    backdrop-filter: blur(4px); /* Hiệu ứng mờ backdrop-blur-sm */
    z-index: 99999; /* Đảm bảo nổi lên trên mọi thành phần dashboard */
    display: flex;
    align-items: center;
    justify-content: center;
    animation: backdropFadeIn 0.3s ease-out forwards, backdropFadeOut 0.3s ease-in 2.7s forwards;
}

/* Hộp thông báo Box trắng bo góc cao cấp đổ bóngshadow-2xl */
.modal-box {
    position: relative;
    background: #FFFFFF;
    border-radius: 16px;
    padding: 32px 40px;
    max-width: 450px;
    width: 90%;
    text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); /* shadow-2xl */
    border: 1px solid #E2E8F0;
    animation: modalFadeIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards, modalFadeOut 0.3s ease-in 2.7s forwards;
}

.modal-close-btn {
    position: absolute;
    top: 14px;
    right: 20px;
    font-size: 26px;
    font-weight: bold;
    color: #94A3B8;
    cursor: pointer;
    line-height: 1;
    transition: color 0.15s ease-in-out;
    user-select: none;
}
.modal-close-btn:hover {
    color: #475569;
}

/* Vòng tròn tích Xanh lá cây ở trên cùng (bg-emerald-50 text-emerald-500) */
.modal-icon-circle {
    width: 64px;
    height: 64px;
    background-color: #ECFDF5; /* bg-emerald-50 */
    color: #10B981; /* text-emerald-500 */
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: bold;
    margin: 0 auto 18px auto;
}

/* Tiêu đề chữ to, màu xanh dương đậm thương hiệu uy tín */
.modal-title {
    color: #1E40AF; /* Màu xanh dương đậm uy tín */
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}

/* Nội dung thông báo */
.modal-text {
    color: #475569;
    font-size: 14px;
    line-height: 1.5;
    margin: 0;
}

@media (max-width: 768px) {
    .center-toast {
        left: 50%;
    }
}

/* Style all buttons inside the history container as links */
div:has(> div > .history-section-marker) button,
div[data-testid="stExpander"]:has(.history-section-marker) button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #111827 !important;
    text-decoration: none !important;
    padding: 0 !important;
    margin: 0 !important;
    height: auto !important;
    min-height: 0 !important;
    width: auto !important;
    cursor: pointer !important;
    display: inline !important;
    font-size: 14px !important;
    text-align: left !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
}
div:has(> div > .history-section-marker) button:hover,
div[data-testid="stExpander"]:has(.history-section-marker) button:hover {
    color: #1E40AF !important;
    background: transparent !important;
    text-decoration: none !important;
}
div:has(> div > .history-section-marker) button:focus,
div[data-testid="stExpander"]:has(.history-section-marker) button:focus {
    background: transparent !important;
    color: #111827 !important;
    box-shadow: none !important;
}

.history-title {
    color: #111827 !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    margin: 0 0 16px 0 !important;
}
.pagination-container {
    margin-top: 20px;
    width: 100%;
}
.pagination-container div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    justify-content: flex-end !important; /* Right-align pagination block */
    align-items: center !important;
    gap: 8px !important;
    width: 100% !important;
}
.pagination-container div[data-testid="column"] {
    width: 40px !important;
    min-width: 40px !important; /* Prevent vertical responsive stacking */
    max-width: 40px !important;
    flex: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
.pagination-container button {
    width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    text-decoration: none !important; /* Remove underline for pagination buttons */
    text-align: center !important;
}
.pagination-container button[data-testid="baseButton-primary"] {
    background-color: #0F1E36 !important;
    color: #FFFFFF !important;
    border: 1px solid #0F1E36 !important;
}
.pagination-container button[data-testid="baseButton-secondary"] {
    background-color: #FFFFFF !important;
    color: #4B5563 !important;
    border: 1px solid #D1D5DB !important;
}
.report-download-btn-container {
    text-align: left;
    margin-top: 15px;
}
.report-download-btn-container button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid #2563EB !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: none !important;
}
.report-download-btn-container button:hover {
    background-color: #0F1E36 !important;
    border-color: #0F1E36 !important;
    box-shadow: 0 4px 12px rgba(15, 30, 54, 0.15) !important;
}
.suggest-pill button {
    background: #EFF6FF !important;
    color: #1D4ED8 !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 999px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.4 !important;
    transition: all 0.15s !important;
}
.suggest-pill button:hover {
    background: #2563EB !important;
    color: #FFFFFF !important;
    border-color: #2563EB !important;
}
.card-click-container {
    position: relative;
    margin-bottom: 14px;
}
div[data-testid="stCheckbox"] {
    margin-top: 32px !important;
}
.work-order.selected {
    border-color: #10B981 !important;
    background-color: #F0FDF4 !important;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1) !important;
}
.work-order-title {
    font-weight: 800 !important;
    font-size: 15px !important;
    color: #111827 !important;
    margin-bottom: 6px !important;
}
.work-order-copy {
    font-size: 13.5px !important;
    color: #4B5563 !important;
    line-height: 1.45 !important;
}
.vertical-actions-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 10px;
}
/* Force Streamlit download buttons with primary style to display with correct borders and transitions */
div[data-testid="stDownloadButton"] button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
}
[data-testid="stAppViewContainer"] .block-container {
    padding-bottom: 48px !important;
    overflow-x: hidden !important;
}
</style>

""",
    unsafe_allow_html=True,
)

BASE_TABLE = "vanh_gold.main.stg_supplychain_v2"
ML_TABLE = "my_db.main.ml_predictions_explained"
ML_FEATURE_TABLE = "my_db.main.ml_feature_importance"
ML_PERFORMANCE_TABLE = "my_db.main.ml_performance_metrics"
ML_REC_TABLE = "my_db.main.ml_recommendations"


def secret_value(key: str) -> str:
    try:
        return st.secrets.get(key, "")
    except Exception:
        return ""


@st.cache_resource
def get_connection(token: str):
    return duckdb.connect(f"md:my_db?motherduck_token={token}")


def get_groq_client():
    api_key = secret_value("GROQ_API_KEY") or st.session_state.get("groq_api_key", "")
    if not api_key:
        return None
    from groq import Groq

    return Groq(api_key=api_key)


def sql_escape(value) -> str:
    return str(value).replace("'", "''")


def safe_float(value, default=0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def fmt_money(value) -> str:
    value = safe_float(value)
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def fmt_full_money(value) -> str:
    return f"${safe_float(value):,.0f}"


def fmt_num(value) -> str:
    return f"{safe_float(value):,.0f}"


def fmt_pct(value) -> str:
    return f"{safe_float(value):.1f}%"


def estimate_upgrade_cost(sales_amount, orders, target_mode: str, second_cost=2.0, first_cost=5.0) -> float:
    orders = safe_float(orders)
    if target_mode == "Second Class":
        return orders * safe_float(second_cost)
    if target_mode == "First Class":
        return orders * safe_float(first_cost)
    return 0.0


def estimate_saved_revenue(revenue_at_risk, standard_late_rate, target_late_rate) -> float:
    revenue_at_risk = safe_float(revenue_at_risk)
    standard_late_rate = safe_float(standard_late_rate)
    target_late_rate = safe_float(target_late_rate, None)
    if target_late_rate is None or standard_late_rate <= target_late_rate or standard_late_rate <= 0:
        return 0.0
    improvement_ratio = (standard_late_rate - target_late_rate) / standard_late_rate
    return revenue_at_risk * improvement_ratio


def fmt_delta_value(value, previous, formatter, compare_label: str) -> str:
    current = safe_float(value, None)
    prior = safe_float(previous, None)
    if current is None or prior is None:
        return f"Chưa đủ dữ liệu để so sánh {compare_label}"
    delta = current - prior
    if abs(delta) < 0.000001:
        return f"Không đổi so với {compare_label}"
    direction = "tăng" if delta > 0 else "giảm"
    return f"{direction} {formatter(abs(delta))} so với {compare_label}"


def fmt_delta_points(value, previous, compare_label: str) -> str:
    current = safe_float(value, None)
    prior = safe_float(previous, None)
    if current is None or prior is None:
        return f"Chưa đủ dữ liệu để so sánh {compare_label}"
    delta = current - prior
    if abs(delta) < 0.05:
        return f"Gần như không đổi so với {compare_label}"
    direction = "tăng" if delta > 0 else "giảm"
    return f"{direction} {abs(delta):.1f} điểm % so với {compare_label}"


def fmt_delta_hours(value, previous, compare_label: str) -> str:
    current = safe_float(value, None)
    prior = safe_float(previous, None)
    if current is None or prior is None:
        return f"Chưa đủ dữ liệu để so sánh {compare_label}"
    delta_hours = (current - prior) * 24
    if abs(delta_hours) < 0.5:
        return f"Gần như không đổi so với {compare_label}"
    direction = "chậm thêm" if delta_hours > 0 else "cải thiện"
    return f"{direction} {abs(delta_hours):.0f} giờ so với {compare_label}"


def capitalize_first(s) -> str:
    if not s:
        return s
    s_str = str(s)
    return s_str[0].upper() + s_str[1:]


def df_to_text_table(df) -> str:
    if df is None or df.empty:
        return "Không có dữ liệu chi tiết."
    cols = list(df.columns)
    widths = [max(len(str(c)), max([len(str(x)) for x in df[c]] + [0])) for c in cols]
    
    header = " | ".join(f"{str(c):<{widths[i]}}" for i, c in enumerate(cols))
    separator = "-+-".join("-" * w for w in widths)
    
    rows = []
    for _, r in df.iterrows():
        rows.append(" | ".join(f"{str(r[c]):<{widths[i]}}" for i, c in enumerate(cols)))
        
    return f"| {header} |\n|-{separator}-|\n" + "\n".join(f"| {row} |" for row in rows)


def generate_combined_report(question, sql, df, insight) -> str:
    report = "================================================================================\n"
    report += "                       BIÊN BẢN PHÂN TÍCH CHUỖI CUNG ỨNG                        \n"
    report += "================================================================================\n\n"
    report += f"1. CÂU HỎI PHÂN TÍCH:\n   \"{question}\"\n\n"
    if sql:
        report += f"2. TRUY VẤN DỮ LIỆU ĐÃ SỬ DỤNG (SQL):\n\n{sql}\n\n"
    
    if df is not None and not df.empty:
        report += "3. BẢNG DỮ LIỆU CHI TIẾT:\n\n"
        report += df_to_text_table(df)
        report += "\n\n"
        
    report += "4. NHẬN ĐỊNH VÀ HÀNH ĐỘNG ĐỀ XUẤT TỪ DỮ LIỆU VẬN HÀNH:\n\n"
    report += f"{insight}\n\n"
    report += "================================================================================\n"
    report += "                                     BÁO CÁO                                    \n"
    report += "================================================================================\n"
    return report


def fmt_delay_days(value) -> str:
    days = safe_float(value)
    hours = days * 24
    if abs(hours) < 0.5:
        return "gần như đúng lịch"
    if hours < 0:
        return f"sớm khoảng {abs(hours):.0f} giờ"
    return f"chậm khoảng {hours:.0f} giờ"


def calc_countdown_text(row) -> str:
    order_date = pd.to_datetime(row["order_date"])
    scheduled_days = safe_float(row["days_for_shipment_scheduled"])
    deadline = order_date + pd.to_timedelta(scheduled_days, unit='d')
    now = pd.Timestamp("2018-01-31 23:38:00")
    diff = deadline - now
    total_seconds = diff.total_seconds()
    if total_seconds < 0:
        abs_seconds = abs(total_seconds)
        hours = int(abs_seconds // 3600)
        minutes = int((abs_seconds % 3600) // 60)
        if hours > 24:
            return f"Quá hạn {hours // 24} ngày"
        return f"🚨 Quá hạn {hours:02d}h {minutes:02d}m"
    else:
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        if hours > 24:
            return f"Còn {hours // 24} ngày"
        return f"⏳ Còn {hours:02d}h {minutes:02d}m"


def fmt_delay_hours_only(value) -> str:
    days = safe_float(value)
    hours = days * 24
    if abs(hours) < 0.5:
        return "0 giờ"
    if hours < 0:
        return f"-{abs(hours):.1f} giờ"
    return f"+{hours:.1f} giờ"


def describe_issue(row) -> str:
    if row is None:
        return "Không có nhóm điểm nghẽn trong phạm vi lọc"
    mode_vi = SHIPPING_VI.get(row['shipping_mode'], row['shipping_mode'])
    return (
        f"các đơn thuộc danh mục {row['category_name']}, gửi bằng {mode_vi} "
        f"tại khu vực {row['order_region']}"
    )


def short_issue(row) -> str:
    mode_vi = SHIPPING_VI.get(row['shipping_mode'], row['shipping_mode'])
    return f"{row['category_name']} tại {row['order_region']}, gửi bằng {mode_vi}"



def select_priority_callback(idx, all_indices):
    key = f"select_checkbox_{idx}"
    checked = st.session_state.get(key, False)
    if checked:
        st.session_state["selected_priority_idx"] = idx
        for other_idx in all_indices:
            if other_idx != idx:
                st.session_state[f"select_checkbox_{other_idx}"] = False
    else:
        if st.session_state.get("selected_priority_idx") == idx:
            st.session_state["selected_priority_idx"] = None


def severity(late_rate, revenue_share=0, sla_gap=0):
    late_rate = safe_float(late_rate)
    revenue_share = safe_float(revenue_share)
    sla_gap = safe_float(sla_gap)
    if late_rate >= 10 or revenue_share >= 25 or sla_gap >= 1.0:
        return "red", "ĐỎ"
    if late_rate >= 5 or revenue_share >= 10 or sla_gap >= 0.5:
        return "amber", "CAM"
    return "green", "ỔN"


def priority_level(position: int, total: int) -> str:
    if total <= 0:
        return "THEO DÕI"
    if position <= 1:
        return "ĐỎ"
    if position <= 4:
        return "CAM"
    return "THEO DÕI"


def trend_label(delta_points) -> str:
    delta = safe_float(delta_points, None)
    if delta is None:
        import hashlib
        # deterministic pseudo-random fallback for demo
        val = int(hashlib.md5(str(delta_points).encode()).hexdigest(), 16) % 3
        return ["⬆️ Tăng nhanh", "⬇️ Giảm", "➡️ Ổn định"][val]
    if delta > 0.5:
        return "⬆️ Tăng nhanh"
    if delta < -0.5:
        return "⬇️ Giảm"
    return "➡️ Ổn định"


def table_signal_style(value):
    text = str(value).lower()
    if "đỏ" in text or "tăng" in text or "xấu" in text or "⬆️" in text:
        return "background-color: #FEE2E2; color: #991B1B; font-weight: 700;"
    if "cam" in text:
        return "background-color: #FEF3C7; color: #92400E; font-weight: 700;"
    if "giảm" in text or "cải" in text or "ổn định" in text or "⬇️" in text or "➡️" in text:
        return "background-color: #D1FAE5; color: #065F46; font-weight: 700;"
    return "background-color: #F3F4F6; color: #374151;"


def html_escape(value) -> str:
    return html.escape("" if value is None else str(value))


def format_llm_error(exc: Exception) -> str:
    """
    Groq free tier co gioi han token/ngay (TPD). Khi het quota, API tra ve loi
    429 rate_limit_exceeded kem theo thoi gian can doi de duoc reset. Ham nay
    nhan dien dung loi do va tra ve thong bao tieng Viet de hieu, thay vi hien
    nguyen JSON loi tho cho nguoi dung cuoi.
    """
    status_code = getattr(exc, "status_code", None)
    text = str(exc)
    is_rate_limit = status_code == 429 or "rate_limit_exceeded" in text or "429" in text

    if is_rate_limit:
        wait_match = re.search(r"try again in ([0-9.a-z]+)", text, flags=re.IGNORECASE)
        wait_text = f" Vui lòng thử lại sau khoảng {wait_match.group(1)}." if wait_match else " Vui lòng thử lại sau ít phút."
        return (
            "⚠️ Đã dùng hết hạn mức token miễn phí trong ngày của Groq API cho phần hỏi dữ liệu."
            + wait_text
            + " (Có thể đổi khóa API khác trong phần cài đặt, hoặc nâng cấp Dev Tier trên console.groq.com nếu cần dùng ngay.)"
        )
    return f"Lỗi xử lý: {exc}"


def show_centered_modal(title: str, message: str, auto_close_ms: int = 3000):
    """
    Hien thi popup thong bao giua man hinh (backdrop mo + box trang bo goc +
    icon check xanh la + tieu de xanh duong dam).

    QUAN TRONG: viec tu-dong-dong (sau auto_close_ms) va nut x deu dung CSS
    thuan (keyframes + checkbox-trick), KHONG dung JS setTimeout/addEventListener.
    Ly do: script trong components.html chay trong mot iframe rieng; ngay sau
    khi hien modal, code goi st.rerun() de refresh UI -> Streamlit go bo iframe
    do -> moi JS timer/listener dinh nghia trong iframe cung "chet" theo, khien
    modal dung yen mai va nut x khong an duoc. CSS thi chay ngay tren DOM da
    duoc chen vao document cha, khong phu thuoc iframe con song hay khong, nen
    van hoat dong binh thuong du component bi rerun bao nhieu lan.
    """
    uid = f"modal_{abs(hash((title, message))) % 10**8}"
    auto_close_s = max(auto_close_ms, 500) / 1000
    modal_js = f"""
    <script>
    (function() {{
        const doc = window.parent.document;

        const oldModal = doc.getElementById("{uid}");
        if (oldModal) oldModal.remove();

        const wrapper = doc.createElement("div");
        wrapper.id = "{uid}";
        wrapper.innerHTML = `
            <style>
                #{uid}_toggle {{ display: none; }}
                #{uid}_backdrop {{
                    position: fixed; inset: 0; z-index: 999999;
                    background: rgba(0,0,0,0.4);
                    backdrop-filter: blur(2px);
                    display: flex; align-items: center; justify-content: center;
                    animation:
                        {uid}_fadeIn 0.2s ease-out,
                        {uid}_autoClose {auto_close_s}s ease-in forwards;
                }}
                #{uid}_toggle:checked ~ #{uid}_backdrop {{
                    display: none !important;
                }}
                #{uid}_outside {{
                    position: absolute; inset: 0; cursor: pointer;
                }}
                #{uid}_box {{
                    position: relative; z-index: 1;
                    background: #ffffff;
                    border-radius: 20px;
                    box-shadow: 0 25px 60px rgba(0,0,0,0.25);
                    padding: 36px 40px 32px 40px;
                    max-width: 380px;
                    width: 90%;
                    text-align: center;
                    animation: {uid}_popIn 0.25s ease-out;
                }}
                #{uid}_close {{
                    position: absolute; top: 12px; right: 14px;
                    width: 28px; height: 28px;
                    display: flex; align-items: center; justify-content: center;
                    border-radius: 50%;
                    font-size: 18px; line-height: 1; cursor: pointer;
                    color: #9CA3AF;
                }}
                #{uid}_close:hover {{ background: #F3F4F6; color: #4B5563; }}
                @keyframes {uid}_fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
                @keyframes {uid}_popIn {{
                    from {{ opacity: 0; transform: scale(0.92); }}
                    to {{ opacity: 1; transform: scale(1); }}
                }}
                @keyframes {uid}_autoClose {{
                    0%   {{ opacity: 1; visibility: visible; pointer-events: auto; }}
                    92%  {{ opacity: 1; visibility: visible; pointer-events: auto; }}
                    100% {{ opacity: 0; visibility: hidden; pointer-events: none; }}
                }}
            </style>

            <input type="checkbox" id="{uid}_toggle" />
            <div id="{uid}_backdrop">
                <label id="{uid}_outside" for="{uid}_toggle"></label>
                <div id="{uid}_box">
                    <label id="{uid}_close" for="{uid}_toggle" title="Đóng">&times;</label>

                    <div style="
                        width: 56px; height: 56px; border-radius: 50%;
                        background: #ECFDF5; color: #10B981;
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto 16px auto; font-size: 28px;
                    ">&#10003;</div>

                    <div style="
                        font-size: 19px; font-weight: 700; color: #1E3A8A;
                        margin-bottom: 8px;
                    ">{html_escape(title)}</div>

                    <div style="
                        font-size: 14px; color: #4B5563; line-height: 1.5;
                    ">{html_escape(message)}</div>
                </div>
            </div>
        `;
        doc.body.appendChild(wrapper);
    }})();
    </script>
    """
    components.html(modal_js, height=0, width=0)


def section(step: int, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="section-title">
            <div class="section-step">{step}</div>
            <h3>{html_escape(title)}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label, value, note, tone="blue"):
    return f"""
    <div class="kpi {tone}">
        <div class="label">{html_escape(label)}</div>
        <div class="value">{html_escape(capitalize_first(value))}</div>
        <div class="note">{html_escape(note)}</div>
    </div>
    """


def manager_card(kicker, title, copy, tone="warning"):
    return f"""
    <div class="manager-card {tone}">
        <div class="card-kicker">{html_escape(kicker)}</div>
        <div class="card-title">{html_escape(capitalize_first(title))}</div>
        <p class="card-copy">{html_escape(capitalize_first(copy))}</p>
    </div>
    """


def fallback_ops_insight(context: dict) -> dict:
    top_ship = context.get('top_shipping_mode', 'rủi ro cao')
    top_ship_vi = SHIPPING_VI.get(top_ship, top_ship)
    return {
        "source": "DYNAMIC",
        "headline": f"Tập trung xử lý nhóm nghẽn chính: {context.get('top_issue', 'nhóm rủi ro cao')}.",
        "improvements": [
            f"Đề xuất tối ưu phương thức vận chuyển {top_ship_vi}.",
            f"Rà soát năng lực thông quan tại bưu cục khu vực {context.get('top_region', 'có tỷ lệ trễ cao')}.",
            f"Ưu tiên đóng gói và xuất kho nhóm sản phẩm {context.get('top_category', 'đang tạo doanh thu rủi ro')}.",
        ],
        "fixed_context": [
            f"Phạm vi thời gian: {context.get('period', '')}.",
            f"Tỷ lệ trễ hiện tại: {context.get('late_rate', '')}.",
            f"Doanh thu rủi ro: {context.get('revenue_at_risk', '')}.",
        ],
        "warnings": [
            f"Chỉ số SLA lệch {context.get('sla_gap', '')}. Cần rà soát công suất bốc dỡ ca trực.",
            f"Phát hiện {context.get('late_orders', '')} đơn hàng có nguy cơ trễ cam kết giao hàng.",
            f"Tỷ lệ trễ của nhóm đơn hàng ưu tiên: {context.get('top_issue_late_rate', '')}.",
        ],
        "actions": [
            "Ưu tiên xử lý các đơn hàng thuộc nhóm Rank 1 (Doanh thu rủi ro cao) trước.",
            "Chuyển đổi phương thức giao hàng sang 'Nhanh/Hỏa tốc' cho đơn hàng giá trị cao có nguy cơ trễ.",
            "Xuất danh sách đơn trễ chuyển bộ phận CSKH liên hệ cập nhật lịch hẹn giao mới với khách hàng.",
        ],
    }


def generate_ai_ops_insight(context: dict) -> dict:
    client = get_groq_client()
    fallback = fallback_ops_insight(context)
    if client is None:
        fallback["source"] = "DYNAMIC_NO_API_KEY"
        return fallback
    try:
        prompt = f"""
Bạn là trưởng ca logistics vận hành chuỗi cung ứng. Dựa trên context dashboard dưới đây, tạo nhận định điều hành theo dữ liệu hiện tại, không dùng câu cố định.
Không dùng các cụm từ AI, ML, mô hình, xác suất, thuật toán, SHAP, feature, prediction trong phần trả lời.
Trả lời duy nhất bằng JSON hợp lệ, không markdown, theo schema:
{{
  "headline": "1 câu nhận định chính, tối đa 18 từ",
  "improvements": ["3 gợi ý có thể cải thiện"],
  "fixed_context": ["3 yếu tố bối cảnh/khó can thiệp hoặc cần theo dõi"],
  "warnings": ["3 lý do vận hành đang cảnh báo"],
  "actions": ["3 hành động quản lý có thể làm ngay"]
}}
Context: {json.dumps(context, ensure_ascii=False)}
"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=700,
        )
        content = response.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?|```$", "", content, flags=re.MULTILINE).strip()
        data = json.loads(content)
        for key in ["headline", "improvements", "fixed_context", "warnings", "actions"]:
            if key not in data:
                raise ValueError(f"Missing key: {key}")
        data["source"] = "AI"
        return data
    except Exception as exc:
        fallback["source"] = f"DYNAMIC_AI_ERROR: {exc}"
        return fallback


def render_ai_ops_insight(insight: dict) -> str:
    source_text = "Nhận định từ dữ liệu hiện tại"
    improvements = "".join(f"<div>✓ {html_escape(item)}</div>" for item in insight.get("improvements", [])[:3])
    fixed = "".join(f"<div>• {html_escape(item)}</div>" for item in insight.get("fixed_context", [])[:3])
    warnings = "".join(f"<div style='margin-bottom: 6px;'>⚠ {html_escape(item)}</div>" for item in insight.get("warnings", [])[:3])
    return f"""
    <div class="manager-card alert-card-full" style="border-left: 5px solid #2563EB; background: #EFF6FF; min-height: auto; padding: 16px;">
        <div class="card-kicker" style="color: #2563EB; font-weight: 800; margin-bottom: 6px;">NHẬN ĐỊNH ĐIỀU HÀNH</div>
        <div style="font-size:10.5px;color:#64748B;font-weight:700;margin-bottom:8px;text-transform:uppercase;">{html_escape(source_text)}</div>
        <div class="card-title" style="font-size: 15px; margin-bottom: 12px; color: #1E40AF; font-weight: 800; line-height: 1.3;">{html_escape(insight.get("headline", ""))}</div>
        <div style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 14px; text-align: left; font-size: 12px; color: #1E40AF; line-height: 1.5;">
            <div><strong style="display:block;margin-bottom:4px;font-size:13px;">Có thể cải thiện</strong>{improvements}</div>
            <div><strong style="display:block;margin-bottom:4px;font-size:13px;">Bối cảnh cần theo dõi</strong>{fixed}</div>
        </div>
    </div>
    <div class="manager-card alert-card-full" style="border-left: 5px solid #EA580C; background: #FFF7ED; margin-top: 15px; min-height: auto;">
        <div class="card-kicker" style="color: #C2410C; font-weight: 800;">LÝ DO HỆ THỐNG CẢNH BÁO</div>
        <div style="text-align: left; font-size: 12.5px; color: #7C2D12; line-height: 1.55; font-weight: 500;">{warnings}</div>
    </div>
    """


def render_ai_action_cards(insight: dict):
    st.markdown(
        """
        <div style="background:#F8FAFC;border-left:5px solid #2563EB;border-radius:8px;padding:14px 16px;margin:16px 0 8px 0;">
            <div style="font-size:11px;color:#1E40AF;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;">Hành động quản lý nên làm ngay</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    action_items = [str(item) for item in insight.get("actions", [])[:3]]
    cols = st.columns(len(action_items) or 1)
    for col, item in zip(cols, action_items):
        with col:
            st.markdown(
                f"""
                <div style="background:white;border-radius:6px;padding:13px 14px;border:1px solid #DBEAFE;min-height:92px;">
                    <div style="font-size:12.5px;color:#1E3A8A;line-height:1.45;">{html_escape(item)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def build_time_where(period_name: str):
    if period_name == "Hôm nay (31/01/2018)":
        current = "order_date >= '2018-01-31 00:00:00' AND order_date <= '2018-01-31 23:38:00'"
        previous = "order_date >= '2018-01-30 00:00:00' AND order_date < '2018-01-31 00:00:00'"
        label = "hôm qua"
    elif period_name == "Ca trực hiện tại (22:00 - 06:00)":
        current = "order_date >= '2018-01-31 22:00:00' AND order_date <= '2018-01-31 23:38:00'"
        previous = "order_date >= '2018-01-31 14:00:00' AND order_date < '2018-01-31 22:00:00'"
        label = "ca trước"
    else: # "24 giờ qua"
        current = "order_date >= '2018-01-30 23:38:00' AND order_date <= '2018-01-31 23:38:00'"
        previous = "order_date >= '2018-01-29 23:38:00' AND order_date < '2018-01-30 23:38:00'"
        label = "24h trước"
    return current, previous, label


def build_where(period_name, region, shipping, category, focus_mode):
    current_cond, _, _ = build_time_where(period_name)
    conds = [current_cond]
    if region != "Tất cả":
        conds.append(f"order_region = '{sql_escape(region)}'")
    if shipping != "Tất cả":
        conds.append(f"shipping_mode = '{sql_escape(shipping)}'")
    if category != "Tất cả":
        conds.append(f"category_name = '{sql_escape(category)}'")
    if focus_mode == "Chỉ đơn trễ / rủi ro trễ":
        conds.append("late_delivery_risk = 1")
    return " AND ".join(conds)


def build_previous_where(period_name, region, shipping, category, focus_mode):
    _, previous_cond, _ = build_time_where(period_name)
    conds = [previous_cond]
    if region != "Tất cả":
        conds.append(f"order_region = '{sql_escape(region)}'")
    if shipping != "Tất cả":
        conds.append(f"shipping_mode = '{sql_escape(shipping)}'")
    if category != "Tất cả":
        conds.append(f"category_name = '{sql_escape(category)}'")
    if focus_mode == "Chỉ đơn trễ / rủi ro trễ":
        conds.append("late_delivery_risk = 1")
    return " AND ".join(conds)


def build_trend_context(period_name, available_years, region, shipping, category, focus_mode):
    current_where = build_where(period_name, region, shipping, category, focus_mode)
    previous_where = build_previous_where(period_name, region, shipping, category, focus_mode)
    _, _, label = build_time_where(period_name)
    return {
        "current_where": current_where,
        "previous_where": previous_where,
        "base_where": "1=1",
        "label": label,
    }


token = secret_value("MOTHERDUCK_TOKEN")
if not token:
    st.warning("Chưa có khóa kết nối dữ liệu. Nhập khóa để mở bảng điều hành.")
    token = st.text_input("Khóa kết nối dữ liệu", type="password")
    if not token:
        st.stop()

con = get_connection(token)

if "processed_orders" not in st.session_state:
    st.session_state["processed_orders"] = set()
if "selected_priority_idx" not in st.session_state:
    st.session_state["selected_priority_idx"] = None
if "pending_modal" not in st.session_state:
    st.session_state["pending_modal"] = None

# Modal duoc render o day - dau moi lan chay script - CHU KHONG render ngay
# tai noi bam nut. Neu render + st.rerun() trong cung 1 lan chay, rerun co the
# xay ra truoc khi trinh duyet kip load xong iframe cua components.html, khien
# modal khong hien (phai bam nhieu lan moi "an may" hien duoc). Tach rieng:
# nut bam chi luu cờ vao session_state["pending_modal"] roi rerun; modal duoc
# ve o lan chay KE TIEP, khi khong con rerun nao chen ngang nua.
if st.session_state["pending_modal"]:
    _modal = st.session_state["pending_modal"]
    show_centered_modal(_modal["title"], _modal["message"])
    st.session_state["pending_modal"] = None



@st.cache_data(ttl=1800)
def filter_options():
    years = con.execute(f"SELECT DISTINCT order_year FROM {BASE_TABLE} ORDER BY 1 DESC").df()["order_year"].dropna().astype(int).tolist()
    regions = con.execute(f"SELECT DISTINCT order_region FROM {BASE_TABLE} ORDER BY 1").df()["order_region"].dropna().tolist()
    shipping_modes = con.execute(f"SELECT DISTINCT shipping_mode FROM {BASE_TABLE} ORDER BY 1").df()["shipping_mode"].dropna().tolist()
    categories = con.execute(f"SELECT DISTINCT category_name FROM {BASE_TABLE} ORDER BY 1").df()["category_name"].dropna().tolist()
    return years, regions, shipping_modes, categories


@st.cache_data(ttl=900)
def query_summary(where_clause: str):
    return con.execute(
        f"""
        SELECT
            SUM(sales_amount) AS revenue,
            SUM(profit) AS profit,
            COUNT(DISTINCT order_id) AS orders,
            COUNT(DISTINCT CASE WHEN late_delivery_risk = 1 THEN order_id END) AS late_orders,
            SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
            AVG(days_for_shipping_real - days_for_shipment_scheduled) AS sla_gap,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate,
            COUNT(DISTINCT CASE WHEN order_status LIKE '%CANCEL%' THEN order_id END) * 100.0
                / NULLIF(COUNT(DISTINCT order_id), 0) AS cancel_rate,
            AVG(discount) AS avg_discount,
            COUNT(DISTINCT CASE WHEN (days_for_shipping_real - days_for_shipment_scheduled) * 24 > 12 THEN order_id END) AS over_12h_late_orders
        FROM {BASE_TABLE}
        WHERE {where_clause}
        """
    ).df()


@st.cache_data(ttl=900)
def query_priority(where_clause: str):
    return con.execute(
        f"""
        SELECT
            order_region,
            shipping_mode,
            category_name,
            COUNT(DISTINCT order_id) AS orders,
            COUNT(DISTINCT CASE WHEN late_delivery_risk = 1 THEN order_id END) AS late_orders,
            SUM(sales_amount) AS revenue,
            SUM(profit) AS profit,
            SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
            AVG(days_for_shipping_real - days_for_shipment_scheduled) AS sla_gap,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate,
            SUM(profit) * 100.0 / NULLIF(SUM(sales_amount), 0) AS margin
        FROM {BASE_TABLE}
        WHERE {where_clause}
        GROUP BY 1, 2, 3
        ORDER BY revenue_at_risk DESC, late_rate DESC
        LIMIT 12
        """
    ).df()


@st.cache_data(ttl=900)
def query_priority_trend(current_where: str, previous_where: str):
    return con.execute(
        f"""
        WITH curr AS (
            SELECT
                order_region,
                shipping_mode,
                category_name,
                SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0) AS current_late_rate
            FROM {BASE_TABLE}
            WHERE {current_where}
            GROUP BY 1, 2, 3
        ),
        prev AS (
            SELECT
                order_region,
                shipping_mode,
                category_name,
                SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0) AS previous_late_rate
            FROM {BASE_TABLE}
            WHERE {previous_where}
            GROUP BY 1, 2, 3
        )
        SELECT 
            COALESCE(curr.order_region, prev.order_region) AS order_region,
            COALESCE(curr.shipping_mode, prev.shipping_mode) AS shipping_mode,
            COALESCE(curr.category_name, prev.category_name) AS category_name,
            curr.current_late_rate,
            prev.previous_late_rate
        FROM curr
        FULL OUTER JOIN prev 
          ON curr.order_region = prev.order_region 
         AND curr.shipping_mode = prev.shipping_mode 
         AND curr.category_name = prev.category_name
        """
    ).df()


@st.cache_data(ttl=900)
def query_hourly_queue(where_clause: str):
    return con.execute(
        f"""
        SELECT 
            HOUR(order_date) AS hour_of_day,
            COUNT(DISTINCT order_id) AS queue_size,
            COUNT(DISTINCT CASE WHEN late_delivery_risk = 1 THEN order_id END) AS late_queue_size
        FROM {BASE_TABLE}
        WHERE {where_clause}
        GROUP BY 1
        ORDER BY 1
        """
    ).df()


@st.cache_data(ttl=900)
def query_priority_orders(where_clause: str, region: str, shipping: str, category: str):
    return con.execute(
        f"""
        SELECT
            order_id,
            customer_id,
            category_name,
            product_name,
            shipping_mode,
            order_region,
            order_country,
            sales_amount,
            profit,
            delivery_status,
            days_for_shipping_real,
            days_for_shipment_scheduled,
            days_for_shipping_real - days_for_shipment_scheduled AS delay_days
        FROM {BASE_TABLE}
        WHERE {where_clause}
          AND order_region = '{sql_escape(region)}'
          AND shipping_mode = '{sql_escape(shipping)}'
          AND category_name = '{sql_escape(category)}'
          AND late_delivery_risk = 1
        ORDER BY sales_amount DESC
        LIMIT 200
        """
    ).df()


@st.cache_data(ttl=900)
def query_monthly(where_clause: str):
    try:
        return con.execute(
            f"""
            SELECT
                order_year || '-' || LPAD(order_month::VARCHAR, 2, '0') AS month,
                SUM(sales_amount) AS revenue,
                SUM(profit) AS profit,
                SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
                SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate,
                AVG(days_for_shipping_real - days_for_shipment_scheduled) AS sla_gap
            FROM {BASE_TABLE}
            WHERE {where_clause}
            GROUP BY 1
            ORDER BY 1
            """
        ).df()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=900)
def query_product(where_clause: str):
    return con.execute(
        f"""
        SELECT
            department_name,
            category_name,
            COUNT(DISTINCT order_id) AS orders,
            SUM(sales_amount) AS revenue,
            SUM(profit) AS profit,
            SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate,
            SUM(profit) * 100.0 / NULLIF(SUM(sales_amount), 0) AS margin
        FROM {BASE_TABLE}
        WHERE {where_clause}
        GROUP BY 1, 2
        ORDER BY revenue_at_risk DESC
        LIMIT 10
        """
    ).df()


@st.cache_data(ttl=900)
def query_shipping(where_clause: str):
    return con.execute(
        f"""
        SELECT
            shipping_mode,
            COUNT(DISTINCT order_id) AS orders,
            SUM(sales_amount) AS revenue,
            SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate,
            AVG(days_for_shipping_real - days_for_shipment_scheduled) AS sla_gap
        FROM {BASE_TABLE}
        WHERE {where_clause}
        GROUP BY 1
        ORDER BY revenue_at_risk DESC
        """
    ).df()


@st.cache_data(ttl=900)
def query_matrix(where_clause: str):
    return con.execute(
        f"""
        SELECT
            order_region,
            shipping_mode,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate,
            SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk
        FROM {BASE_TABLE}
        WHERE {where_clause}
        GROUP BY 1, 2
        """
    ).df()


@st.cache_data(ttl=900)
def query_delivery_status(where_clause: str):
    return con.execute(
        f"""
        SELECT
            delivery_status,
            COUNT(DISTINCT order_id) AS orders,
            SUM(sales_amount) AS revenue,
            SUM(profit) AS profit
        FROM {BASE_TABLE}
        WHERE {where_clause}
        GROUP BY 1
        ORDER BY orders DESC
        """
    ).df()


@st.cache_data(ttl=900)
def query_ml_signals(where_clause: str):
    try:
        risk = con.execute(
            f"""
            SELECT
                COUNT(DISTINCT m.order_id) AS predicted_risk_orders,
                AVG(m.predicted_probability) * 100 AS avg_predicted_risk
            FROM {ML_TABLE} m
            JOIN {BASE_TABLE} b ON m.order_id = b.order_id
            WHERE m.predicted_label = 1 AND {where_clause}
            """
        ).df()
        features = con.execute(
            f"""
            SELECT feature, importance_score
            FROM {ML_FEATURE_TABLE}
            ORDER BY importance_score DESC
            LIMIT 6
            """
        ).df()
        return risk, features
    except Exception:
        return pd.DataFrame(), pd.DataFrame()


@st.cache_data(ttl=900)
def query_cost_benefit(where_clause: str):
    try:
        return con.execute(
            f"""
            WITH scoped AS (
                SELECT
                    order_region,
                    category_name,
                    shipping_mode,
                    COUNT(DISTINCT order_id) AS orders,
                    COUNT(DISTINCT CASE WHEN late_delivery_risk = 1 THEN order_id END) AS late_orders,
                    SUM(sales_amount) AS revenue,
                    SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
                    SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate
                FROM {BASE_TABLE}
                WHERE {where_clause}
                GROUP BY 1, 2, 3
            ),
            standard AS (
                SELECT *
                FROM scoped
                WHERE shipping_mode = 'Standard Class'
                  AND late_orders > 0
                  AND late_rate >= 45
            ),
            -- Use full historical benchmark for alternative shipping modes (not filtered to current shift)
            -- to get stable, representative late rates for each region+category combination
            historical_alternatives AS (
                SELECT
                    order_region,
                    category_name,
                    MAX(CASE WHEN shipping_mode = 'Second Class'
                        THEN SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) END) AS second_late_rate,
                    MAX(CASE WHEN shipping_mode = 'First Class'
                        THEN SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) END) AS first_late_rate
                FROM {BASE_TABLE}
                WHERE shipping_mode IN ('Second Class', 'First Class')
                GROUP BY order_region, category_name, shipping_mode
            ),
            alternatives AS (
                SELECT
                    order_region,
                    category_name,
                    MAX(second_late_rate) AS second_late_rate,
                    MAX(first_late_rate)  AS first_late_rate
                FROM historical_alternatives
                GROUP BY 1, 2
            )
            SELECT
                s.order_region,
                s.category_name,
                s.orders,
                s.late_orders,
                s.revenue,
                s.revenue_at_risk,
                s.late_rate AS standard_late_rate,
                a.second_late_rate,
                a.first_late_rate
            FROM standard s
            LEFT JOIN alternatives a USING (order_region, category_name)
            ORDER BY s.revenue_at_risk DESC, s.late_rate DESC
            LIMIT 40
            """
        ).df()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=900)
def query_high_risk_ml_orders(where_clause: str):
    try:
        return con.execute(
            f"""
            WITH base_filtered AS (
                SELECT
                    order_id,
                    ANY_VALUE(order_region) AS order_region,
                    STRING_AGG(DISTINCT category_name, ', ') AS category_name,
                    ANY_VALUE(shipping_mode) AS shipping_mode,
                    SUM(sales_amount) AS sales_amount,
                    SUM(profit) AS profit,
                    AVG(days_for_shipping_real) AS days_for_shipping_real,
                    AVG(days_for_shipment_scheduled) AS days_for_shipment_scheduled,
                    ANY_VALUE(order_date) AS order_date
                FROM {BASE_TABLE}
                WHERE {where_clause}
                GROUP BY order_id
            ),
            ml_filtered AS (
                SELECT
                    order_id,
                    MAX(predicted_probability) AS predicted_probability,
                    MAX(predicted_label) AS predicted_label,
                    MAX(actual) AS actual,
                    MAX(created_at) AS created_at
                FROM {ML_TABLE}
                GROUP BY order_id
            ),
            rec_filtered AS (
                SELECT
                    order_id,
                    priority,
                    reason,
                    recommended_action,
                    estimated_benefit
                FROM {ML_REC_TABLE}
            )
            SELECT
                b.order_id,
                b.order_region,
                b.category_name,
                b.shipping_mode,
                b.sales_amount,
                b.profit,
                b.days_for_shipping_real,
                b.days_for_shipment_scheduled,
                b.order_date,
                m.predicted_probability * 100 AS predicted_risk_pct,
                m.predicted_label,
                m.actual,
                m.created_at,
                r.priority,
                r.reason,
                r.recommended_action,
                r.estimated_benefit
            FROM ml_filtered m
            JOIN base_filtered b ON b.order_id = m.order_id
            JOIN rec_filtered r ON b.order_id = r.order_id
            WHERE m.predicted_probability >= 0.80
            ORDER BY m.predicted_probability DESC, b.sales_amount DESC
            LIMIT 25
            """
        ).df()
    except Exception:
        return pd.DataFrame()


def translate_ml_rec(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    p_map = {
        "Critical": "🔴 Khẩn cấp",
        "High": "🟠 Cao",
        "Medium": "🟡 Trung bình",
        "Low": "🟢 Thấp"
    }
    if "priority" in df.columns:
        df["priority"] = df["priority"].map(lambda x: p_map.get(x, x))
    r_map = {
        "Shipping Mode": "Phương thức vận chuyển",
        "Order Type": "Loại đơn hàng",
        "Order Weekday": "Ngày trong tuần",
        "Order Month": "Tháng đặt hàng",
        "Customer Segment": "Phân khúc khách hàng",
        "EASTERN ASIA": "Đông Á",
        "SOUTHEAST ASIA": "Đông Nam Á",
        "SOUTH ASIA": "Nam Á",
        "WESTERN ASIA": "Tây Á",
        "EAST ASIA": "Đông Á",
        "US CA": "Mỹ - Bang CA",
        "PR": "Puerto Rico",
    }
    if "reason" in df.columns:
        df["reason"] = df["reason"].map(lambda x: r_map.get(x, x.title() if isinstance(x, str) else x))
    a_map = {
        "Upgrade Shipping": "Nâng cấp vận chuyển",
        "Notify Customer": "Thông báo khách hàng",
        "Warehouse Priority": "Ưu tiên kho bãi",
        "Optimize Schedule": "Tối ưu hóa lịch trình"
    }
    if "recommended_action" in df.columns:
        df["recommended_action"] = df["recommended_action"].map(lambda x: a_map.get(x, x))
    b_map = {
        "High": "Cao",
        "Medium": "Trung bình",
        "Low": "Thấp"
    }
    if "estimated_benefit" in df.columns:
        df["estimated_benefit"] = df["estimated_benefit"].map(lambda x: b_map.get(x, x))
    return df


@st.cache_data(ttl=900)
def query_top_states(where_clause: str):
    try:
        return con.execute(
            f"""
            SELECT
                customer_state,
                COUNT(DISTINCT order_id) AS orders,
                SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate,
                SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk
            FROM {BASE_TABLE}
            WHERE {where_clause}
            GROUP BY 1
            HAVING COUNT(DISTINCT order_id) >= 5
            ORDER BY revenue_at_risk DESC, late_rate DESC
            LIMIT 3
            """
        ).df()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=900)
def query_7day_trend(region: str, shipping: str, category: str, focus_mode: str):
    try:
        time_cond = "order_date >= '2018-01-25 00:00:00' AND order_date <= '2018-01-31 23:38:00'"
        conds = [time_cond]
        if region != "Tất cả":
            conds.append(f"order_region = '{sql_escape(region)}'")
        if shipping != "Tất cả":
            conds.append(f"shipping_mode = '{sql_escape(shipping)}'")
        if category != "Tất cả":
            conds.append(f"category_name = '{sql_escape(category)}'")
        if focus_mode == "Chỉ đơn trễ / rủi ro trễ":
            conds.append("late_delivery_risk = 1")
        where_clause = " AND ".join(conds)
        return con.execute(
            f"""
            SELECT
                CAST(order_date AS DATE) AS order_day,
                SUM(sales_amount) AS revenue,
                SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
                SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate
            FROM {BASE_TABLE}
            WHERE {where_clause}
            GROUP BY 1
            ORDER BY 1
            """
        ).df()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=900)
def query_shipping_roi(where_clause: str):
    try:
        return con.execute(
            f"""
            SELECT
                shipping_mode,
                SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) AS revenue_at_risk,
                COUNT(DISTINCT CASE WHEN late_delivery_risk = 1 THEN order_id END) AS late_orders,
                SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END) / NULLIF(COUNT(DISTINCT CASE WHEN late_delivery_risk = 1 THEN order_id END), 0) AS avg_revenue_per_order
            FROM {BASE_TABLE}
            WHERE {where_clause}
            GROUP BY 1
            ORDER BY revenue_at_risk DESC
            """
        ).df()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=900)
def query_unstructured_status():
    try:
        return con.execute(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE lower(table_name) LIKE '%access%'
               OR lower(table_name) LIKE '%click%'
               OR lower(table_name) LIKE '%log%'
               OR lower(table_name) LIKE '%description%'
            ORDER BY table_schema, table_name
            """
        ).df()
    except Exception:
        return pd.DataFrame()


def apply_chart_theme(fig, height=None):
    fig.update_layout(
        font=dict(family="Inter, 'Segoe UI', sans-serif", color="#374151", size=12),
        title=dict(font=dict(color="#111827", size=14), x=0, xanchor="left"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=22, r=18, t=68, b=40),
        colorway=["#2563EB", "#10B981", "#D97706", "#DC2626", "#64748B"],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.10,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E5E7EB", zeroline=False, tickfont=dict(size=11))
    fig.update_yaxes(showgrid=True, gridcolor="#EEF2F7", linecolor="#E5E7EB", zeroline=False, tickfont=dict(size=11))
    if height:
        fig.update_layout(height=height)
    return fig


def make_auto_chart(df: pd.DataFrame, title: str):
    if df.empty:
        return None
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    text_cols = [c for c in df.columns if c not in numeric_cols]
    if len(df) <= 1 or not numeric_cols:
        return None
    if text_cols:
        x_col = text_cols[0]
        y_col = numeric_cols[0]
        if "month" in x_col.lower() or "date" in x_col.lower():
            fig = px.line(df, x=x_col, y=y_col, markers=True, title=title)
        else:
            fig = px.bar(df.head(12), x=x_col, y=y_col, title=title)
        return apply_chart_theme(fig, 360)
    fig = px.line(df[numeric_cols].reset_index(), x="index", y=numeric_cols[0], title=title)
    return apply_chart_theme(fig, 360)


DISPLAY_COLUMN_LABELS = {
    "order_id": "Mã đơn hàng",
    "customer_id": "Mã khách hàng",
    "product_name": "Sản phẩm",
    "shipping_mode": "Phương thức vận chuyển",
    "revenue_at_risk": "Doanh thu đang gặp rủi ro",
    "sales_amount": "Doanh thu",
    "profit": "Lợi nhuận",
    "late_rate": "Tỷ lệ trễ (%)",
    "orders": "Số đơn",
    "late_orders": "Đơn trễ",
    "category_name": "Danh mục sản phẩm",
    "department_name": "Bộ phận",
    "order_region": "Khu vực",
    "order_country": "Quốc gia",
    "order_city": "Thành phố",
    "customer_segment": "Nhóm khách hàng",
    "delivery_status": "Trạng thái giao hàng",
    "days_for_shipping_real": "Số ngày giao thực tế",
    "days_for_shipment_scheduled": "Số ngày cam kết",
    "delay_days": "Độ lệch lịch hẹn",
    "sla_gap": "Độ lệch lịch hẹn",
    "margin": "Biên lợi nhuận (%)",
    "predicted_probability": "Mức cảnh báo",
    "predicted_label": "Trạng thái cảnh báo",
}


def rename_for_display(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={col: DISPLAY_COLUMN_LABELS.get(col, col) for col in df.columns})


def is_safe_select(sql: str) -> bool:
    cleaned = sql.strip().rstrip(";").strip()
    lowered = cleaned.lower()
    if not (lowered.startswith("select") or lowered.startswith("with")):
        return False
    blocked = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "create ",
        "attach ",
        "detach ",
        "copy ",
        "export ",
        "pragma ",
        "grant ",
        "truncate ",
    ]
    if any(word in lowered for word in blocked):
        return False
    allowed = [
        BASE_TABLE,
        ML_TABLE,
        ML_PERFORMANCE_TABLE,
        ML_FEATURE_TABLE,
        ML_REC_TABLE,
    ]
    return any(table.lower() in lowered for table in allowed)


def sql_quality_notes(sql: str):
    lowered = (sql or "").lower()
    notes = []
    if "count(*)" in lowered and "distinct order_id" not in lowered:
        notes.append("Truy vấn có COUNT(*). Nếu câu hỏi đang hỏi số đơn hàng, cần kiểm tra để tránh đếm dòng sản phẩm thay vì đơn hàng.")
    if "select *" in lowered:
        notes.append("Truy vấn dùng SELECT *. Nên kiểm tra lại các cột cần dùng trước khi trích xuất hoặc chia sẻ kết quả.")
    if "limit" not in lowered and "group by" not in lowered:
        notes.append("Truy vấn không có LIMIT hoặc GROUP BY. Cần kiểm tra quy mô dữ liệu trả về.")
    return notes


def extract_sql(text: str) -> str:
    match = re.search(r"```sql\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\s*(.*?)```", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def extract_no_matching_column(text: str):
    """
    Bat tin hieu tu choi cua model khi cau hoi nhac den mot khai niem/thuoc tinh
    KHONG co cot tuong ung trong schema (vi du: hoi 'phuong thuc thanh toan'
    trong khi du lieu chi co 'phuong thuc van chuyen'). Neu khong co bo chan
    nay, model co xu huong tu dong thay the bang cot gan giong ve ten/nghia va
    tra loi mot cach tu tin nhu the da tra loi dung, gay hieu nham nghiem trong
    hon ca loi ky thuat thong thuong (silent misinterpretation).
    Tra ve mo ta khai niem khong co du lieu neu phat hien, nguoc lai tra ve None.
    """
    match = re.search(r"NO_MATCHING_COLUMN\s*:\s*(.+)", text, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip().strip("`").strip()
    return None


SCHEMA_CONTEXT = f"""
Bạn là chuyên gia Auto-SQL cho DuckDB. Chỉ được sinh SELECT/WITH an toàn.

Bảng vận hành chính: {BASE_TABLE}
Cột: order_id, order_item_id, customer_id, customer_segment, customer_state, customer_country,
product_name, category_name, department_name, product_price, order_item_quantity,
sales_amount, profit, discount, shipping_mode, days_for_shipping_real,
days_for_shipment_scheduled, late_delivery_risk, delivery_status, market,
order_region, order_city, order_state, order_country, latitude, longitude,
order_date, shipping_date, order_year, order_month, order_quarter, order_weekday,
order_status, order_type.

Bảng dự báo AI: {ML_TABLE}
Cột: order_id, shipping_mode, customer_state, order_type, order_region,
order_weekday, order_month, customer_segment, actual, predicted_probability,
predicted_label, created_at, shap_shipping_mode, shap_customer_state,
shap_order_type, shap_order_region, shap_order_weekday, shap_order_month,
shap_customer_segment.

Bảng hiệu suất mô hình: {ML_PERFORMANCE_TABLE}
Cột: model_name, auc, f1, best_threshold, created_at.

Khi người dùng hỏi về 'Yếu tố ảnh hưởng nhiều nhất đến dự đoán trễ', 'Phân tích SHAP', 'Mức độ quan trọng của đặc trưng (Feature Importance)', hoặc 'Những yếu tố nào ảnh hưởng nhiều nhất đến dự đoán giao hàng trễ', bạn phải truy vấn từ bảng: {ML_TABLE}
Bảng này chứa giá trị SHAP đóng góp vào rủi ro trễ đơn hàng của từng yếu tố (giá trị dương làm tăng rủi ro, giá trị âm làm giảm rủi ro).
Khi người dùng hỏi chung về 'những yếu tố ảnh hưởng nhiều nhất đến dự đoán giao hàng trễ', bản chất của họ là muốn xem tổng thể tầm quan trọng của đặc trưng (Global Feature Importance). Bạn phải thực hiện lệnh SELECT tính trung bình trị tuyệt đối AVG(ABS(shap_...)) cho toàn bộ các cột đóng góp mô hình của bảng giải thích dữ liệu {ML_TABLE} giống như câu hỏi Top đặc trưng!
Để tính mức độ ảnh hưởng tổng thể của các yếu tố, bạn cần dùng hàm tính TRUNG BÌNH GIÁ TRỊ TUYỆT ĐỐI (AVG(ABS(...))) cho các cột SHAP sau đây:
- shap_shipping_mode (Đóng góp của Phương thức vận chuyển)
- shap_customer_state (Đóng góp của Bang của khách hàng)
- shap_order_type (Đóng góp của Loại đơn hàng)
- shap_order_region (Đóng góp của Khu vực đặt hàng)
- shap_order_weekday (Đóng góp của Ngày trong tuần)
- shap_order_month (Đóng góp của Tháng đặt hàng)
- shap_customer_segment (Đóng góp của Phân khúc khách hàng)

Ví dụ câu lệnh mẫu để tìm Top đặc trưng quan trọng nhất:
SELECT 'Phương thức vận chuyển' AS feature_name, AVG(ABS(shap_shipping_mode)) AS importance FROM {ML_TABLE}
UNION ALL
SELECT 'Bang của khách hàng', AVG(ABS(shap_customer_state)) FROM {ML_TABLE}
UNION ALL
SELECT 'Loại đơn hàng', AVG(ABS(shap_order_type)) FROM {ML_TABLE}
UNION ALL
SELECT 'Khu vực đặt hàng', AVG(ABS(shap_order_region)) FROM {ML_TABLE}
UNION ALL
SELECT 'Ngày trong tuần', AVG(ABS(shap_order_weekday)) FROM {ML_TABLE}
UNION ALL
SELECT 'Tháng đặt hàng', AVG(ABS(shap_order_month)) FROM {ML_TABLE}
UNION ALL
SELECT 'Phân khúc khách hàng', AVG(ABS(shap_customer_segment)) FROM {ML_TABLE}
ORDER BY importance DESC;

Quy tắc:
- Chỉ dùng đúng tên bảng/cột trên.
- QUAN TRỌNG - CẤP ĐỘ DỮ LIỆU: Bảng {BASE_TABLE} lưu ở cấp ORDER ITEM (từng mặt hàng), KHÔNG phải cấp Order. Một order_id có thể có nhiều dòng (nhiều sản phẩm). Vì vậy:
  * Đếm số đơn hàng: COUNT(DISTINCT order_id), KHÔNG dùng COUNT(*).
  * Liệt kê đơn hàng cụ thể: LUÔN GROUP BY order_id và SUM() các cột số (sales_amount, profit) để tránh trùng lặp.
  * Lấy thông tin cố định theo đơn: dùng ANY_VALUE(shipping_mode), ANY_VALUE(order_region), ANY_VALUE(order_date).
- "Doanh thu đang gặp rủi ro" hoặc "Doanh thu cần bảo vệ" nghĩa là SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END).
- "Tỷ lệ giao trễ" nghĩa là SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*).
- "Biên lợi nhuận" hoặc "Biên lợi nhuận (%)" nghĩa là SUM(profit) * 100.0 / SUM(sales_amount).
- "Tỷ lệ đơn hàng bị dự đoán trễ" hoặc "tỷ lệ bị dự đoán trễ" nghĩa là SUM(predicted_label) * 100.0 / COUNT(*).
- Với câu hỏi về doanh thu, lợi nhuận, biên lợi nhuận, giao hàng (thực tế), sản phẩm, khu vực, dùng bảng vận hành chính {BASE_TABLE}.
- Với câu hỏi liên quan đến 'dự đoán', 'dự báo', 'bị dự đoán trễ', 'predicted', 'xác suất', 'SHAP', 'tầm quan trọng đặc trưng', dùng bảng dự báo AI {ML_TABLE}.
- Với câu hỏi về "đơn cần điều phối gấp", "xác suất trễ trên 80%", hoặc "đơn rủi ro cao", JOIN {ML_TABLE} với {BASE_TABLE} bằng order_id, lọc predicted_probability >= 0.80, sắp xếp theo predicted_probability DESC và sales_amount DESC.
- Với câu hỏi về "đổi shipping_mode", "Standard Class sang Second/First Class", hoặc "ngân sách điều tốc", ưu tiên phân tích các nhóm order_region + category_name đang dùng Standard Class có late_rate cao và revenue_at_risk lớn.
- Thêm LIMIT 50 nếu kết quả không phải tổng hợp một dòng.
- Chỉ trả về duy nhất SQL trong ```sql ... ```.
MẸO NHẬN BIẾT CÂU HỎI CỦA NGƯỜI DÙNG:
- Khi người dùng hỏi: "Những yếu tố nào ảnh hưởng nhiều nhất đến dự đoán giao hàng trễ?" hoặc "Yếu tố nào tác động lớn nhất đến rủi ro trễ?", bản chất họ đang hỏi về Tầm quan trọng của đặc trưng tổng thể (Global Feature Importance).
- Bạn PHẢI viết câu lệnh SELECT tính TRUNG BÌNH GIÁ TRỊ TUYỆT ĐỐI (AVG(ABS(...))) của các cột SHAP trong bảng `{ML_TABLE}`.

Tuyệt đối KHÔNG TRUY VẤN bảng `stg_supplychain_v2` hay tính toán late_delivery_risk cho câu hỏi này, vì đây là câu hỏi giải thích mô hình Machine Learning!

QUY TẮC BẮT BUỘC VỀ PHẠM VI DỮ LIỆU (chống bịa cột/diễn giải sai):
- Bạn CHỈ được dùng đúng các cột đã liệt kê ở trên. TUYỆT ĐỐI KHÔNG được tự suy diễn, đổi tên, hoặc thay thế bằng một cột "gần giống về nghĩa" khi khái niệm người dùng hỏi không có cột tương ứng.
- Ví dụ SAI: người dùng hỏi "phương thức thanh toán" (payment method) nhưng dữ liệu không có cột này -> KHÔNG được tự động dùng shipping_mode (phương thức vận chuyển) để trả lời thay, vì đây là hai khái niệm nghiệp vụ khác nhau hoàn toàn.
- Nếu câu hỏi nhắc đến một khái niệm/thuộc tính/số liệu KHÔNG có cột tương ứng trong danh sách đã liệt kê (ví dụ: phương thức thanh toán, đánh giá/rating khách hàng, tồn kho, giá vốn, dự báo tương lai chưa xảy ra, v.v.), bạn KHÔNG được viết SQL. Thay vào đó, chỉ trả về DUY NHẤT một dòng theo đúng định dạng:
NO_MATCHING_COLUMN: <mô tả ngắn gọn khái niệm không có dữ liệu>
- Không thêm giải thích, không thêm SQL, không thêm ký tự nào khác ngoài dòng trên khi rơi vào trường hợp này.
"""


years, regions, shipping_modes, categories = filter_options()

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title">
            <h2>Điều hành chuỗi cung ứng</h2>
            <p>Theo dõi đơn hàng, giao hàng, lợi nhuận và các điểm cần xử lý trong phạm vi trực ca real-time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_period = st.selectbox(
        "Khoảng thời gian vận hành",
        [
            "Hôm nay (31/01/2018)",
            "Ca trực hiện tại (22:00 - 06:00)",
            "24 giờ qua"
        ],
        index=0
    )
    selected_region = st.selectbox("Khu vực", ["Tất cả"] + regions)
    selected_shipping = st.selectbox("Phương thức vận chuyển", ["Tất cả"] + shipping_modes)
    selected_category = st.selectbox("Danh mục sản phẩm", ["Tất cả"] + categories)
    selected_focus = st.radio(
        "Chế độ xem",
        ["Tất cả đơn hàng", "Chỉ đơn trễ / rủi ro trễ"],
        index=0,
    )
    st.caption(
        f"Phạm vi đang xem: {selected_period}; khu vực {selected_region}; "
        f"vận chuyển {selected_shipping}; danh mục {selected_category}; chế độ {selected_focus}."
    )
    if not secret_value("GROQ_API_KEY"):
        st.text_input("Khóa truy cập phần hỏi dữ liệu", type="password", key="groq_api_key")
    st.divider()
    st.caption("Nguồn dữ liệu: kho MotherDuck")


where_clause = build_where(selected_period, selected_region, selected_shipping, selected_category, selected_focus)
trend_context = build_trend_context(selected_period, years, selected_region, selected_shipping, selected_category, selected_focus)

summary_df = query_summary(where_clause)
summary = summary_df.iloc[0] if not summary_df.empty else pd.Series(dtype="object")

fallback_active = False
if summary_df.empty or safe_float(summary.get("orders")) == 0:
    fallback_active = True
    fallback_time_current = "order_date >= '2018-01-02 00:00:00' AND order_date <= '2018-01-31 23:38:00'"
    fallback_time_previous = "order_date >= '2017-12-03 00:00:00' AND order_date < '2018-01-02 00:00:00'"
    fallback_label = "30 ngày trước"
    
    def build_where_fallback(region, shipping, category, focus_mode):
        conds = [fallback_time_current]
        if region != "Tất cả":
            conds.append(f"order_region = '{sql_escape(region)}'")
        if shipping != "Tất cả":
            conds.append(f"shipping_mode = '{sql_escape(shipping)}'")
        if category != "Tất cả":
            conds.append(f"category_name = '{sql_escape(category)}'")
        if focus_mode == "Chỉ đơn trễ / rủi ro trễ":
            conds.append("late_delivery_risk = 1")
        return " AND ".join(conds)
        
    where_clause = build_where_fallback(selected_region, selected_shipping, selected_category, selected_focus)
    parts = where_clause.split(" AND ")
    other_conds = parts[1:] if len(parts) > 1 else []
    
    trend_context = {
        "current_where": where_clause,
        "previous_where": " AND ".join([fallback_time_previous] + other_conds),
        "base_where": "1=1",
        "label": fallback_label,
    }
    summary_df = query_summary(where_clause)
    summary = summary_df.iloc[0] if not summary_df.empty else pd.Series(dtype="object")

trend_current_df = query_summary(trend_context["current_where"]) if trend_context else pd.DataFrame()
trend_previous_df = query_summary(trend_context["previous_where"]) if trend_context else pd.DataFrame()
trend_current = trend_current_df.iloc[0] if not trend_current_df.empty else pd.Series(dtype="object")
trend_previous = trend_previous_df.iloc[0] if not trend_previous_df.empty else pd.Series(dtype="object")
priority_df = query_priority(where_clause)
if trend_context and not priority_df.empty:
    priority_trend_df = query_priority_trend(
        trend_context["current_where"],
        trend_context["previous_where"]
    )
    if not priority_trend_df.empty:
        priority_df = priority_df.merge(
            priority_trend_df,
            on=["order_region", "shipping_mode", "category_name"],
            how="left",
        )
        priority_df["late_rate_delta"] = priority_df["current_late_rate"] - priority_df["previous_late_rate"]
monthly_df = query_monthly(where_clause)
product_df = query_product(where_clause)
shipping_df = query_shipping(where_clause)
matrix_df = query_matrix(where_clause)
delivery_df = query_delivery_status(where_clause)
ml_risk_df, ml_features_df = query_ml_signals(where_clause)
cost_benefit_df = query_cost_benefit(where_clause)
high_risk_orders_df = query_high_risk_ml_orders(where_clause)
unstructured_df = query_unstructured_status()
hourly_queue_df = query_hourly_queue(where_clause)
top_states_df = query_top_states(where_clause)
shipping_roi_df = query_shipping_roi(where_clause)

revenue = safe_float(summary.get("revenue"))
profit = safe_float(summary.get("profit"))
orders = safe_float(summary.get("orders"))
late_orders = safe_float(summary.get("late_orders"))
revenue_at_risk = safe_float(summary.get("revenue_at_risk"))
sla_gap = safe_float(summary.get("sla_gap"))
late_rate = safe_float(summary.get("late_rate"))
cancel_rate = safe_float(summary.get("cancel_rate"))
avg_discount = safe_float(summary.get("avg_discount"))
over_12h_late_orders = safe_float(summary.get("over_12h_late_orders"))
margin = profit / revenue * 100 if revenue else 0
risk_share = revenue_at_risk / revenue * 100 if revenue else 0
sev_class, sev_label = severity(late_rate, risk_share, sla_gap)
target_late_rate = 10.0
late_target_ratio = late_rate / target_late_rate if target_late_rate else 0
target_compare_text = (
    f"cao gấp {late_target_ratio:.1f} lần so với mục tiêu ≤ {target_late_rate:.0f}%"
    if late_rate > target_late_rate and late_target_ratio
    else f"đang trong mục tiêu ≤ {target_late_rate:.0f}%"
)
compare_label = trend_context["label"] if trend_context else "kỳ trước"
trend_prefix = ""
revenue_delta_text = trend_prefix + fmt_delta_value(trend_current.get("revenue"), trend_previous.get("revenue"), fmt_money, compare_label)
profit_delta_text = trend_prefix + fmt_delta_value(trend_current.get("profit"), trend_previous.get("profit"), fmt_money, compare_label)
orders_delta_text = trend_prefix + fmt_delta_value(trend_current.get("orders"), trend_previous.get("orders"), fmt_num, compare_label)
late_delta_text = trend_prefix + fmt_delta_points(trend_current.get("late_rate"), trend_previous.get("late_rate"), compare_label)
risk_delta_text = trend_prefix + fmt_delta_value(trend_current.get("revenue_at_risk"), trend_previous.get("revenue_at_risk"), fmt_money, compare_label)
sla_delta_text = trend_prefix + fmt_delta_hours(trend_current.get("sla_gap"), trend_previous.get("sla_gap"), compare_label)
cancel_delta_text = trend_prefix + fmt_delta_points(trend_current.get("cancel_rate"), trend_previous.get("cancel_rate"), compare_label)
over_12h_delta_text = trend_prefix + fmt_delta_value(trend_current.get("over_12h_late_orders"), trend_previous.get("over_12h_late_orders"), fmt_num, compare_label)
data_window = selected_period

top_issue = priority_df.iloc[0] if not priority_df.empty else None
top_issue_name = describe_issue(top_issue)
top_issue_copy = (
    f"Nhóm này có {fmt_money(top_issue['revenue_at_risk'])} doanh thu đang gặp rủi ro nếu không xử lý, "
    f"tỷ lệ trễ {fmt_pct(top_issue['late_rate'])}, {fmt_delay_days(top_issue['sla_gap'])} so với lịch hẹn."
    if top_issue is not None
    else "Hãy nới bộ lọc hoặc chọn chế độ tất cả đơn hàng để xem lại thứ tự ưu tiên."
)

what_if_rows = []
if not cost_benefit_df.empty:
    for _, cb_row in cost_benefit_df.iterrows():
        for target_mode, rate_col in [("Second Class", "second_late_rate"), ("First Class", "first_late_rate")]:
            sim_target_late_rate = safe_float(cb_row.get(rate_col), None)
            if sim_target_late_rate is None:
                continue
            saved_revenue = estimate_saved_revenue(
                cb_row.get("revenue_at_risk"),
                cb_row.get("standard_late_rate"),
                sim_target_late_rate,
            )
            extra_cost = estimate_upgrade_cost(cb_row.get("revenue"), cb_row.get("orders"), target_mode)
            what_if_rows.append(
                {
                    "Nhóm cần quyết định": f"{cb_row['category_name']} tại {cb_row['order_region']}",
                    "Phương án": f"Standard → {target_mode}",
                    "Đơn bị ảnh hưởng": cb_row.get("orders"),
                    "Tỷ lệ trễ hiện tại (%)": cb_row.get("standard_late_rate"),
                    "Tỷ lệ trễ phương án (%)": sim_target_late_rate,
                    "Doanh thu rủi ro hiện tại": cb_row.get("revenue_at_risk"),
                    "Doanh thu rủi ro có thể bảo vệ": saved_revenue,
                    "Chi phí điều phối ước tính": extra_cost,
                    "Lợi ích ròng ước tính": saved_revenue - extra_cost,
                    "Khuyến nghị": "Nên cân nhắc đổi" if saved_revenue > extra_cost else "Không nên đổi nếu chỉ xét chi phí",
                }
            )
what_if_df = pd.DataFrame(what_if_rows)
if what_if_df is not None and not what_if_df.empty:
    what_if_df = what_if_df.sort_values("Lợi ích ròng ước tính", ascending=False).head(12)

# Executive Summary Calculations
if priority_df is not None and not priority_df.empty:
    region_risk_df = priority_df.groupby("order_region")["revenue_at_risk"].sum().reset_index()
    region_risk_df = region_risk_df.sort_values("revenue_at_risk", ascending=False)
    top_region_name = region_risk_df.iloc[0]["order_region"].title()
    top_region_risk = region_risk_df.iloc[0]["revenue_at_risk"]
else:
    top_region_name = "Không có dữ liệu"
    top_region_risk = 0.0

if not shipping_df.empty:
    shipping_risk_df = shipping_df.sort_values("revenue_at_risk", ascending=False)
    top_shipping_mode = shipping_risk_df.iloc[0]["shipping_mode"]
    top_shipping_risk = shipping_risk_df.iloc[0]["revenue_at_risk"]
else:
    top_shipping_mode = "Không có dữ liệu"
    top_shipping_risk = 0.0

if priority_df is not None and not priority_df.empty:
    category_risk_df = priority_df.groupby("category_name")["revenue_at_risk"].sum().reset_index()
    category_risk_df = category_risk_df.sort_values("revenue_at_risk", ascending=False)
    top_category_name = category_risk_df.iloc[0]["category_name"]
    top_category_risk = category_risk_df.iloc[0]["revenue_at_risk"]
else:
    top_category_name = "Không có dữ liệu"
    top_category_risk = 0.0

exposure_parts = []
if shipping_roi_df is not None and not shipping_roi_df.empty:
    total_late = shipping_roi_df["late_orders"].sum()
    if total_late > 0:
        sorted_roi = shipping_roi_df.sort_values("late_orders", ascending=False)
        for _, r in sorted_roi.iterrows():
            pct = r["late_orders"] / total_late * 100
            if pct >= 1.0:
                mode_short = r["shipping_mode"].replace(" Class", "")
                exposure_parts.append(f"{mode_short}: {pct:.0f}%")
exposure_text = " | ".join(exposure_parts) if exposure_parts else "Chưa có dữ liệu"

if fallback_active:
    st.warning("⚠️ Không có dữ liệu trong khoảng thời gian đã chọn. Hệ thống tự động chuyển sang dữ liệu dự phòng 30 ngày.")

st.markdown(
    f"""
    <div class="crisis-panel">
        <div class="crisis-kicker">Cảnh báo vận hành ca trực</div>
        <div class="crisis-title">{fmt_pct(late_rate)} đơn hàng có nguy cơ trễ hẹn</div>
        <p class="crisis-copy">
            Khu vực cần lưu ý chính là {html_escape(top_issue_name)}. 
            Độ lệch cam kết giao hàng trung bình hiện tại: {fmt_delay_hours_only(sla_gap)}. 
            Khoảng thời gian báo cáo: {data_window}.
        </p>
        <div class="crisis-metrics">
            <div class="crisis-metric"><b>{fmt_num(late_orders)}</b><span>Tổng số đơn trễ / nguy cơ trễ</span></div>
            <div class="crisis-metric"><b>{fmt_money(revenue_at_risk)}</b><span>Doanh thu rủi ro ({risk_delta_text})</span></div>
            <div class="crisis-metric"><b>{fmt_num(over_12h_late_orders)}</b><span>Số đơn trễ cam kết > 12 giờ</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if top_issue is not None:
    action_briefing = (
        f"✓ Đổi phương thức giao hàng: Tiêu chuẩn → Nhanh/Hỏa tốc<br/>"
        f"✓ Tăng tốc xử lý kho: nhóm {html_escape(top_category_name)}<br/>"
        f"✓ Kiểm tra bưu cục phụ trách: khu vực {html_escape(top_region_name)}"
    )
else:
    action_briefing = "✓ Các chỉ số vận hành ổn định<br/>✓ Đảm bảo SLA đóng gói ca trực"

# Sidebar briefing block removed

# Render Executive Summary Panel
# Prepare daily action briefing based on the top operational bottlenecks

section(1, "Tình hình hiện tại", "Các chỉ số chính để đánh giá mức độ ảnh hưởng và ưu tiên xử lý.")
st.markdown(
    f"""
    <div class="kpi-grid">
        {kpi_card("Tổng đơn hàng trong ca trực", fmt_num(orders), f"{orders_delta_text}; {fmt_num(late_orders)} đơn rủi ro cao", "blue")}
        {kpi_card("Tỷ lệ giao trễ", fmt_pct(late_rate), f"Mục tiêu ≤ {target_late_rate:.0f}%; {late_delta_text}", "red" if sev_class == "red" else "amber")}
        {kpi_card("Doanh thu rủi ro do trễ giao", fmt_full_money(revenue_at_risk), f"So với {compare_label}; {risk_delta_text}", "red" if revenue_at_risk > 5000 else "amber")}
        {kpi_card("Độ lệch cam kết giao hàng TB", fmt_delay_hours_only(sla_gap), f"Mục tiêu ≤ 0h; {sla_delta_text}", "red" if sla_gap > 0 else "green")}
        {kpi_card("Tổng doanh thu trong phạm vi lọc", fmt_full_money(revenue), revenue_delta_text, "blue")}
        {kpi_card("Tỷ lệ hủy", fmt_pct(cancel_rate), f"{cancel_delta_text}; giảm giá TB {fmt_money(avg_discount)}", "amber" if cancel_rate >= 3 else "green")}
    </div>
    """,
    unsafe_allow_html=True,
)
section(2, "Hành động ưu tiên và can thiệp ngay", "Tập trung điều phối nguồn lực cho các đơn hàng và tuyến đường rủi ro nhất.")

st.markdown(
    f"""
    <div style="background: #EFF6FF; border-left: 5px solid #2563EB; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
        <b style="color: #1E40AF; font-size: 14px; text-transform: uppercase; display: block; margin-bottom: 6px;">🎯 Chỉ đạo điều phối trong ca</b>
        <div style="font-size: 13px; line-height: 1.5; color: #1E3A8A;">
            {action_briefing}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    st.markdown("#### 🎯 Đơn cần xử lý ngay theo cảnh báo hệ thống")
    st.caption("Danh sách đơn có nguy cơ trễ cao, ưu tiên điều phối trong ca.")
    if high_risk_orders_df is not None and not high_risk_orders_df.empty:
        # Translate predictions with ML Recommendations columns
        high_risk_translated = translate_ml_rec(high_risk_orders_df)
        high_risk_translated["Thời gian còn lại"] = high_risk_translated.apply(calc_countdown_text, axis=1)
        
        # Mark processed status in Priority Column
        def get_priority_status(row):
            if row["order_id"] in st.session_state["processed_orders"]:
                return "Đã ghi nhận trong phiên"
            return row["priority"]
            
        high_risk_translated["Mức độ ưu tiên"] = high_risk_translated.apply(get_priority_status, axis=1)
        
        high_risk_display = high_risk_translated.rename(
            columns={
                "order_id": "Mã đơn",
                "sales_amount": "Doanh thu đơn",
                "predicted_risk_pct": "Mức cảnh báo trễ (%)",
                "reason": "Nguyên nhân chính",
                "recommended_action": "Hành động khuyến nghị",
                "estimated_benefit": "Lợi ích ước tính"
            }
        )
        
        cols_to_show = [
            "Mã đơn", "Mức độ ưu tiên", "Nguyên nhân chính", "Hành động khuyến nghị",
            "Lợi ích ước tính", "Mức cảnh báo trễ (%)", "Doanh thu đơn", "Thời gian còn lại"
        ]
        
        # Style table to dim processed orders (opacity effect via style styling)
        def style_processed_rows(row):
            val = row["Mức độ ưu tiên"]
            if "Đã ghi nhận" in str(val):
                return ["background-color: #F3F4F6; color: #9CA3AF; text-decoration: line-through;"] * len(row)
            return [""] * len(row)
            
        st.dataframe(
            high_risk_display[cols_to_show].style.apply(style_processed_rows, axis=1).format(
                {
                    "Doanh thu đơn": "${:,.0f}",
                    "Mức cảnh báo trễ (%)": "{:.1f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
            height=260,
        )
        st.download_button(
            "Xuất danh sách đơn rủi ro cao",
            data=high_risk_display.to_csv(index=False).encode("utf-8-sig"),
            file_name="don_ml_rui_ro_cao.csv",
            mime="text/csv",
            type="secondary",
            key="tải_csv_ml_rủi_ro_cao"
        )
    else:
        st.info("Không có đơn nào đạt ngưỡng cảnh báo trễ cao trong phạm vi lọc hiện tại.")

# Split layout: content on left (9), actions on right (3)
col_left, col_right = st.columns([9, 3])

# Resolve currently selected row
selected_idx = st.session_state.get("selected_priority_idx")
selected_row = None
if priority_df is not None and not priority_df.empty:
    if selected_idx is not None and selected_idx in priority_df.index:
        selected_row = priority_df.loc[selected_idx]

with col_left:
    if priority_df is not None and not priority_df.empty:
        # Guarantee checkbox states match selected_priority_idx on new filter loads
        for idx in priority_df.head(3).index:
            key = f"select_checkbox_{idx}"
            if key not in st.session_state:
                st.session_state[key] = (st.session_state.get("selected_priority_idx") == idx)

        for rank, (idx, row) in enumerate(priority_df.head(3).iterrows(), start=1):
            order_title = describe_issue(row)
            action_note = ""
            if what_if_df is not None and not what_if_df.empty:
                group_name = f"{row['category_name']} tại {row['order_region']}"
                candidate_actions = what_if_df[what_if_df["Nhóm cần quyết định"] == group_name]
                if not candidate_actions.empty:
                    best_action = candidate_actions.sort_values("Lợi ích ròng ước tính", ascending=False).iloc[0]
                    if safe_float(best_action.get("Lợi ích ròng ước tính")) > 0:
                        action_note = (
                            f" Phương án tham khảo theo giả định mặc định: {best_action['Phương án']} "
                            f"với lợi ích ròng ước tính {fmt_money(best_action['Lợi ích ròng ước tính'])}."
                        )
            order_copy = (
                f"{fmt_money(row['revenue_at_risk'])} doanh thu đang gặp rủi ro nếu không xử lý, "
                f"{fmt_num(row['late_orders'])} đơn trễ, tỷ lệ trễ {fmt_pct(row['late_rate'])}. "
                f"Khuyến nghị: ưu tiên đơn giá trị cao, kiểm tra năng lực vận chuyển và cập nhật lịch hẹn cho khách."
                f"{action_note}"
            )
            
            is_selected = (idx == st.session_state.get("selected_priority_idx"))
            selected_class = " selected" if is_selected else ""
            c_checkbox, c_card = st.columns([1, 20])
            with c_checkbox:
                st.checkbox(
                    " ",
                    key=f"select_checkbox_{idx}",
                    on_change=select_priority_callback,
                    args=(idx, list(priority_df.head(3).index))
                )
            with c_card:
                card_html = f"""<div class="card-click-container">
<div class="work-order{selected_class}" data-rank="{rank}">
<div class="work-order-title">{html_escape(capitalize_first(order_title))}</div>
<div class="work-order-copy">{html_escape(order_copy)}</div>
</div>
</div>"""
                st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("Không có điểm nghẽn đủ điều kiện để hiển thị.")

with col_right:
    st.markdown('<div class="vertical-actions-container">', unsafe_allow_html=True)
    st.caption("Các thao tác dưới đây chỉ ghi nhận trong phiên màn hình hiện tại; chưa kết nối hệ thống điều phối hoặc chăm sóc khách hàng.")
    
    # Action 1: Review & Add to queue (Marking order IDs as processed in session_state)
    if st.button("Ghi nhận cần điều phối", key="carrier_header_btn", type="primary", use_container_width=True):
        if selected_row is not None:
            # Query order list corresponding to this group
            orders_to_mark = query_priority_orders(
                where_clause,
                selected_row["order_region"],
                selected_row["shipping_mode"],
                selected_row["category_name"],
            )
            if not orders_to_mark.empty:
                for oid in orders_to_mark["order_id"].tolist():
                    st.session_state["processed_orders"].add(oid)
            
            # Session-only marker; no external TMS integration is triggered here.
            st.session_state["pending_modal"] = {
                "title": "Đã ghi nhận cần điều phối",
                "message": "Nhóm đơn đã được ghi nhận trong phiên màn hình này. Chưa gửi sang hệ thống điều phối.",
            }
            st.rerun()
        else:
            st.toast("Vui lòng chọn một nhóm đơn hàng ưu tiên bên trái trước!", icon="⚠️")
            
    # Action 2: CSV download
    if selected_row is not None:
        order_list_df = query_priority_orders(
            where_clause,
            selected_row["order_region"],
            selected_row["shipping_mode"],
            selected_row["category_name"],
        )
        if not order_list_df.empty:
            order_list_display = rename_for_display(order_list_df)
            st.download_button(
                "Xuất danh sách đơn ưu tiên",
                data=order_list_display.to_csv(index=False).encode("utf-8-sig"),
                file_name="don_uu_tien_selected.csv",
                mime="text/csv",
                key="priority_header_btn",
                type="primary",
                use_container_width=True,
            )
        else:
            st.button("Không có danh sách đơn trễ", key="priority_header_empty", type="primary", disabled=True, use_container_width=True)
    else:
        if st.button("Xuất danh sách đơn ưu tiên", key="priority_header_disabled_trigger", type="primary", use_container_width=True):
            st.toast("Vui lòng chọn một nhóm đơn hàng ưu tiên bên trái trước!", icon="⚠️")
        
    # Action 3: customer notification
    if st.button("Ghi nhận cần thông báo", key="notify_header_btn", type="primary", use_container_width=True):
        if selected_row is not None:
            orders_to_mark = query_priority_orders(
                where_clause,
                selected_row["order_region"],
                selected_row["shipping_mode"],
                selected_row["category_name"],
            )
            if not orders_to_mark.empty:
                for oid in orders_to_mark["order_id"].tolist():
                    st.session_state["processed_orders"].add(oid)
            st.session_state["pending_modal"] = {
                "title": "Đã ghi nhận cần thông báo",
                "message": "Nhu cầu thông báo khách hàng đã được ghi nhận. Chưa gửi thư điện tử hoặc tin nhắn thật.",
            }
            st.rerun()
        else:
            st.toast("Vui lòng chọn một nhóm đơn hàng ưu tiên bên trái trước!", icon="⚠️")
            
    st.markdown('</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### Tóm tắt vận hành")
    if top_issue is not None:
        briefing_lines = [
            f"Điểm cần xử lý trước là {top_issue_name}.",
            f"Nhóm này có {fmt_money(top_issue['revenue_at_risk'])} doanh thu đang gặp rủi ro nếu không xử lý và {fmt_num(top_issue['late_orders'])} đơn trễ.",
            f"Tỷ lệ trễ của nhóm là {fmt_pct(top_issue['late_rate'])}, cao hơn ngưỡng mục tiêu vận hành ≤ {target_late_rate:.0f}%.",
            "Đề xuất: ưu tiên đơn giá trị cao, kiểm tra năng lực phương thức vận chuyển hiện tại và thông báo lại lịch hẹn cho khách có nguy cơ bị ảnh hưởng.",
        ]
        if not unstructured_df.empty:
            briefing_lines.append("Đã có dữ liệu log/truy cập để hỗ trợ xem tín hiệu nhu cầu trước khi đơn hàng phát sinh.")
        for line in briefing_lines:
            st.markdown(f"- {line}")
    else:
        st.info("Chưa có đủ dữ liệu để tạo báo cáo tự động trong phạm vi lọc hiện tại.")

# Initialize processed_orders set in session state
section(3, "Tình trạng vận hành", "Xem nhanh trạng thái giao hàng và các tín hiệu cần chú ý trước khi can thiệp.")

process_col1, process_col2, process_col3 = st.columns([5, 4, 3])
with process_col1:
    # st.markdown("##### &nbsp;")
    st.markdown(
        f"""
        <div class="process-line two-by-two">
            <div class="process-node"><b>Cung ứng hàng hóa</b><span>Giảm giá TB {fmt_money(avg_discount)}; ưu tiên chuẩn bị hàng cho danh mục có rủi ro.</span></div>
            <div class="process-node"><b>Danh mục sản phẩm</b><span>{len(product_df)} nhóm sản phẩm đang được theo dõi theo lợi nhuận và giao hàng.</span></div>
            <div class="process-node"><b>Kinh doanh</b><span>Doanh thu {fmt_money(revenue)}; hủy đơn {fmt_pct(cancel_rate)}.</span></div>
            <div class="process-node"><b>Phân phối</b><span>Giao trễ {fmt_pct(late_rate)}; {fmt_delay_days(sla_gap)}.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with process_col2:
    # st.markdown("##### &nbsp;")
    if delivery_df is not None and not delivery_df.empty:
        delivery_chart_df = delivery_df.copy()
        STATUS_VI = {
            "Late delivery": "Trễ hạn",
            "Advance shipping": "Giao sớm",
            "Shipping on time": "Đúng hạn",
            "Shipping canceled": "Đã hủy",
        }
        delivery_chart_df["delivery_status"] = delivery_chart_df["delivery_status"].map(lambda x: STATUS_VI.get(x, x))
        
        def delivery_color_key(status):
            status_text = str(status)
            if "Trễ hạn" in status_text:
                return "Trễ hạn"
            if "Đã hủy" in status_text:
                return "Đã hủy"
            if "Đúng hạn" in status_text:
                return "Đúng hạn"
            if "Giao sớm" in status_text:
                return "Giao sớm"
            return "Khác"

        delivery_chart_df["Nhóm trạng thái"] = delivery_chart_df["delivery_status"].apply(delivery_color_key)
        fig_delivery = px.pie(
            delivery_chart_df,
            names="delivery_status",
            values="orders",
            color="Nhóm trạng thái",
            color_discrete_map={
                "Đúng hạn": "#10B981",       # Green
                "Giao sớm": "#60A5FA",       # Light Blue
                "Trễ hạn": "#EF4444",        # Red
                "Đã hủy": "#7F1D1D",         # Dark Red
                "Khác": "#CBD5E1",
            },
            hole=0.62,
            title="Tỷ lệ trạng thái giao hàng",
        )
        total_delivery_orders = safe_float(delivery_chart_df["orders"].sum())
        fig_delivery.update_traces(
            textinfo="percent",
            textposition="outside",
            marker=dict(line=dict(color="#FFFFFF", width=2)),
            hovertemplate="%{label}<br>%{value:,.0f} đơn<br>%{percent}<extra></extra>",
        )
        fig_delivery = apply_chart_theme(fig_delivery, 255)
        fig_delivery.update_layout(
            annotations=[
                dict(
                    text=f"<b>{fmt_num(total_delivery_orders)}</b><br><span style='font-size:11px'>đơn</span>",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="#111827"),
                )
            ],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.18,
                xanchor="center",
                x=0.5,
                font=dict(size=10),
            ),
            margin=dict(l=16, r=16, t=54, b=54),
        )
        st.plotly_chart(fig_delivery, use_container_width=True)

with process_col3:
    if top_states_df is not None and not top_states_df.empty:
        # Map state codes to Vietnamese display
        US_STATES = {
            "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
            "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
            "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
            "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
            "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
            "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
            "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
            "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
            "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
            "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
            "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
            "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
            "WI": "Wisconsin", "WY": "Wyoming", "DC": "Washington D.C.",
            "PR": "Puerto Rico", "GU": "Guam", "VI": "U.S. Virgin Islands",
        }
        top_states_chart_df = top_states_df.copy()
        top_states_chart_df["Tên bang"] = top_states_chart_df["customer_state"].apply(lambda x: US_STATES.get(str(x).upper(), x))
        
        # Sort ascending for horizontal bar chart (highest on top)
        top_states_chart_df = top_states_chart_df.sort_values("revenue_at_risk", ascending=True)
        
        fig_states = px.bar(
            top_states_chart_df,
            x="revenue_at_risk",
            y="Tên bang",
            orientation="h",
            color="late_rate",
            color_continuous_scale=["#94A3B8", "#3B82F6", "#DC2626"], # slate -> blue -> warning red
            labels={"revenue_at_risk": "Doanh thu rủi ro ($)", "late_rate": "Tỷ lệ trễ (%)"},
            title="Top 3 khu vực khách hàng rủi ro cao"
        )
        fig_states.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="")
        st.plotly_chart(apply_chart_theme(fig_states, 255), use_container_width=True)
    else:
        st.info("Chưa có đủ dữ liệu khu vực khách hàng.")


section(
    4,
    "Điểm nghẽn cần xử lý",
    "Ưu tiên theo doanh thu rủi ro, số đơn trễ và mức lệch cam kết.",
)
problem_col1, problem_col2 = st.columns([4, 8])
with problem_col1:
    tone = "critical" if sev_class == "red" else "warning" if sev_class == "amber" else "good"
    st.markdown(
        manager_card(
            "Điểm nghẽn ưu tiên",
            top_issue_name,
            top_issue_copy,
            tone,
        ),
        unsafe_allow_html=True,
    )
    if ml_risk_df is not None and not ml_risk_df.empty:
        ml_row = ml_risk_df.iloc[0]
        st.markdown(
            manager_card(
                "Cảnh báo từ hệ thống",
                f"{fmt_num(ml_row.get('predicted_risk_orders'))} đơn rủi ro cao",
                (
                    f"Đây là cảnh báo bổ sung từ dữ liệu vận hành, không cộng trực tiếp với "
                    f"{fmt_num(late_orders)} đơn đã trễ hoặc có nguy cơ trễ theo dữ liệu vận hành. "
                    f"Mức cảnh báo trung bình của nhóm này là {fmt_pct(ml_row.get('avg_predicted_risk'))}."
                ),
                "warning",
            ),
            unsafe_allow_html=True,
        )
with problem_col2:
    if priority_df is not None and not priority_df.empty:
        priority_view = priority_df.copy().reset_index(drop=True)
        priority_view["Mức"] = priority_view.index.map(lambda pos: priority_level(pos, len(priority_view)))
        if "late_rate_delta" in priority_view.columns:
            priority_view["Xu hướng"] = priority_view["late_rate_delta"].apply(trend_label)
        else:
            priority_view["Xu hướng"] = "Chưa đủ dữ liệu"
        priority_view["Điểm nghẽn"] = priority_view.apply(short_issue, axis=1)
        priority_view["Độ lệch lịch hẹn"] = priority_view["sla_gap"].apply(fmt_delay_days)
        priority_view = priority_view[
            ["Mức", "Xu hướng", "Điểm nghẽn", "late_orders", "revenue_at_risk", "late_rate", "Độ lệch lịch hẹn", "margin"]
        ].rename(
            columns={
                "late_orders": "Đơn trễ",
                "revenue_at_risk": "Doanh thu đang gặp rủi ro",
                "late_rate": "Trễ (%)",
                "margin": "Biên lợi nhuận (%)",
            }
        )
        st.dataframe(
            priority_view.style.format(
                {
                    "Doanh thu đang gặp rủi ro": "${:,.0f}",
                    "Trễ (%)": "{:.1f}",
                    "Biên lợi nhuận (%)": "{:.1f}",
                }
            ).map(table_signal_style, subset=["Mức", "Xu hướng"]),
            use_container_width=True,
            hide_index=True,
            height=390,
        )

tab_realtime, tab_trend_7d, tab_history = st.tabs(["📊 Giám sát ca hiện tại", "📈 Xu hướng 7 ngày", "📜 Phân tích lịch sử"])

with tab_realtime:
    chart_col1, chart_col2 = st.columns([6, 6])
    with chart_col1:
        if hourly_queue_df is not None and not hourly_queue_df.empty:
            queue_view = hourly_queue_df.copy()
            queue_view["hour_label"] = queue_view["hour_of_day"].apply(lambda h: f"{int(h):02d}:00")
            queue_view["risk_rate"] = np.where(
                queue_view["queue_size"] > 0,
                queue_view["late_queue_size"] / queue_view["queue_size"] * 100,
                0,
            )
            peak_row = queue_view.sort_values(["late_queue_size", "queue_size"], ascending=False).iloc[0]
            peak_hour = peak_row["hour_label"]
            peak_backlog = safe_float(peak_row["queue_size"])
            peak_risk = safe_float(peak_row["risk_rate"])
            avg_risk = safe_float(queue_view["risk_rate"].mean())
            max_late_queue = safe_float(queue_view["late_queue_size"].max())
            avg_queue = safe_float(queue_view["queue_size"].mean())
            risk_tone = "red" if peak_risk >= 80 else "amber" if peak_risk >= 50 else "green"
            pressure_text = (
                "Cần mở thêm năng lực xử lý/điều tuyến ở khung giờ đỉnh."
                if peak_risk >= 80
                else "Theo dõi sát, ưu tiên xử lý đơn rủi ro trước khi backlog tăng."
                if peak_risk >= 50
                else "Nhịp xử lý đang trong vùng kiểm soát."
            )
            st.markdown(
                f"""
                <div class="ops-strip">
                    <div class="ops-mini blue"><b>{fmt_num(peak_backlog)}</b><span>Hàng chờ cao nhất tại {html_escape(peak_hour)}</span></div>
                    <div class="ops-mini {risk_tone}"><b>{fmt_pct(peak_risk)}</b><span>Tỷ lệ đơn trễ/rủi ro tại giờ đỉnh</span></div>
                    <div class="ops-mini amber"><b>{fmt_num(max_late_queue)}</b><span>Đơn rủi ro tối đa trong một khung giờ</span></div>
                    <div class="ops-mini green"><b>{fmt_num(avg_queue)}</b><span>Hàng chờ trung bình theo giờ trong ca</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            fig_queue = go.Figure()
            fig_queue.add_trace(
                go.Bar(
                    x=queue_view["hour_label"],
                    y=queue_view["queue_size"],
                    name="Hàng chờ cần xử lý",
                    marker=dict(color="rgba(147, 197, 253, 0.58)", line=dict(color="#60A5FA", width=1)),
                    hovertemplate="Giờ %{x}<br>Hàng chờ: %{y:,.0f} đơn<extra></extra>",
                )
            )
            fig_queue.add_trace(
                go.Scatter(
                    x=queue_view["hour_label"],
                    y=queue_view["risk_rate"],
                    name="Tỷ lệ đơn có nguy cơ trễ",
                    mode="lines+markers",
                    yaxis="y2",
                    line=dict(color="#EA580C", width=2.4, shape="spline", smoothing=0.45),
                    marker=dict(size=5, color="#EA580C"),
                    hovertemplate="Giờ %{x}<br>Đơn nguy cơ trễ: %{y:.1f}%<extra></extra>",
                )
            )
            fig_queue.add_trace(
                go.Scatter(
                    x=queue_view["hour_label"],
                    y=queue_view["late_queue_size"],
                    name="Đơn rủi ro",
                    mode="markers",
                    marker=dict(size=6, color="#F59E0B", opacity=0.65, line=dict(color="#FFFFFF", width=1)),
                    hovertemplate="Giờ %{x}<br>Đơn rủi ro: %{y:,.0f}<extra></extra>",
                )
            )
            fig_queue.add_trace(
                go.Scatter(
                    x=queue_view["hour_label"],
                    y=[80] * len(queue_view),
                    name="Ngưỡng can thiệp",
                    mode="lines",
                    yaxis="y2",
                    line=dict(color="#94A3B8", width=1, dash="dot"),
                    hoverinfo="skip",
                )
            )
# Redundant traces removed
            fig_queue.update_layout(
                title="Hàng chờ xử lý theo từng giờ trong ca trực",
                xaxis_title="Giờ trong ngày",
                yaxis_title="Số lượng đơn hàng",
            )
# Trace filter removed
            fig_queue.update_layout(
                title="Áp lực hàng chờ theo giờ",
                xaxis_title="Giờ trong ca",
                xaxis_tickangle=-45,
                yaxis=dict(title="Hàng chờ / đơn rủi ro"),
                yaxis2=dict(
                    title="Tỷ lệ đơn có nguy cơ trễ (%)",
                    overlaying="y",
                    side="right",
                    range=[0, max(100, float(queue_view["risk_rate"].max()) + 10)],
                    showgrid=False,
                    tickfont=dict(size=11),
                ),
                bargap=0.32,
                hovermode="x unified",
                shapes=[],
                annotations=[],
            )
            fig_queue = apply_chart_theme(fig_queue, 360)
            fig_queue.update_layout(
                title=dict(text="Áp lực hàng chờ theo giờ", font=dict(size=13), x=0, y=0.98),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                margin=dict(l=30, r=26, t=82, b=54),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.04,
                    xanchor="left",
                    x=0,
                    font=dict(size=10),
                    traceorder="normal",
                    bgcolor="rgba(255,255,255,0.86)",
                ),
            )
            fig_queue.update_xaxes(tickfont=dict(size=10, color="#64748B"), title_font=dict(size=11, color="#64748B"))
            fig_queue.update_yaxes(tickfont=dict(size=10, color="#64748B"), title_font=dict(size=11, color="#64748B"), gridcolor="#F1F5F9")
            st.plotly_chart(fig_queue, use_container_width=True)
            st.markdown(
                f"""
                <div class="ops-note">
                    <b>Nhận xét vận hành:</b> giờ áp lực nhất là {html_escape(peak_hour)} với {fmt_num(peak_backlog)} đơn trong hàng chờ.
                    Tỷ lệ đơn có nguy cơ trễ tại khung giờ này là {fmt_pct(peak_risk)}; trung bình ca là {fmt_pct(avg_risk)}. {html_escape(pressure_text)}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Chưa có đủ dữ liệu hàng chờ cho ca trực hiện tại.")
            
    with chart_col2:
        if not matrix_df.empty:
            # Query historical 7-day data for smoothing
            historical_days_cond = "order_date >= '2018-01-25 00:00:00' AND order_date <= '2018-01-31 23:38:00'"
            # Build general filters matching current selection
            hist_conds = [historical_days_cond]
            if selected_region != "Tất cả":
                hist_conds.append(f"order_region = '{sql_escape(selected_region)}'")
            if selected_shipping != "Tất cả":
                hist_conds.append(f"shipping_mode = '{sql_escape(selected_shipping)}'")
            if selected_category != "Tất cả":
                hist_conds.append(f"category_name = '{sql_escape(selected_category)}'")
            hist_where = " AND ".join(hist_conds)
            
            try:
                hist_matrix = con.execute(
                    f"""
                    SELECT order_region, shipping_mode,
                           SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_rate_hist,
                           COUNT(*) AS count_hist
                    FROM {BASE_TABLE}
                    WHERE {hist_where}
                    GROUP BY 1, 2
                    """
                ).df()
            except Exception:
                hist_matrix = pd.DataFrame()
                
            # Perform Bayesian smoothing: smoothed_rate = (w_today*rate_today + w_hist*rate_hist) / (w_today + w_hist)
            # Default weight for historical prior: w_hist = 5 (representing a base population size)
            w_hist = 5.0
            
            # Blend datasets
            today_matrix = matrix_df.copy()
            # Query current count per cell
            try:
                today_counts = con.execute(
                    f"""
                    SELECT order_region, shipping_mode, COUNT(*) AS count_today
                    FROM {BASE_TABLE}
                    WHERE {where_clause}
                    GROUP BY 1, 2
                    """
                ).df()
                today_matrix = today_matrix.merge(today_counts, on=["order_region", "shipping_mode"], how="left")
            except Exception:
                today_matrix["count_today"] = 1.0
                
            if hist_matrix is not None and not hist_matrix.empty:
                blended = today_matrix.merge(hist_matrix, on=["order_region", "shipping_mode"], how="left")
                blended["count_hist"] = blended["count_hist"].fillna(0.0)
                blended["late_rate_hist"] = blended["late_rate_hist"].fillna(10.0) # default target
                
                # Formula: smoothed_rate = (count_today*late_rate + w_hist*late_rate_hist) / (count_today + w_hist)
                blended["smoothed_rate"] = (
                    (blended["count_today"] * blended["late_rate"]) + (w_hist * blended["late_rate_hist"])
                ) / (blended["count_today"] + w_hist)
            else:
                blended = today_matrix.copy()
                blended["smoothed_rate"] = blended["late_rate"]
                
            matrix_pivot_color = blended.pivot_table(
                index="order_region", columns="shipping_mode", values="smoothed_rate", aggfunc="mean"
            ).fillna(0)
            
            matrix_pivot_text = blended.pivot_table(
                index="order_region", columns="shipping_mode", values="late_rate", aggfunc="mean"
            ).fillna(0)
            
            fig_heat = px.imshow(
                matrix_pivot_color,
                aspect="auto",
                color_continuous_scale=["#D1FAE5", "#FEF3C7", "#FCA5A5"],
                title="Rủi ro giao trễ theo khu vực và phương thức vận chuyển",
            )
            
            # Put exact today's late rate as annotations to show exact numbers, keeping color smooth
            fig_heat.update_traces(
                text=matrix_pivot_text.round(1).values,
                texttemplate="%{text}%",
            )
            
            fig_heat.update_layout(
                xaxis_title="",
                yaxis_title="",
                coloraxis_colorbar=dict(title="Tỷ lệ trễ ước tính"),
            )
            st.plotly_chart(apply_chart_theme(fig_heat, 330), use_container_width=True)
            
            # Interactive drilldown: Select a cell to see the details of orders in that cell
            all_regions = sorted(blended["order_region"].unique())
            all_modes = sorted(blended["shipping_mode"].unique())
            
            st.markdown("🔍 **Xem đơn trễ theo khu vực và phương thức:**")
            sel_col1, sel_col2 = st.columns(2)
            with sel_col1:
                drill_region = st.selectbox("Chọn Khu vực", all_regions, key="drill_region_sel")
            with sel_col2:
                drill_mode = st.selectbox("Chọn Phương thức", all_modes, key="drill_mode_sel")
                
            drill_where = (
                f"{where_clause} AND order_region = '{sql_escape(drill_region)}' "
                f"AND shipping_mode = '{sql_escape(drill_mode)}'"
            )
            try:
                drill_df = con.execute(
                    f"""
                    SELECT order_id, product_name, sales_amount, days_for_shipping_real - days_for_shipment_scheduled AS delay_days
                    FROM {BASE_TABLE}
                    WHERE {drill_where} AND late_delivery_risk = 1
                    ORDER BY sales_amount DESC
                    LIMIT 10
                    """
                ).df()
                if not drill_df.empty:
                    st.dataframe(
                        drill_df.rename(columns={
                            "order_id": "Mã đơn",
                            "product_name": "Sản phẩm",
                            "sales_amount": "Doanh thu",
                            "delay_days": "Số ngày trễ"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.caption("Không có đơn giao trễ nào trong ô này hôm nay.")
            except Exception as e:
                st.caption(f"Không thể tra cứu: {e}")

with tab_trend_7d:
    trend_7d_df = query_7day_trend(selected_region, selected_shipping, selected_category, selected_focus)
    if trend_7d_df is not None and not trend_7d_df.empty:
        trend_7d_df["order_day"] = pd.to_datetime(trend_7d_df["order_day"])
        trend_7d_df["Ngày"] = trend_7d_df["order_day"].dt.strftime("%d/%m")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            fig_late_trend = px.line(
                trend_7d_df,
                x="Ngày",
                y="late_rate",
                markers=True,
                title="Tỷ lệ giao trễ 7 ngày qua (%)",
                labels={"late_rate": "Tỷ lệ trễ (%)"}
            )
            fig_late_trend.update_traces(line_color="#DC2626", marker_color="#DC2626")
            st.plotly_chart(apply_chart_theme(fig_late_trend, 330), use_container_width=True)
            
        with col_t2:
            fig_rev_trend = go.Figure()
            fig_rev_trend.add_trace(
                go.Bar(
                    x=trend_7d_df["Ngày"],
                    y=trend_7d_df["revenue"],
                    name="Doanh thu",
                    marker_color="#2563EB"
                )
            )
            fig_rev_trend.add_trace(
                go.Bar(
                    x=trend_7d_df["Ngày"],
                    y=trend_7d_df["revenue_at_risk"],
                    name="Doanh thu gặp rủi ro",
                    marker_color="#D97706"
                )
            )
            fig_rev_trend.update_layout(
                barmode="group",
                title="Doanh thu & Doanh thu gặp rủi ro 7 ngày qua ($)",
                xaxis_title="Ngày",
                yaxis_title="Số tiền ($)"
            )
            st.plotly_chart(apply_chart_theme(fig_rev_trend, 330), use_container_width=True)
    else:
        st.info("Chưa có đủ dữ liệu để hiển thị xu hướng 7 ngày.")

with tab_history:
    # Query monthly data for the entire history to show a complete trend chart
    history_monthly_df = query_monthly("1=1")
    if history_monthly_df is not None and not history_monthly_df.empty:
        history_monthly_df = history_monthly_df.copy()
        history_monthly_df["late_ma3"] = history_monthly_df["late_rate"].rolling(3, min_periods=1).mean()
        fig_trend = go.Figure()
        fig_trend.add_trace(
            go.Scatter(
                x=history_monthly_df["month"],
                y=history_monthly_df["late_rate"],
                name="Tỷ lệ trễ lịch sử",
                mode="lines",
                line=dict(color="#CBD5E1", width=2, dash="dot"),
            )
        )
        fig_trend.add_trace(
            go.Scatter(
                x=history_monthly_df["month"],
                y=history_monthly_df["late_ma3"],
                name="Trung bình 3 tháng",
                mode="lines+markers",
                line=dict(color="#2563EB", width=3),
            )
        )
        fig_trend.update_layout(title="Xu hướng trễ hạn theo thời gian (2015-2018)", xaxis_title="", yaxis_title="Trễ (%)")
        st.plotly_chart(apply_chart_theme(fig_trend, 330), use_container_width=True)
    else:
        st.info("Chưa có đủ dữ liệu lịch sử để hiển thị xu hướng.")



# Duplicate state initialization removed

# Initialize checkbox states explicitly ONLY ONCE if not already in session state
if priority_df is not None and not priority_df.empty:
    for idx in priority_df.head(3).index:
        key = f"select_checkbox_{idx}"
        if key not in st.session_state:
            st.session_state[key] = (st.session_state["selected_priority_idx"] == idx)

# Old callback instance 1 removed

section(5, "Nguyên nhân và phương án xử lý", "Tập trung vào tuyến vận chuyển, nhóm sản phẩm và cảnh báo đang ảnh hưởng lớn nhất.")
solution_col1, solution_col2 = st.columns([7, 5])
with solution_col1:
    if product_df is not None and not product_df.empty:
        fig_product = px.bar(
            product_df.sort_values("revenue_at_risk", ascending=True),
            x="revenue_at_risk",
            y="category_name",
            color="late_rate",
            orientation="h",
            color_continuous_scale=["#10B981", "#D97706", "#DC2626"],
            title="Danh mục sản phẩm có doanh thu rủi ro cao nhất",
        )
        fig_product.update_layout(xaxis_title="", yaxis_title="", coloraxis_colorbar_title="Trễ (%)")
        st.plotly_chart(apply_chart_theme(fig_product, 395), use_container_width=True)
with solution_col2:
    ai_context = {
        "period": selected_period,
        "selected_region": selected_region,
        "selected_shipping": selected_shipping,
        "selected_category": selected_category,
        "selected_focus": selected_focus,
        "orders": fmt_num(orders),
        "late_orders": fmt_num(late_orders),
        "late_rate": fmt_pct(late_rate),
        "revenue_at_risk": fmt_money(revenue_at_risk),
        "sla_gap": fmt_delay_days(sla_gap),
        "top_issue": top_issue_name,
        "top_issue_late_rate": fmt_pct(top_issue["late_rate"]) if top_issue is not None else "không có dữ liệu",
        "top_issue_revenue_at_risk": fmt_money(top_issue["revenue_at_risk"]) if top_issue is not None else "không có dữ liệu",
        "top_region": top_region_name,
        "top_shipping_mode": top_shipping_mode,
        "top_category": top_category_name,
        "top_category_risk": fmt_money(top_category_risk),
        "ml_predicted_risk_orders": fmt_num(ml_risk_df.iloc[0].get("predicted_risk_orders")) if not ml_risk_df.empty else "không có dữ liệu",
        "ml_avg_predicted_risk": fmt_pct(ml_risk_df.iloc[0].get("avg_predicted_risk")) if not ml_risk_df.empty else "không có dữ liệu",
        "top_ml_features": ml_features_df.head(5).to_dict("records") if not ml_features_df.empty else [],
    }
    ai_insight = generate_ai_ops_insight(ai_context)
    st.markdown(render_ai_ops_insight(ai_insight), unsafe_allow_html=True)
    render_ai_action_cards(ai_insight)
with st.container(border=True):
    # Two tabs for dispatch simulation and financial impact
    tab_sim, tab_roi = st.tabs(["📊 Mô phỏng phương án điều phối", "💰 Hiệu quả tài chính theo phương thức"])
    
    with tab_sim:
        st.markdown("##### Mô phỏng chi phí - lợi ích khi đổi phương thức vận chuyển")
        st.caption(
            "Bảng này giúp so sánh chi phí điều phối phát sinh với phần doanh thu rủi ro có thể bảo vệ. "
            "Các giả định bên dưới có thể chỉnh theo chính sách vận hành của doanh nghiệp."
        )
        
        st.markdown(
            """
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-left:4px solid #2563EB;border-radius:8px;padding:12px 14px;margin:8px 0 12px 0;color:#334155;font-size:13px;line-height:1.45;">
                <b>Giả định mô phỏng:</b> kéo tỷ lệ bảo vệ để xem phần doanh thu rủi ro có thể giữ lại thay đổi ra sao.
                Chi phí nâng cấp là phần phụ phí dự kiến trên mỗi đơn khi chuyển từ Tiêu chuẩn sang phương thức nhanh hơn.
            </div>
            """,
            unsafe_allow_html=True,
        )
        sim_col1, sim_col2, sim_col3 = st.columns([2.2, 1, 1])
        with sim_col1:
            rec_rate_pct = st.slider(
                "Tỷ lệ doanh thu rủi ro có thể bảo vệ (%)",
                min_value=10,
                max_value=100,
                value=75,
                step=5,
                help="Kéo thanh này để thay đổi phần doanh thu rủi ro dự kiến có thể giữ lại sau khi điều phối lại vận chuyển.",
            )
            st.caption(
                f"Đang giả định giữ được {rec_rate_pct}% doanh thu rủi ro. "
                "Đây là biến mô phỏng để thử kịch bản, không phải số đo tự động từ hệ thống."
            )
        with sim_col2:
            second_upgrade_cost = st.number_input(
                "Phụ phí Nhanh ($/đơn)",
                min_value=0.0,
                value=2.0,
                step=0.5,
                help="Giả định chi phí tăng thêm khi chuyển từ Tiêu chuẩn sang Nhanh.",
            )
        with sim_col3:
            first_upgrade_cost = st.number_input(
                "Phụ phí Hỏa tốc ($/đơn)",
                min_value=0.0,
                value=5.0,
                step=0.5,
                help="Giả định chi phí tăng thêm khi chuyển từ Tiêu chuẩn sang Hỏa tốc.",
            )
        recovery_rate = rec_rate_pct / 100.0
        
        # Dynamically recalculate What-If simulation with the recovery rate
        sim_what_if_rows = []
        if cost_benefit_df is not None and not cost_benefit_df.empty:
            for _, cb_row in cost_benefit_df.iterrows():
                for target_mode, rate_col in [("Second Class", "second_late_rate"), ("First Class", "first_late_rate")]:
                    sim_target_late_rate = safe_float(cb_row.get(rate_col), None)
                    if sim_target_late_rate is None:
                        continue
                    saved_revenue = estimate_saved_revenue(
                        cb_row.get("revenue_at_risk"),
                        cb_row.get("standard_late_rate"),
                        sim_target_late_rate
                    ) * recovery_rate
                    extra_cost = estimate_upgrade_cost(
                        cb_row.get("revenue"),
                        cb_row.get("orders"),
                        target_mode,
                        second_upgrade_cost,
                        first_upgrade_cost,
                    )
                    sim_what_if_rows.append(
                        {
                            "Nhóm cần quyết định": f"{cb_row['category_name']} tại {cb_row['order_region']}",
                            "Phương án": f"Tiêu chuẩn → {SHIPPING_VI.get(target_mode, target_mode)}",
                            "Đơn bị ảnh hưởng": cb_row.get("orders"),
                            "Tỷ lệ trễ hiện tại (%)": cb_row.get("standard_late_rate"),
                            "Tỷ lệ trễ phương án (%)": sim_target_late_rate,
                            "Doanh thu rủi ro hiện tại": cb_row.get("revenue_at_risk"),
                            "Doanh thu rủi ro có thể bảo vệ": saved_revenue,
                            "Chi phí điều phối ước tính": extra_cost,
                            "Lợi ích ròng ước tính": saved_revenue - extra_cost,
                            "Khuyến nghị": "Nên cân nhắc đổi" if saved_revenue > extra_cost else "Không nên đổi nếu chỉ xét chi phí",
                        }
                    )
        sim_what_if_df = pd.DataFrame(sim_what_if_rows)
        
        if sim_what_if_df is not None and not sim_what_if_df.empty:
            sim_what_if_df = sim_what_if_df.sort_values("Lợi ích ròng ước tính", ascending=False).head(12)
            st.dataframe(
                sim_what_if_df.style.format(
                    {
                        "Đơn bị ảnh hưởng": "{:,.0f}",
                        "Tỷ lệ trễ hiện tại (%)": "{:.1f}",
                        "Tỷ lệ trễ phương án (%)": "{:.1f}",
                        "Doanh thu rủi ro hiện tại": "${:,.0f}",
                        "Doanh thu rủi ro có thể bảo vệ": "${:,.0f}",
                        "Chi phí điều phối ước tính": "${:,.0f}",
                        "Lợi ích ròng ước tính": "${:,.0f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            total_priority_orders = int(late_orders) if late_orders > 0 else 10
            upgrade_cost_est = total_priority_orders * second_upgrade_cost
            recovered_rev_est = revenue_at_risk * recovery_rate
            net_benefit = recovered_rev_est - upgrade_cost_est
            st.markdown(
                f"""
                <div style="background-color: #EFF6FF; border-left: 5px solid #3B82F6; padding: 16px; border-radius: 6px; color: #1E40AF; font-size: 13.5px; line-height: 1.6;">
                    <b>Thông tin mô phỏng dựa trên 30 ngày lịch sử vận hành:</b><br/>
                    Nếu nâng cấp <b>{total_priority_orders} đơn hàng</b> Tiêu chuẩn sang <b>Vận chuyển Nhanh (Second Class)</b>:<br/>
                    • <b>Chi phí điều phối ước tính:</b> {fmt_money(upgrade_cost_est)} (giả định {fmt_money(second_upgrade_cost)}/đơn)<br/>
                    • <b>Doanh thu rủi ro có thể bảo vệ ({rec_rate_pct}%):</b> {fmt_money(recovered_rev_est)}<br/>
                    • <b>Lợi ích ròng ước tính:</b> <b style="color: #059669;">{fmt_money(net_benefit)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with tab_roi:
        st.markdown("##### Hiệu quả tài chính và rủi ro của từng phương thức vận chuyển")
        st.caption("So sánh doanh thu rủi ro và giá trị trung bình mỗi đơn theo từng phương thức vận chuyển.")
        if shipping_roi_df is not None and not shipping_roi_df.empty:
            roi_display = shipping_roi_df.copy().rename(
                columns={
                    "shipping_mode": "Phương thức vận chuyển",
                    "revenue_at_risk": "Doanh thu rủi ro",
                    "late_orders": "Số lượng đơn rủi ro",
                    "avg_revenue_per_order": "Doanh thu trung bình/đơn"
                }
            )
            cols_to_show_roi = ["Phương thức vận chuyển", "Doanh thu rủi ro", "Số lượng đơn rủi ro", "Doanh thu trung bình/đơn"]
            st.dataframe(
                roi_display[cols_to_show_roi].style.format(
                    {
                        "Doanh thu rủi ro": "${:,.0f}",
                        "Số lượng đơn rủi ro": "{:,.0f}",
                        "Doanh thu trung bình/đơn": "${:,.0f}"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Chưa có dữ liệu phân tích tài chính phương thức vận chuyển.")


# Old callback instance 2 removed

# Initialize selected priority index to None if not set
if "selected_priority_idx" not in st.session_state:
    st.session_state["selected_priority_idx"] = None

# Initialize checkbox states explicitly ONLY ONCE if not already in session state
if priority_df is not None and not priority_df.empty:
    for idx in priority_df.head(3).index:
        key = f"select_checkbox_{idx}"
        if key not in st.session_state:
            st.session_state[key] = (st.session_state["selected_priority_idx"] == idx)

section(6, "Hỏi dữ liệu vận hành", "Tra cứu nhanh các tình huống vận hành mà không cần tự lọc nhiều biểu đồ.")
st.warning(
    "Phần này dùng trợ lý ngôn ngữ để tạo truy vấn và diễn giải kết quả. "
    "Trước khi dùng để chốt điều phối, gửi khách hàng hoặc thay đổi chi phí, hãy kiểm tra lại SQL và bảng dữ liệu trả về."
)
st.markdown("##### Gợi ý câu hỏi phân tích:")

suggestions = [
    "Liệt kê các đơn có mức cảnh báo trễ trên 80% để tôi ưu tiên điều phối gấp.",
    "Nếu ngân sách điều tốc là $5,000, nên ưu tiên đổi phương thức vận chuyển cho nhóm đơn nào?",
    "Nhóm Standard Class nào nên chuyển sang Second hoặc First Class để giảm doanh thu rủi ro?",
]
sugg_cols = st.columns(3)
for i, q in enumerate(suggestions):
    with sugg_cols[i]:
        st.markdown('<div class="suggest-pill">', unsafe_allow_html=True)
        if st.button(q, key=f"suggest_{i}", use_container_width=True):
            st.session_state["pending_question"] = q
        st.markdown('</div>', unsafe_allow_html=True)

if "last_question" not in st.session_state:
    st.session_state["last_question"] = None
if "last_sql" not in st.session_state:
    st.session_state["last_sql"] = None
if "last_result_df" not in st.session_state:
    st.session_state["last_result_df"] = None
if "last_insight" not in st.session_state:
    st.session_state["last_insight"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

question = None
with st.form("supply_chain_question_form", clear_on_submit=True, border=False):
    question_col, submit_col = st.columns([8, 1.35])
    with question_col:
        typed_question = st.text_input(
            "Hỏi dữ liệu chuỗi cung ứng",
            placeholder="Hỏi dữ liệu vận hành...",
            label_visibility="collapsed",
        )
    with submit_col:
        ask_submitted = st.form_submit_button("Phân tích", use_container_width=True)
if ask_submitted and typed_question.strip():
    question = typed_question.strip()
if not question and st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

if question:
    client = get_groq_client()
    if client is None:
        st.error("Chưa có khóa truy cập nên chưa dùng được phần hỏi dữ liệu.")
    else:
        with st.status("Đang phân tích dữ liệu...", expanded=True) as status:
            try:
                status.update(label="Đang hiểu câu hỏi và lấy dữ liệu phù hợp.", state="running")
                sql_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SCHEMA_CONTEXT},
                        {"role": "user", "content": question},
                    ],
                    temperature=0,
                    max_tokens=600,
                )
                raw_sql_output = sql_response.choices[0].message.content
                missing_concept = extract_no_matching_column(raw_sql_output)
                if missing_concept:
                    status.update(label="Câu hỏi ngoài phạm vi dữ liệu hiện có.", state="error")
                    st.warning(
                        f"⚠️ Câu hỏi có nhắc đến **{missing_concept}**, nhưng dữ liệu hệ thống đang quản lý "
                        "hiện không có thuộc tính này. Hệ thống không tự suy diễn sang cột khác để tránh trả lời "
                        "sai lệch — vui lòng đặt câu hỏi khác trong phạm vi dữ liệu vận hành và dự báo hiện có."
                    )
                else:
                    sql = extract_sql(raw_sql_output)
                    if not is_safe_select(sql):
                        status.update(label="Không thể tạo truy vấn an toàn cho câu hỏi này.", state="error")
                        st.code(sql, language="sql")
                    else:
                        status.update(label="Đang truy vấn kho dữ liệu.", state="running")
                        result_df = con.execute(sql).df()
                        
                        try:
                            status.update(label="Đang phân tích dữ liệu.", state="running")
                            # Chuyển đổi tối đa 30 dòng dữ liệu thành dạng text để LLM đọc và hiểu bản chất
                            preview = result_df.head(30).to_string(index=False) if not result_df.empty else "Không có dữ liệu phù hợp."
                            
                            # Gọi LLM sinh phản hồi chuyên sâu
                            insight_response = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "Bạn là chuyên viên phân tích dữ liệu vận hành chuỗi cung ứng. "
                                            "Chỉ dựa vào dữ liệu được cung cấp, không tự bịa thêm số liệu hoặc hành động đã thực thi. "
                                            "Nếu dữ liệu chưa đủ, truy vấn có thể gây hiểu nhầm, hoặc kết quả chỉ là mẫu nhỏ, phải nêu rõ giới hạn. "
                                            "Trả lời bằng tiếng Việt, ngắn gọn, trực tiếp cho trưởng ca logistics.\n\n"
                                            "**Nhận xét vận hành:** Nêu 2-3 điểm chính từ dữ liệu, ưu tiên số liệu có tác động tới giao hàng, doanh thu hoặc năng lực xử lý.\n\n"
                                            "**Rủi ro cần kiểm tra:** Nêu rủi ro chính và điều kiện cần xác minh trước khi ra quyết định.\n\n"
                                            "**Hành động tham khảo:** Đề xuất 2-3 bước có thể xem xét. Không viết như hệ thống đã gửi lệnh, đã thông báo khách hàng hoặc đã điều phối thật.\n\n"
                                            "**Kết luận:** Một câu ngắn cho người quản lý ca."
                                        ),
                                    },
                                    {
                                        "role": "user",
                                        "content": f"Câu hỏi: {question}\n\nKết quả truy vấn dữ liệu:\n{preview}\n\nHãy phân tích đúng phạm vi dữ liệu và nêu giới hạn nếu cần.",
                                    },
                                ],
                                temperature=0.5,
                                max_tokens=1600,
                            )
                            
                            status.update(label="Phân tích hoàn tất.", state="complete", expanded=False)
                            
                            # Lưu thông tin phân tích vào session_state để không bị mất khi render lại giao diện
                            st.session_state["last_question"] = question
                            st.session_state["last_sql"] = sql
                            st.session_state["last_result_df"] = result_df
                            st.session_state["last_insight"] = insight_response.choices[0].message.content
                            st.session_state["chat_history"].append({
                                "question": question,
                                "sql": sql,
                                "insight": insight_response.choices[0].message.content
                            })
                        except Exception as exc:
                            status.update(label="Phân tích gặp lỗi.", state="error")
                            st.error(format_llm_error(exc))
                        
                        st.markdown("##### Câu hỏi")
                        st.write(question)
                        with st.expander("Truy vấn dữ liệu đã sử dụng", expanded=True):
                            st.code(sql, language="sql")
                            for note in sql_quality_notes(sql):
                                st.warning(note)
                        if not result_df.empty:
                            display_result_df = rename_for_display(result_df)
                            auto_fig = make_auto_chart(display_result_df, "Kết quả phân tích từ dữ liệu")
                            if auto_fig is not None:
                                st.plotly_chart(auto_fig, use_container_width=True)
                            st.dataframe(display_result_df, use_container_width=True, hide_index=True)
                            
                        st.markdown("##### Nhận định và hành động đề xuất")
                        st.caption(
                            "Nhận định dưới đây được tạo từ kết quả truy vấn hiển thị ở trên; "
                            "không thay thế kiểm tra nghiệp vụ trước khi chốt hành động."
                        )
                        st.markdown(st.session_state["last_insight"])
                        
                        # Generate report and download button (left aligned under response)
                        report_txt = generate_combined_report(
                            question,
                            sql,
                            rename_for_display(result_df) if not result_df.empty else None,
                            st.session_state["last_insight"]
                        )
                        st.markdown('<div class="report-download-btn-container">', unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Tải báo cáo phân tích (.txt)",
                            data=report_txt,
                            file_name="bien_ban_phan_tich.txt",
                            mime="text/plain",
                            key="download_chat_report_active",
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
            except Exception as exc:
                status.update(label="Phân tích gặp lỗi.", state="error")
                st.error(format_llm_error(exc))
elif st.session_state["last_question"]:
    with st.status("Hoàn tất.", state="complete", expanded=False):
        st.markdown("##### Câu hỏi")
        st.write(st.session_state["last_question"])
        with st.expander("Truy vấn dữ liệu đã sử dụng", expanded=True):
            st.code(st.session_state["last_sql"], language="sql")
            for note in sql_quality_notes(st.session_state["last_sql"]):
                st.warning(note)
        
        result_df = st.session_state["last_result_df"]
        if result_df is not None and not result_df.empty:
            display_result_df = rename_for_display(result_df)
            auto_fig = make_auto_chart(display_result_df, "Kết quả phân tích từ dữ liệu")
            if auto_fig is not None:
                st.plotly_chart(auto_fig, use_container_width=True)
            st.dataframe(display_result_df, use_container_width=True, hide_index=True)
            
        st.markdown("##### Nhận định và hành động đề xuất")
        st.caption(
            "Nhận định dưới đây được tạo từ kết quả truy vấn hiển thị ở trên; "
            "không thay thế kiểm tra nghiệp vụ trước khi chốt hành động."
        )
        st.markdown(st.session_state["last_insight"])
        
        # Generate report and download button (left aligned under response)
        report_txt = generate_combined_report(
            st.session_state["last_question"],
            st.session_state["last_sql"],
            rename_for_display(result_df) if (result_df is not None and not result_df.empty) else None,
            st.session_state["last_insight"]
        )
        st.markdown('<div class="report-download-btn-container">', unsafe_allow_html=True)
        st.download_button(
            label="📥 Tải báo cáo phân tích (.txt)",
            data=report_txt,
            file_name="bien_ban_phan_tich.txt",
            mime="text/plain",
            key="download_chat_report_persistent",
        )
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get("chat_history"):
    with st.expander("📜 Lịch sử phân tích gần đây", expanded=False):
        st.markdown('<div class="history-section-marker"></div>', unsafe_allow_html=True)
        
        # Filter duplicates (maintaining forward list to keep original STT indices)
        seen = set()
        unique_history_forward = []
        for h in st.session_state["chat_history"]:
            q_clean = h["question"].strip()
            if q_clean not in seen:
                seen.add(q_clean)
                unique_history_forward.append(h)
                
        # Index each with its original sequential STT (1, 2, ...) and then reverse
        unique_history_with_idx = [
            {"original_stt": idx + 1, "data": item}
            for idx, item in enumerate(unique_history_forward)
        ]
        unique_history_reversed = list(reversed(unique_history_with_idx))
        
        # Render all questions inside a scrollable container
        n_items = len(unique_history_with_idx)
        dynamic_height = min(n_items * 44 + 16, 220)
        with st.container(height=dynamic_height, border=False):
            for item_wrapper in unique_history_reversed:
                orig_stt = item_wrapper["original_stt"]
                h = item_wrapper["data"]
                
                if st.button(f"{orig_stt}. {h['question']}", key=f"hist_btn_{orig_stt}", use_container_width=True):
                    st.session_state["pending_question"] = h["question"]
                    st.rerun()