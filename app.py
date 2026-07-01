import html
import re

import duckdb
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


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
    background: linear-gradient(135deg, #7F1D1D 0%, #B91C1C 56%, #DC2626 100%);
    color: #FFFFFF;
    border-radius: 10px;
    padding: 24px 26px;
    margin: 12px 0 16px 0;
    border: 1px solid rgba(127, 29, 29, 0.35);
}
.crisis-kicker {
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #FEE2E2;
    margin-bottom: 8px;
}
.crisis-title {
    font-size: 38px;
    line-height: 1.05;
    font-weight: 900;
    margin: 0 0 10px 0;
}
.crisis-copy {
    font-size: 15px;
    line-height: 1.5;
    color: #FEE2E2;
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
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.24);
    border-radius: 8px;
    padding: 13px 14px;
}
.crisis-metric b {
    display: block;
    font-size: 22px;
    color: #FFFFFF;
    margin-bottom: 4px;
}
.crisis-metric span {
    display: block;
    font-size: 12px;
    color: #FEE2E2;
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
.manager-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 18px;
    min-height: 178px;
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
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 9px;
}
.card-title {
    color: #111827;
    font-size: 20px;
    line-height: 1.2;
    font-weight: 800;
    margin-bottom: 8px;
}
.card-copy {
    color: #374151;
    font-size: 13px;
    line-height: 1.5;
    margin: 0;
}
.process-line {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
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
}
@media (max-width: 760px) {
    .kpi-grid, .theory-ribbon, .process-line, .action-list, .crisis-metrics {
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
</style>

""",
    unsafe_allow_html=True,
)


BASE_TABLE = "vanh_gold.main.stg_supplychain_v2"
ML_TABLE = "vanh_gold.main.ml_predictions_explained"
ML_FEATURE_TABLE = "vanh_gold.main.ml_feature_importance"
ML_PERFORMANCE_TABLE = "vanh_gold.main.ml_performance_metrics"


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
        
    report += "4. NHẬN ĐỊNH VÀ HÀNH ĐỘNG ĐỀ XUẤT TỪ TRỢ LÝ AI:\n\n"
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


def describe_issue(row) -> str:
    if row is None:
        return "Không có nhóm điểm nghẽn trong phạm vi lọc"
    return (
        f"các đơn thuộc danh mục {row['category_name']}, gửi bằng {row['shipping_mode']} "
        f"tại khu vực {row['order_region']}"
    )


def short_issue(row) -> str:
    return f"{row['category_name']} tại {row['order_region']}, gửi bằng {row['shipping_mode']}"


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
        return "Chưa đủ dữ liệu"
    if delta >= 2:
        return "Xấu đi"
    if delta <= -2:
        return "Cải thiện"
    return "Ổn định"


def table_signal_style(value):
    text = str(value).lower()
    if text in {"đỏ", "xấu đi"}:
        return "background-color: #FEE2E2; color: #991B1B; font-weight: 700;"
    if text == "cam":
        return "background-color: #FEF3C7; color: #92400E; font-weight: 700;"
    if text in {"cải thiện", "ổn định"}:
        return "background-color: #D1FAE5; color: #065F46; font-weight: 700;"
    return "background-color: #F3F4F6; color: #374151;"


def html_escape(value) -> str:
    return html.escape("" if value is None else str(value))


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


def build_where(year, region, shipping, category, focus_mode):
    conds = ["1=1"]
    if year != "Tất cả":
        conds.append(f"order_year = {int(year)}")
    if region != "Tất cả":
        conds.append(f"order_region = '{sql_escape(region)}'")
    if shipping != "Tất cả":
        conds.append(f"shipping_mode = '{sql_escape(shipping)}'")
    if category != "Tất cả":
        conds.append(f"category_name = '{sql_escape(category)}'")
    if focus_mode == "Chỉ đơn trễ / rủi ro trễ":
        conds.append("late_delivery_risk = 1")
    return " AND ".join(conds)


def build_previous_where(year, region, shipping, category, focus_mode):
    if year == "Tất cả":
        return None
    previous_year = int(year) - 1
    return build_where(str(previous_year), region, shipping, category, focus_mode)


def build_trend_context(year, available_years, region, shipping, category, focus_mode):
    year_values = sorted(int(y) for y in available_years)
    if year != "Tất cả":
        current_year = int(year)
        previous_year = current_year - 1
    elif len(year_values) >= 2:
        current_year = year_values[-1]
        previous_year = year_values[-2]
    else:
        return None
    return {
        "current_year": current_year,
        "previous_year": previous_year,
        "current_where": build_where(str(current_year), region, shipping, category, focus_mode),
        "previous_where": build_where(str(previous_year), region, shipping, category, focus_mode),
        "base_where": build_where("Tất cả", region, shipping, category, focus_mode),
        "label": f"năm {previous_year}",
    }


token = secret_value("MOTHERDUCK_TOKEN")
if not token:
    st.warning("Chưa có MOTHERDUCK_TOKEN. Nhập token để mở bảng điều hành.")
    token = st.text_input("MOTHERDUCK_TOKEN", type="password")
    if not token:
        st.stop()

con = get_connection(token)


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
            AVG(discount) AS avg_discount
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
def query_priority_trend(base_where_clause: str, current_year: int, previous_year: int):
    return con.execute(
        f"""
        SELECT
            order_region,
            shipping_mode,
            category_name,
            SUM(CASE WHEN order_year = {current_year} AND late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0
                / NULLIF(SUM(CASE WHEN order_year = {current_year} THEN 1 ELSE 0 END), 0) AS current_late_rate,
            SUM(CASE WHEN order_year = {previous_year} AND late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0
                / NULLIF(SUM(CASE WHEN order_year = {previous_year} THEN 1 ELSE 0 END), 0) AS previous_late_rate
        FROM {BASE_TABLE}
        WHERE {base_where_clause}
          AND order_year IN ({current_year}, {previous_year})
        GROUP BY 1, 2, 3
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
def query_ml_signals():
    try:
        risk = con.execute(
            f"""
            SELECT
                COUNT(DISTINCT order_id) AS predicted_risk_orders,
                AVG(predicted_probability) * 100 AS avg_predicted_risk
            FROM {ML_TABLE}
            WHERE predicted_label = 1
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
        font=dict(family="Inter, sans-serif", color="#374151", size=12),
        title=dict(font=dict(color="#111827", size=15), x=0),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=20, r=18, t=46, b=25),
        colorway=["#2563EB", "#3B82F6", "#D97706", "#DC2626", "#7C3AED"],
    )
    fig.update_xaxes(showgrid=False, linecolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F3F4F6", linecolor="#E5E7EB", zeroline=False)
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
    "predicted_probability": "Xác suất dự báo",
    "predicted_label": "Nhãn dự báo",
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
    ]
    return any(table.lower() in lowered for table in allowed)


def extract_sql(text: str) -> str:
    match = re.search(r"```sql\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\s*(.*?)```", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


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
shap_customer_segment, shap_days_for_shipment_scheduled.

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
- shap_days_for_shipment_scheduled (Đóng góp của Số ngày dự kiến giao)

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
UNION ALL
SELECT 'Số ngày dự kiến giao', AVG(ABS(shap_days_for_shipment_scheduled)) FROM {ML_TABLE}
ORDER BY importance DESC;

Quy tắc:
- Chỉ dùng đúng tên bảng/cột trên.
- "Doanh thu đang gặp rủi ro" hoặc "Doanh thu cần bảo vệ" nghĩa là SUM(CASE WHEN late_delivery_risk = 1 THEN sales_amount ELSE 0 END).
- "Tỷ lệ giao trễ" nghĩa là SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*).
- "Biên lợi nhuận" hoặc "Biên lợi nhuận (%)" nghĩa là SUM(profit) * 100.0 / SUM(sales_amount).
- "Tỷ lệ đơn hàng bị dự đoán trễ" hoặc "tỷ lệ bị dự đoán trễ" nghĩa là SUM(predicted_label) * 100.0 / COUNT(*).
- Với câu hỏi về doanh thu, lợi nhuận, biên lợi nhuận, giao hàng (thực tế), sản phẩm, khu vực, dùng bảng vận hành chính {BASE_TABLE}.
- Với câu hỏi liên quan đến 'dự đoán', 'dự báo', 'bị dự đoán trễ', 'predicted', 'xác suất', 'SHAP', 'tầm quan trọng đặc trưng', dùng bảng dự báo AI {ML_TABLE}.
- Thêm LIMIT 50 nếu kết quả không phải tổng hợp một dòng.
- Chỉ trả về duy nhất SQL trong ```sql ... ```.
MẸO NHẬN BIẾT CÂU HỎI CỦA NGƯỜI DÙNG:
- Khi người dùng hỏi: "Những yếu tố nào ảnh hưởng nhiều nhất đến dự đoán giao hàng trễ?" hoặc "Yếu tố nào tác động lớn nhất đến rủi ro trễ?", bản chất họ đang hỏi về Tầm quan trọng của đặc trưng tổng thể (Global Feature Importance).
- Bạn PHẢI viết câu lệnh SELECT tính TRUNG BÌNH GIÁ TRỊ TUYỆT ĐỐI (AVG(ABS(...))) của các cột SHAP trong bảng `vanh_gold.main.ml_predictions_explained`.

Tuyệt đối KHÔNG TRUY VẤN bảng `stg_supplychain_v2` hay tính toán late_delivery_risk cho câu hỏi này, vì đây là câu hỏi giải thích mô hình Machine Learning!
"""


years, regions, shipping_modes, categories = filter_options()

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title">
            <h2>Điều hành chuỗi cung ứng</h2>
            <p>Theo dõi đơn hàng, giao hàng, lợi nhuận và các điểm cần xử lý trong phạm vi dữ liệu lịch sử.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_year = st.selectbox("Năm", ["Tất cả"] + [str(y) for y in years])
    selected_region = st.selectbox("Khu vực", ["Tất cả"] + regions)
    selected_shipping = st.selectbox("Phương thức vận chuyển", ["Tất cả"] + shipping_modes)
    selected_category = st.selectbox("Danh mục sản phẩm", ["Tất cả"] + categories)
    selected_focus = st.radio(
        "Chế độ xem",
        ["Tất cả đơn hàng", "Chỉ đơn trễ / rủi ro trễ"],
        index=0,
    )
    st.caption(
        f"Phạm vi đang xem: năm {selected_year}; khu vực {selected_region}; "
        f"vận chuyển {selected_shipping}; danh mục {selected_category}; chế độ {selected_focus}."
    )
    if not secret_value("GROQ_API_KEY"):
        st.text_input("GROQ_API_KEY", type="password", key="groq_api_key")
    st.divider()
    st.caption("Nguồn dữ liệu: kho MotherDuck")


where_clause = build_where(selected_year, selected_region, selected_shipping, selected_category, selected_focus)
trend_context = build_trend_context(selected_year, years, selected_region, selected_shipping, selected_category, selected_focus)

summary_df = query_summary(where_clause)
summary = summary_df.iloc[0] if not summary_df.empty else pd.Series(dtype="object")
trend_current_df = query_summary(trend_context["current_where"]) if trend_context else pd.DataFrame()
trend_previous_df = query_summary(trend_context["previous_where"]) if trend_context else pd.DataFrame()
trend_current = trend_current_df.iloc[0] if not trend_current_df.empty else pd.Series(dtype="object")
trend_previous = trend_previous_df.iloc[0] if not trend_previous_df.empty else pd.Series(dtype="object")
priority_df = query_priority(where_clause)
if trend_context and not priority_df.empty:
    priority_trend_df = query_priority_trend(
        trend_context["base_where"],
        trend_context["current_year"],
        trend_context["previous_year"],
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
ml_risk_df, ml_features_df = query_ml_signals()
unstructured_df = query_unstructured_status()

revenue = safe_float(summary.get("revenue"))
profit = safe_float(summary.get("profit"))
orders = safe_float(summary.get("orders"))
late_orders = safe_float(summary.get("late_orders"))
revenue_at_risk = safe_float(summary.get("revenue_at_risk"))
sla_gap = safe_float(summary.get("sla_gap"))
late_rate = safe_float(summary.get("late_rate"))
cancel_rate = safe_float(summary.get("cancel_rate"))
avg_discount = safe_float(summary.get("avg_discount"))
margin = profit / revenue * 100 if revenue else 0
risk_share = revenue_at_risk / revenue * 100 if revenue else 0
sev_class, sev_label = severity(late_rate, risk_share, sla_gap)
target_late_rate = 10.0
late_target_ratio = late_rate / target_late_rate if target_late_rate else 0
target_compare_text = (
    f"cao gấp {late_target_ratio:.1f} lần so với mục tiêu {target_late_rate:.0f}%"
    if late_rate > target_late_rate and late_target_ratio
    else f"đang trong mục tiêu {target_late_rate:.0f}%"
)
compare_label = trend_context["label"] if trend_context else "kỳ trước"
trend_prefix = f"Năm {trend_context['current_year']} " if trend_context else ""
revenue_delta_text = trend_prefix + fmt_delta_value(trend_current.get("revenue"), trend_previous.get("revenue"), fmt_money, compare_label)
profit_delta_text = trend_prefix + fmt_delta_value(trend_current.get("profit"), trend_previous.get("profit"), fmt_money, compare_label)
orders_delta_text = trend_prefix + fmt_delta_value(trend_current.get("orders"), trend_previous.get("orders"), fmt_num, compare_label)
late_delta_text = trend_prefix + fmt_delta_points(trend_current.get("late_rate"), trend_previous.get("late_rate"), compare_label)
risk_delta_text = trend_prefix + fmt_delta_value(trend_current.get("revenue_at_risk"), trend_previous.get("revenue_at_risk"), fmt_money, compare_label)
sla_delta_text = trend_prefix + fmt_delta_hours(trend_current.get("sla_gap"), trend_previous.get("sla_gap"), compare_label)
cancel_delta_text = trend_prefix + fmt_delta_points(trend_current.get("cancel_rate"), trend_previous.get("cancel_rate"), compare_label)
data_window = f"{min(years)}-{max(years)}" if years else "dữ liệu lịch sử"

top_issue = priority_df.iloc[0] if not priority_df.empty else None
top_issue_name = describe_issue(top_issue)
top_issue_copy = (
    f"Nhóm này có {fmt_money(top_issue['revenue_at_risk'])} doanh thu đang gặp rủi ro nếu không xử lý, "
    f"tỷ lệ trễ {fmt_pct(top_issue['late_rate'])}, {fmt_delay_days(top_issue['sla_gap'])} so với lịch hẹn."
    if top_issue is not None
    else "Hãy nới bộ lọc hoặc chọn chế độ tất cả đơn hàng để xem lại thứ tự ưu tiên."
)

st.markdown(
    f"""
    <div class="crisis-panel">
        <div class="crisis-kicker">Cảnh báo vận hành cần xử lý ngay</div>
        <div class="crisis-title">{fmt_pct(late_rate)} đơn hàng đang giao trễ hoặc có nguy cơ trễ</div>
        <p class="crisis-copy">
            Vấn đề ưu tiên hiện tại là {html_escape(top_issue_name)}. 
            Mức này {target_compare_text}; {late_delta_text}. 
            Dữ liệu đang dùng là dữ liệu lịch sử tham chiếu {data_window}, phục vụ nhận diện mẫu rủi ro và ưu tiên xử lý.
        </p>
        <div class="crisis-metrics">
            <div class="crisis-metric"><b>{fmt_num(late_orders)}</b><span>Đơn đã trễ hoặc có nguy cơ trễ theo dữ liệu vận hành</span></div>
            <div class="crisis-metric"><b>{fmt_money(revenue_at_risk)}</b><span>Doanh thu đang gặp rủi ro nếu không xử lý; {risk_delta_text}</span></div>
            <div class="crisis-metric"><b>{capitalize_first(fmt_delay_days(sla_gap))}</b><span>Độ lệch lịch hẹn trung bình toàn hệ thống</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

section(1, "Tình hình hiện tại", "Các chỉ số nền để đánh giá mức độ nghiêm trọng và tác động tài chính.")
st.markdown(
    f"""
    <div class="kpi-grid">
        {kpi_card("Doanh thu", fmt_full_money(revenue), revenue_delta_text, "blue")}
        {kpi_card("Lợi nhuận", fmt_full_money(profit), f"Biên lợi nhuận {fmt_pct(margin)}; {profit_delta_text}", "green" if margin >= 10 else "amber")}
        {kpi_card("Đơn hàng", fmt_num(orders), f"{orders_delta_text}; {fmt_num(late_orders)} đơn có rủi ro trễ", "blue")}
        {kpi_card("Tỷ lệ giao trễ", fmt_pct(late_rate), f"Ngưỡng mục tiêu {target_late_rate:.0f}%; {late_delta_text}", "red" if sev_class == "red" else "amber")}
        {kpi_card("Độ lệch lịch hẹn", fmt_delay_days(sla_gap), f"Tính trên toàn bộ đơn; {sla_delta_text}", "red" if sla_gap >= 1.5 else "amber" if sla_gap >= 0.75 else "green")}
        {kpi_card("Tỷ lệ hủy", fmt_pct(cancel_rate), f"{cancel_delta_text}; giảm giá TB {fmt_money(avg_discount)}", "amber" if cancel_rate >= 3 else "green")}
    </div>
    """,
    unsafe_allow_html=True,
)

process_col1, process_col2 = st.columns([7, 5])
with process_col1:
    st.markdown(
        f"""
        <div class="process-line">
            <div class="process-node"><b>Cung ứng hàng hóa</b><span>Giảm giá TB {fmt_money(avg_discount)}; ưu tiên chuẩn bị hàng cho danh mục có rủi ro.</span></div>
            <div class="process-node"><b>Sản phẩm & danh mục</b><span>{len(product_df)} nhóm sản phẩm đang được theo dõi theo lợi nhuận và giao hàng.</span></div>
            <div class="process-node"><b>Kinh doanh</b><span>Doanh thu {fmt_money(revenue)}; hủy đơn {fmt_pct(cancel_rate)}.</span></div>
            <div class="process-node"><b>Phân phối</b><span>Giao trễ {fmt_pct(late_rate)}; {fmt_delay_days(sla_gap)}.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with process_col2:
    if not delivery_df.empty:
        delivery_chart_df = delivery_df.copy()
        def delivery_color_key(status):
            status_text = str(status).lower()
            if "late" in status_text:
                return "Trễ"
            if "cancel" in status_text:
                return "Hủy"
            if "on time" in status_text:
                return "Đúng hạn"
            if "advance" in status_text:
                return "Sớm hơn hẹn"
            return "Khác"

        delivery_chart_df["Nhóm trạng thái"] = delivery_chart_df["delivery_status"].apply(delivery_color_key)
        fig_delivery = px.bar(
            delivery_chart_df,
            x="delivery_status",
            y="orders",
            color="Nhóm trạng thái",
            color_discrete_map={
                "Đúng hạn": "#10B981",
                "Sớm hơn hẹn": "#2563EB",
                "Trễ": "#DC2626",
                "Hủy": "#7F1D1D",
                "Khác": "#6B7280",
            },
            title="Trạng thái giao hàng",
        )
        fig_delivery.update_layout(showlegend=False, xaxis_title="", yaxis_title="Số đơn")
        st.plotly_chart(apply_chart_theme(fig_delivery, 255), use_container_width=True)


section(
    2,
    "Điểm nghẽn cần xử lý",
    "Xếp hạng chính theo số tiền bị ảnh hưởng; độ lệch lịch hẹn dùng để hiểu mức chậm, không phải tiêu chí duy nhất.",
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
    if not ml_risk_df.empty:
        ml_row = ml_risk_df.iloc[0]
        st.markdown(
            manager_card(
                "Tín hiệu dự báo",
                f"{fmt_num(ml_row.get('predicted_risk_orders'))} đơn rủi ro cao",
                (
                    f"Đây là tín hiệu bổ sung từ bảng dự báo ML, không cộng trực tiếp với "
                    f"{fmt_num(late_orders)} đơn đã trễ hoặc có nguy cơ trễ theo dữ liệu vận hành. "
                    f"Xác suất dự báo trung bình của nhóm này là {fmt_pct(ml_row.get('avg_predicted_risk'))}."
                ),
                "warning",
            ),
            unsafe_allow_html=True,
        )
with problem_col2:
    if not priority_df.empty:
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
            height=330,
        )

chart_col1, chart_col2 = st.columns([6, 6])
with chart_col1:
    if not monthly_df.empty:
        monthly_df = monthly_df.copy()
        monthly_df["late_ma3"] = monthly_df["late_rate"].rolling(3, min_periods=1).mean()
        fig_trend = go.Figure()
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_df["month"],
                y=monthly_df["late_rate"],
                name="Tỷ lệ trễ",
                mode="lines",
                line=dict(color="#CBD5E1", width=2, dash="dot"),
            )
        )
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_df["month"],
                y=monthly_df["late_ma3"],
                name="Trung bình 3 tháng",
                mode="lines+markers",
                line=dict(color="#2563EB", width=3),
            )
        )
        fig_trend.update_layout(title="Xu hướng trễ hạn theo thời gian", xaxis_title="", yaxis_title="Trễ (%)")
        st.plotly_chart(apply_chart_theme(fig_trend, 330), use_container_width=True)
with chart_col2:
    if not matrix_df.empty:
        matrix_pivot = matrix_df.pivot_table(
            index="order_region", columns="shipping_mode", values="late_rate", aggfunc="mean"
        ).fillna(0)
        fig_heat = px.imshow(
            matrix_pivot,
            aspect="auto",
            color_continuous_scale=["#D1FAE5", "#FEF3C7", "#FCA5A5"],
            text_auto=".1f",
            title="Bản đồ nhiệt rủi ro: khu vực x phương thức vận chuyển",
        )
        fig_heat.update_layout(
            xaxis_title="",
            yaxis_title="",
            coloraxis_colorbar=dict(title="Tỷ lệ trễ (%)"),
        )
        st.plotly_chart(apply_chart_theme(fig_heat, 330), use_container_width=True)


section(3, "Nguyên nhân và phương án xử lý", "Tập trung vào tuyến vận chuyển, nhóm sản phẩm và tín hiệu dự báo đang ảnh hưởng lớn nhất.")
solution_col1, solution_col2 = st.columns([7, 5])
with solution_col1:
    if not product_df.empty:
        fig_product = px.bar(
            product_df.sort_values("revenue_at_risk", ascending=True),
            x="revenue_at_risk",
            y="category_name",
            color="late_rate",
            orientation="h",
            color_continuous_scale=["#10B981", "#D97706", "#DC2626"],
            title="Danh mục sản phẩm có doanh thu đang gặp rủi ro cao nhất",
        )
        fig_product.update_layout(xaxis_title="", yaxis_title="", coloraxis_colorbar_title="Trễ (%)")
        st.plotly_chart(apply_chart_theme(fig_product, 395), use_container_width=True)
with solution_col2:
    root_cause = []
    if not shipping_df.empty:
        top_ship = shipping_df.sort_values("revenue_at_risk", ascending=False).iloc[0]
        root_cause.append(("Vận chuyển", f"{top_ship['shipping_mode']} đang có {fmt_money(top_ship['revenue_at_risk'])} doanh thu gặp rủi ro."))
    if not product_df.empty:
        top_product = product_df.iloc[0]
        root_cause.append(("Danh mục hàng", f"{top_product['category_name']} có {fmt_money(top_product['revenue_at_risk'])} doanh thu gặp rủi ro."))
    if not ml_features_df.empty:
        top_feature = ml_features_df.iloc[0]
        root_cause.append(("Tín hiệu dự báo", f"Yếu tố ảnh hưởng mạnh nhất đến dự báo: {top_feature['feature']}."))
    if not unstructured_df.empty:
        root_cause.append(("Tín hiệu truy cập", f"Đã phát hiện {len(unstructured_df)} bảng log/mô tả có thể hỗ trợ phân tích nhu cầu."))
    rows = ""
    for label, text in root_cause:
        rows += f"<div class='alert-row'><div><span class='tag amber'>{html_escape(label)}</span></div><div>{html_escape(capitalize_first(text))}</div></div>"
    st.markdown(
        f"""
        <div class="manager-card alert-card-full">
            <div class="card-kicker">Gợi ý ưu tiên từ hệ thống</div>
            {rows}
        </div>
        """,
        unsafe_allow_html=True,
    )


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

# Initialize selected priority index to None if not set
if "selected_priority_idx" not in st.session_state:
    st.session_state["selected_priority_idx"] = None

# Initialize checkbox states explicitly ONLY ONCE if not already in session state
if not priority_df.empty:
    for idx in priority_df.head(3).index:
        key = f"select_checkbox_{idx}"
        if key not in st.session_state:
            st.session_state[key] = (st.session_state["selected_priority_idx"] == idx)

# Render Section 4 Title
section(4, "Hành động ưu tiên cho phạm vi lọc", "")

# Split layout: content on left (9), actions on right (3)
col_left, col_right = st.columns([9, 3])

# Resolve currently selected row
selected_idx = st.session_state.get("selected_priority_idx")
selected_row = None
if not priority_df.empty:
    if selected_idx is not None and selected_idx in priority_df.index:
        selected_row = priority_df.loc[selected_idx]

with col_left:
    if not priority_df.empty:
        # Guarantee checkbox states match selected_priority_idx on new filter loads
        for idx in priority_df.head(3).index:
            key = f"select_checkbox_{idx}"
            if key not in st.session_state:
                st.session_state[key] = (st.session_state.get("selected_priority_idx") == idx)

        for rank, (idx, row) in enumerate(priority_df.head(3).iterrows(), start=1):
            order_title = describe_issue(row)
            order_copy = (
                f"{fmt_money(row['revenue_at_risk'])} doanh thu đang gặp rủi ro nếu không xử lý, "
                f"{fmt_num(row['late_orders'])} đơn trễ, tỷ lệ trễ {fmt_pct(row['late_rate'])}. "
                f"Khuyến nghị: ưu tiên đơn giá trị cao, kiểm tra năng lực vận chuyển và cập nhật lịch hẹn cho khách."
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
    
    # Action 1: carrier coordination
    if st.button("Điều phối vận tải", key="carrier_header_btn", type="primary", use_container_width=True):
        if selected_row is not None:
            order_title = describe_issue(selected_row)
            st.markdown(
                f"""
                <div class="modal-backdrop" id="modal-carrier-header" onclick="this.style.display='none'">
                    <div class="modal-box" onclick="event.stopPropagation()">
                        <span class="modal-close-btn" onclick="document.getElementById('modal-carrier-header').style.display='none'">&times;</span>
                        <div class="modal-icon-circle">🔔</div>
                        <div class="modal-title">Điều phối thành công</div>
                        <div class="modal-text">Đã gửi yêu cầu điều phối vận tải khẩn cấp đối với nhóm đơn: <br><b>{html_escape(order_title)}</b>. Hệ thống đang tối ưu lộ trình ngầm.</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
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
                "Tải CSV đơn ưu tiên",
                data=order_list_display.to_csv(index=False).encode("utf-8-sig"),
                file_name="don_uu_tien_selected.csv",
                mime="text/csv",
                key="priority_header_btn",
                type="primary",
                use_container_width=True,
            )
        else:
            st.button("Không có CSV đơn trễ", key="priority_header_empty", type="primary", disabled=True, use_container_width=True)
    else:
        if st.button("Tải CSV đơn ưu tiên", key="priority_header_disabled_trigger", type="primary", use_container_width=True):
            st.toast("Vui lòng chọn một nhóm đơn hàng ưu tiên bên trái trước!", icon="⚠️")
        
    # Action 3: customer notification
    if st.button("Thông báo khách hàng", key="notify_header_btn", type="primary", use_container_width=True):
        if selected_row is not None:
            st.markdown(
                f"""
                <div class="modal-backdrop" id="modal-notify-header" onclick="this.style.display='none'">
                    <div class="modal-box" onclick="event.stopPropagation()">
                        <span class="modal-close-btn" onclick="document.getElementById('modal-notify-header').style.display='none'">&times;</span>
                        <div class="modal-icon-circle">🔔</div>
                        <div class="modal-title">Đã phát thông báo</div>
                        <div class="modal-text">Hệ thống đã tự động gửi thông tin cập nhật lịch trình hẹn mới và lời xin lỗi đến toàn bộ khách hàng thuộc nhóm đơn bị ảnh hưởng.</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.toast("Vui lòng chọn một nhóm đơn hàng ưu tiên bên trái trước!", icon="⚠️")
            
    st.markdown('</div>', unsafe_allow_html=True)


with st.container(border=True):
    st.markdown("#### Bản tóm tắt tự động từ dữ liệu lịch sử")
    if top_issue is not None:
        briefing_lines = [
            f"Điểm cần xử lý trước là {top_issue_name}.",
            f"Nhóm này có {fmt_money(top_issue['revenue_at_risk'])} doanh thu đang gặp rủi ro nếu không xử lý và {fmt_num(top_issue['late_orders'])} đơn trễ.",
            f"Tỷ lệ trễ của nhóm là {fmt_pct(top_issue['late_rate'])}, cao hơn ngưỡng mục tiêu {target_late_rate:.0f}%.",
            "Đề xuất: ưu tiên đơn giá trị cao, kiểm tra năng lực phương thức vận chuyển hiện tại và thông báo lại lịch hẹn cho khách có nguy cơ bị ảnh hưởng.",
        ]
        if not unstructured_df.empty:
            briefing_lines.append("Đã có dữ liệu log/truy cập để hỗ trợ xem tín hiệu nhu cầu trước khi đơn hàng phát sinh.")
        for line in briefing_lines:
            st.markdown(f"- {line}")
    else:
        st.info("Chưa có đủ dữ liệu để tạo báo cáo tự động trong phạm vi lọc hiện tại.")


section(5, "Trợ lý phân tích dữ liệu", "Hỏi nhanh các tình huống vận hành mà không cần tự lọc nhiều biểu đồ.")
st.markdown("##### Gợi ý câu hỏi phân tích:")

suggestions = [
    "Top 5 sản phẩm Clothing có doanh thu cao nhất nhưng bị trễ giao hàng trong quý 3?",
    "Phương thức vận chuyển nào có doanh thu đang gặp rủi ro cao nhất?",
    "Khu vực nào có tỷ lệ giao trễ cao và biên lợi nhuận thấp?",
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

question = st.chat_input("Hỏi dữ liệu chuỗi cung ứng...")
if not question and st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

if question:
    client = get_groq_client()
    if client is None:
        st.error("Chưa có khóa AI nên chưa dùng được trợ lý phân tích.")
    else:
        with st.status("Trợ lý đang phân tích dữ liệu...", expanded=True) as status:
            try:
                status.update(label="Đang hiểu câu hỏi và lấy dữ liệu phù hợp.", state="running")
                sql_response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": SCHEMA_CONTEXT},
                        {"role": "user", "content": question},
                    ],
                    temperature=0,
                    max_tokens=500,
                )
                sql = extract_sql(sql_response.choices[0].message.content)
                if not is_safe_select(sql):
                    status.update(label="Không thể tạo truy vấn an toàn cho câu hỏi này.", state="error")
                    st.code(sql, language="sql")
                else:
                    status.update(label="Đang truy vấn kho dữ liệu.", state="running")
                    result_df = con.execute(sql).df()
                    
                    try:
                        status.update(label="Trợ lý AI đang phân tích dữ liệu và lập luận...", state="running")
                        # Chuyển đổi tối đa 30 dòng dữ liệu thành dạng text để LLM đọc và hiểu bản chất
                        preview = result_df.head(30).to_string(index=False) if not result_df.empty else "Không có dữ liệu phù hợp."
                        
                        # Gọi LLM sinh phản hồi chuyên sâu
                        insight_response = client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "Bạn là chuyên gia phân tích chuỗi cung ứng (Supply Chain Analyst) cấp cao, "
                                        "có nhiều năm kinh nghiệm tư vấn cho ban giám đốc về logistics và quản trị rủi ro giao hàng. "
                                        "Dựa CHÍNH XÁC vào dữ liệu được cung cấp, không tự bịa thêm số liệu nào ngoài những gì đã cho. "
                                        "Hãy trả lời bằng tiếng Việt, văn phong chuyên nghiệp nhưng dễ hiểu cho nhà quản lý không rành kỹ thuật. "
                                        "LUÔN LUÔN trình bày đầy đủ và chi tiết theo đúng cấu trúc sau, mỗi phần ít nhất 2-3 câu hoặc 2-3 bullet point, "
                                        "không trả lời qua loa, không rút gọn:\n\n"
                                        "**Nhận xét chi tiết:** Phân tích sâu các số liệu quan trọng nhất trong dữ liệu, "
                                        "so sánh giữa các nhóm (nếu có), chỉ ra xu hướng hoặc điểm bất thường đáng chú ý.\n\n"
                                        "**Đánh giá rủi ro:** Nêu rõ mức độ nghiêm trọng của rủi ro, ảnh hưởng tiềm tàng tới doanh thu/uy tín "
                                        "nếu không xử lý, và nguyên nhân gốc rễ có thể gây ra tình trạng này.\n\n"
                                        "**Khuyến nghị hành động:** Đề xuất ít nhất 2-3 hành động cụ thể, khả thi, có thể triển khai ngay, "
                                        "ưu tiên theo mức độ quan trọng (đánh số 1, 2, 3).\n\n"
                                        "**Kết luận ngắn:** Tóm tắt lại trong 1 câu thông điệp quan trọng nhất gửi tới nhà quản lý."
                                    ),
                                },
                                {
                                    "role": "user",
                                    "content": f"Câu hỏi: {question}\n\nKết quả truy vấn dữ liệu thật:\n{preview}\n\nHãy phân tích đầy đủ và đưa khuyến nghị chi tiết.",
                                },
                            ],
                            temperature=0.5,
                            max_tokens=1600,
                        )
                        
                        status.update(label="Phân tích hoàn tất! Xem kết quả tại đây.", state="complete", expanded=False)
                        
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
                        status.update(label="Trợ lý phân tích gặp lỗi.", state="error")
                        st.error(f"Lỗi trong quá trình Trợ lý phân tích lập luận chuyên sâu: {exc}")
                    
                    st.markdown("##### Câu hỏi")
                    st.write(question)
                    with st.expander("Truy vấn dữ liệu đã sử dụng"):
                        st.code(sql, language="sql")
                    if not result_df.empty:
                        display_result_df = rename_for_display(result_df)
                        auto_fig = make_auto_chart(display_result_df, "Kết quả phân tích từ dữ liệu")
                        if auto_fig is not None:
                            st.plotly_chart(auto_fig, use_container_width=True)
                        st.dataframe(display_result_df, use_container_width=True, hide_index=True)
                        
                    st.markdown("##### Nhận định và hành động đề xuất")
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
                status.update(label="Trợ lý phân tích gặp lỗi.", state="error")
                st.error(f"Lỗi xử lý: {exc}")
elif st.session_state["last_question"]:
    with st.status("Hoàn tất.", state="complete", expanded=False):
        st.markdown("##### Câu hỏi")
        st.write(st.session_state["last_question"])
        with st.expander("Truy vấn dữ liệu đã sử dụng"):
            st.code(st.session_state["last_sql"], language="sql")
        
        result_df = st.session_state["last_result_df"]
        if result_df is not None and not result_df.empty:
            display_result_df = rename_for_display(result_df)
            auto_fig = make_auto_chart(display_result_df, "Kết quả phân tích từ dữ liệu")
            if auto_fig is not None:
                st.plotly_chart(auto_fig, use_container_width=True)
            st.dataframe(display_result_df, use_container_width=True, hide_index=True)
            
        st.markdown("##### Nhận định và hành động đề xuất")
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