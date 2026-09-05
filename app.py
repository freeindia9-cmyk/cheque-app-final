import streamlit as st
import pandas as pd
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime, timedelta
import random
import re
import io
import json

# ==========================================
# 1. PAGE CONFIGURATION & STATE INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="8K Cyberpunk Cheque Dispatcher Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if 'crm_data' not in st.session_state:
    st.session_state['crm_data'] = None
if 'sent_count' not in st.session_state:
    st.session_state['sent_count'] = 0
if 'failed_count' not in st.session_state:
    st.session_state['failed_count'] = 0
if 'stop_dispatch' not in st.session_state:
    st.session_state['stop_dispatch'] = False
if 'dispatch_logs' not in st.session_state:
    st.session_state['dispatch_logs'] = []
if 'validation_alerts' not in st.session_state:
    st.session_state['validation_alerts'] = []
if 'theme_color' not in st.session_state:
    st.session_state['theme_color'] = "Electric Cyan"

# ==========================================
# 2. ADVANCED DYNAMIC CSS & UI STYLING ENGINE
# ==========================================
def inject_custom_styles():
    st.markdown("""
    <style>
        /* Global Background and Fonts */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: radial-gradient(circle at 50% 20%, #0d1b2a, #0b132b, #040814) !important;
            color: #e0e1dd !important;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0d1322 !important;
            border-right: 2px solid #00b4d8 !important;
            box-shadow: 5px 0 25px rgba(0, 180, 216, 0.25);
        }

        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] h3 {
            color: #90e0ef !important;
            font-weight: 700 !important;
            text-shadow: 0 0 8px rgba(144, 224, 239, 0.5) !important;
        }

        /* High Visibility Text Accent Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #48cae4 !important;
            text-shadow: 0 0 12px rgba(72, 202, 228, 0.6) !important;
            font-weight: 800 !important;
        }

        p, span, label {
            color: #e0e1dd !important;
        }

        /* Input Controls, Textboxes & Selects */
        input, select, textarea, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
            background-color: #1b263b !important;
            color: #00f5d4 !important;
            border: 2px solid #00b4d8 !important;
            border-radius: 12px !important;
            box-shadow: 0 0 15px rgba(0, 180, 216, 0.3) !important;
            font-weight: 700 !important;
            transition: all 0.4s ease-in-out !important;
        }

        input:focus, div[data-baseweb="input"]:focus-within {
            border-color: #00f5d4 !important;
            box-shadow: 0 0 25px rgba(0, 245, 212, 0.8) !important;
        }

        /* HIGH-VISIBILITY DATA GRID FIX (NO MORE BLACK BACKGROUND/TEXT ISSUE) */
        div[data-testid="stDataFrame"], div[data-testid="data-grid-canvas"], div[aria-label="Data Grid"] {
            background-color: #16243b !important;
            border: 2px solid #00b4d8 !important;
            border-radius: 16px !important;
            padding: 8px !important;
            box-shadow: 0 0 30px rgba(0, 180, 216, 0.4) !important;
        }

        /* Grid Cells & Header Contrast Enhancement */
        [data-testid="stDataFrame"] * {
            background-color: #16243b !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* Glide Data Grid Specific Cell Rules */
        .gdg-header-cell, .gdg-cell, .dvn-scroller, .glideDataEditor {
            background-color: #101d30 !important;
            color: #00f5d4 !important;
            border-color: #00b4d8 !important;
        }

        div[data-testid="stDataFrame"] iframe, 
        div[data-testid="stDataFrame"] canvas {
            background-color: #0b132b !important;
            color: #00f5d4 !important;
        }

        /* Modern File Uploader Dropzone */
        [data-testid="stFileUploadDropzone"], div[data-testid="stFileUploader"] section {
            background: linear-gradient(135deg, #101d30, #0c1827) !important;
            border: 2px dashed #00b4d8 !important;
            border-radius: 16px !important;
            box-shadow: 0 0 20px rgba(0, 180, 216, 0.3) !important;
            transition: all 0.5s ease-in-out !important;
        }

        [data-testid="stFileUploadDropzone"]:hover, div[data-testid="stFileUploader"] section:hover {
            border-color: #00f5d4 !important;
            box-shadow: 0 0 35px rgba(0, 245, 212, 0.6) !important;
        }

        [data-testid="stFileUploadDropzone"] button, div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
            color: #ffffff !important;
            border: 2px solid #90e0ef !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
            box-shadow: 0 0 15px rgba(0, 180, 216, 0.6) !important;
            transition: all 0.5s ease-in-out !important;
        }

        [data-testid="stFileUploadDropzone"] button:hover, div[data-testid="stFileUploader"] button:hover {
            transform: translateY(-3px) scale(1.03);
            background: linear-gradient(135deg, #00f5d4, #00b4d8) !important;
            color: #000000 !important;
            box-shadow: 0 0 30px rgba(144, 224, 239, 0.9) !important;
        }

        /* Top Cyber Header Banner */
        .header-wrapper {
            margin-top: 10px !important;
            margin-bottom: 30px !important;
            background: rgba(13, 27, 42, 0.85);
            border: 2px solid #00b4d8;
            box-shadow: 0 0 40px rgba(0, 180, 216, 0.5);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
        }

        .main-title {
            color: #00f5d4 !important;
            font-size: 38px;
            font-weight: 900;
            letter-spacing: 2px;
            margin: 0;
            text-shadow: 0 0 25px rgba(0, 245, 212, 0.8) !important;
        }

        .subtitle-badge {
            display: inline-block;
            background: #0b132b;
            border: 1.5px solid #ffb703;
            padding: 6px 24px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 800;
            color: #ffb703 !important;
            margin-top: 12px;
            box-shadow: 0 0 15px rgba(255, 183, 3, 0.5);
        }

        /* Analytics Metric Cards */
        .metric-card-box {
            background: #111d33 !important;
            border: 2px solid #00b4d8;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0, 180, 216, 0.3);
            transition: all 0.4s ease-in-out;
        }

        .metric-card-box:hover {
            transform: translateY(-5px);
            border-color: #00f5d4;
            box-shadow: 0 0 35px rgba(0, 245, 212, 0.7);
        }

        .metric-label {
            font-size: 13px;
            color: #90e0ef !important;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.2px;
        }

        .metric-value-num {
            font-size: 36px;
            font-weight: 900;
            margin-top: 8px;
            color: #ffffff !important;
            text-shadow: 0 0 18px rgba(255, 255, 255, 0.8) !important;
        }

        /* Dynamic Glowing Action Buttons */
        div.stButton > button, div.stDownloadButton > button {
            font-weight: 900 !important;
            border-radius: 14px !important;
            padding: 16px 24px !important;
            font-size: 15px !important;
            letter-spacing: 1px !important;
            transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1) !important;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.8) !important;
        }

        /* Launch Dispatch Primary Button */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #00b4d8, #0077b6) !important;
            color: #ffffff !important;
            border: 2px solid #00f5d4 !important;
            box-shadow: 0 0 25px rgba(0, 245, 212, 0.6) !important;
            width: 100% !important;
        }

        div.stButton > button[kind="primary"]:hover {
            transform: translateY(-3px) scale(1.02);
            background: linear-gradient(135deg, #00f5d4, #0096c7) !important;
            box-shadow: 0 0 45px rgba(0, 245, 212, 0.95) !important;
        }

        /* Emergency Stop Secondary Button */
        div.stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #d90429, #ef233c) !important;
            color: #ffffff !important;
            border: 2px solid #ff4d6d !important;
            box-shadow: 0 0 25px rgba(239, 35, 60, 0.6) !important;
            width: 100% !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            transform: translateY(-3px) scale(1.02);
            background: linear-gradient(135deg, #ff4d6d, #b7094c) !important;
            box-shadow: 0 0 45px rgba(255, 77, 109, 0.95) !important;
        }

        /* Download Button */
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #3a0ca3, #4361ee) !important;
            color: #ffffff !important;
            border: 2px solid #4cc9f0 !important;
            box-shadow: 0 0 25px rgba(76, 201, 240, 0.6) !important;
            width: 100% !important;
        }

        div.stDownloadButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            background: linear-gradient(135deg, #4cc9f0, #7209b7) !important;
            box-shadow: 0 0 45px rgba(76, 201, 240, 0.95) !important;
        }

        /* Log Output Panel */
        .log-box {
            background-color: #060a12;
            border: 1px solid #00b4d8;
            border-radius: 12px;
            padding: 16px;
            max-height: 280px;
            overflow-y: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 13px;
            color: #48cae4;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_styles()

# ==========================================
# 3. HELPER UTILITIES & DATA VALIDATORS
# ==========================================
def get_field_strict(row, column_aliases, default_val="N/A"):
    """
    Extracts values dynamically across various possible column headers.
    """
    clean_aliases = [re.sub(r'[^a-zA-Z0-9]', '', str(a)).lower() for a in column_aliases]
    for col in row.index:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', str(col)).lower()
        if col_clean in clean_aliases:
            val = str(row[col]).strip()
            if val and val.lower() not in ["nan", "none", "n/a", "", "null"]:
                return val
    return default_val

def validate_email_address(email_str):
    """
    Validates email format using regex pattern matching.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email_str).strip()))

def perform_batch_data_audit(dataframe):
    """
    Audits incoming dataframe for invalid emails, missing records, or empty fields.
    """
    alerts = []
    if dataframe is None or dataframe.empty:
        return ["Dataset is empty. Please upload data or load default sample records."]

    total_rows = len(dataframe)
    invalid_email_count = 0
    missing_account_count = 0

    for idx, row in dataframe.iterrows():
        email_val = get_field_strict(row, ["Email", "Email ID", "Mail"], "")
        if not validate_email_address(email_val):
            invalid_email_count += 1

        acc_val = get_field_strict(row, ["Account Number", "Account No", "Acc"], "")
        if acc_val == "N/A" or not acc_val:
            missing_account_count += 1

    if invalid_email_count > 0:
        alerts.append(f"⚠️ {invalid_email_count} out of {total_rows} records contain invalid/missing Email IDs.")
    if missing_account_count > 0:
        alerts.append(f"⚠️ {missing_account_count} records are missing Account Numbers.")
    if not alerts:
        alerts.append("✅ Data Audit Passed: All records are well-formatted and ready for dispatch.")
    
    return alerts

# ==========================================
# 4. DEFAULT DATASET GENERATION ENGINE
# ==========================================
@st.cache_data
def generate_default_100_records():
    """
    Generates a full 100-record dataset for initial demonstration.
    """
    parties = [
        "Aarav Sharma", "Priya Patel", "Rahul Verma", "Ananya Iyer", 
        "Amit Gupta", "Vikram Singh", "Neha Kapoor", "Sanjay Dutt",
        "Pooja Joshi", "Rajesh Kumar", "Meera Nair", "Deepak Chopra"
    ]
    places = ["Patna", "Delhi", "Mumbai", "Kolkata", "Bangalore", "Ranchi", "Varanasi", "Ahmedabad", "Jaipur"]
    banks = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Canara Bank"]
    
    records = []
    base_date = datetime(2026, 8, 1)
    
    for i in range(1, 101):
        party_name = parties[(i - 1) % len(parties)]
        email_prefix = party_name.split()[0].lower() + str(i)
        entry_dt = base_date + timedelta(days=(i % 25))
        account_no = f"35{random.randint(1000000000, 9999999999)}"
        
        records.append({
            "Record ID": f"REC-{1000+i}",
            "Date": entry_dt.strftime("%Y-%m-%d"),
            "Party Name": party_name,
            "Account Number": account_no,
            "Email": f"{email_prefix}@clientdomain.com",
            "Place": random.choice(places),
            "Bank Name": random.choice(banks),
            "Number of cheque used in AIL": random.randint(1, 10),
            "Number of cheque used In AHPL": random.randint(1, 10),
            "Total cheque in hand AIL": random.randint(5, 25),
            "Total cheque in hand AHPL": random.randint(5, 25)
        })
    return pd.DataFrame(records)

if st.session_state['crm_data'] is None:
    st.session_state['crm_data'] = generate_default_100_records()

# ==========================================
# 5. SIDEBAR CONFIGURATION STUDIO
# ==========================================
with st.sidebar:
    st.markdown("### 🖼️ Branding & Identity Studio")
    logo_file = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"], key="logo_uploader")
    if logo_file:
        st.image(logo_file, use_container_width=True)
    
    st.divider()
    st.markdown("### 🔑 Secure SMTP Engine Setup")
    smtp_server = st.text_input("SMTP Server Host", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587, min_value=1, max_value=65535)
    sender_email = st.text_input("Sender Email ID", placeholder="your_email@gmail.com")
    app_password = st.text_input("16-Digit App Password", type="password")
    dispatch_delay = st.slider("Dispatch Rate Delay (Sec)", 0.2, 5.0, 0.8, step=0.1)
    
    st.divider()
    st.markdown("### 📝 Email Content Settings")
    email_subject_prefix = st.text_input("Custom Email Subject Prefix", value="BUFFER CHEQUE DETAILS", key="sb_email_subject")
    custom_cfa_title = st.text_input("CFA Header Title", value="RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA", key="sb_cfa_title")
    
    st.divider()
    st.markdown("### 🛠️ Data Management Tools")
    if st.button("🔄 Reset to Default 100 Sample Records", use_container_width=True):
        st.session_state['crm_data'] = generate_default_100_records()
        st.session_state['sent_count'] = 0
        st.session_state['failed_count'] = 0
        st.session_state['dispatch_logs'] = []
        st.rerun()

# ==========================================
# 6. MAIN APP HEADER BANNER
# ==========================================
st.markdown("""
<div class="header-wrapper">
    <h1 class="main-title">DHARMENDRA KUMAR (MISHRA)</h1>
    <span class="subtitle-badge">✨ ARCHITECT & DESIGNER: RAJVEER</span>
    <p style="color: #90e0ef; margin-top: 12px; font-weight: 700; font-size: 16px;">
        ⚡ 8K ULTRA-DYNAMIC CHEQUE DISPATCHER & AUTOMATED EMAIL MANAGEMENT ENGINE
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. BATCH FILE IMPORT & VALIDATION SECTION
# ==========================================
st.markdown("### 📁 Import Custom Excel/CSV Batch File")
uploaded_file = st.file_uploader("Upload Batch File (XLSX / CSV)", type=["xlsx", "csv"], key="batch_uploader")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            imported_df = pd.read_csv(uploaded_file)
        else:
            imported_df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        imported_df.columns = [str(col).strip() for col in imported_df.columns]
        st.session_state['crm_data'] = imported_df
        st.session_state['sent_count'] = 0
        st.session_state['failed_count'] = 0
        st.session_state['dispatch_logs'] = []
        st.success(f"✅ Successfully loaded {len(imported_df)} records from file!")
    except Exception as err:
        st.error(f"❌ Failed to parse uploaded file: {err}")

df = st.session_state['crm_data']
st.session_state['validation_alerts'] = perform_batch_data_audit(df)

# ==========================================
# 8. ANALYTICS & METRICS PANEL
# ==========================================
total_records = len(df) if df is not None else 0
sent_count = st.session_state['sent_count']
failed_count = st.session_state['failed_count']
pending_count = max(0, total_records - (sent_count + failed_count))

st.markdown("### 📊 Real-time Batch Metrics & Validation")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Total Records</div><div class="metric-value-num" style="color:#48cae4 !important;">{total_records}</div></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Sent Success</div><div class="metric-value-num" style="color:#00f5d4 !important;">{sent_count}</div></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Failed / Invalid</div><div class="metric-value-num" style="color:#ff4d6d !important;">{failed_count}</div></div>', unsafe_allow_html=True)
with col_m4:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Pending Dispatch</div><div class="metric-value-num" style="color:#ffb703 !important;">{pending_count}</div></div>', unsafe_allow_html=True)

# Show Data Audit Alerts
with st.expander("🔍 System Data Audit & Health Report", expanded=False):
    for alert in st.session_state['validation_alerts']:
        st.write(alert)

st.markdown("---")

# ==========================================
# 9. INTERACTIVE DATA GRID & FILTERING
# ==========================================
st.markdown("### ✏️ Interactive Data Grid")

search_query = st.text_input("🔍 Quick Search Filter (Party Name, Email, or Bank)", placeholder="Type to filter records...")

if df is not None and not df.empty:
    if search_query:
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

    edited_df = st.data_editor(
        filtered_df,
        num_rows="dynamic",
        use_container_width=True,
        height=380,
        key="data_editor_grid"
    )
    
    if not search_query:
        st.session_state['crm_data'] = edited_df
        df = st.session_state['crm_data']

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 10. DISPATCH CONTROL ACTION BUTTONS
# ==========================================
st.markdown("### 🚀 Dispatch Control Actions")
col_b1, col_b2, col_b3 = st.columns([1.8, 1.1, 1.1])

with col_b1:
    start_dispatch_btn = st.button("🚀 LAUNCH CHEQUE DETAILS DISPATCH", type="primary", use_container_width=True)
with col_b2:
    stop_dispatch_btn = st.button("🛑 EMERGENCY STOP", type="secondary", use_container_width=True)
with col_b3:
    csv_buffer = io.StringIO()
    if df is not None:
        df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 EXPORT CLEAN CSV",
        data=csv_buffer.getvalue(),
        file_name=f"Cheque_Dispatch_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

if stop_dispatch_btn:
    st.session_state['stop_dispatch'] = True
    st.warning("🛑 Emergency Stop Triggered by User!")

st.markdown("---")

# ==========================================
# 11. HTML EMAIL TEMPLATE GENERATOR
# ==========================================
def build_email_template(party, date_val, acc, place, bank, u_ail, u_ahpl, h_ail, h_ahpl, cfa_title, email_title):
    """
    Generates HTML email content linking dynamically with Sidebar Email Content inputs.
    """
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @keyframes fullSplashAnimation {
            0% { opacity: 1; visibility: visible; }
            80% { opacity: 1; visibility: visible; }
            100% { opacity: 0; visibility: hidden; height: 0; padding: 0; margin: 0; }
        }

        .splash-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, #0077b6, #023e8a, #03045e);
            z-index: 99999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            animation: fullSplashAnimation 4s forwards ease-in-out;
            box-sizing: border-box;
            padding: 20px;
        }

        .splash-title {
            color: #00f5d4;
            font-size: 26px;
            font-weight: 900;
            font-family: Arial, sans-serif;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(0, 245, 212, 0.9);
            margin: 0;
        }

        .splash-sub {
            color: #caf0f8;
            font-size: 14px;
            font-weight: bold;
            margin-top: 12px;
            letter-spacing: 1px;
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body style="margin:0; padding:20px; background-color:#f4f6f8; font-family: 'Segoe UI', Arial, sans-serif;">

  <!-- 4 SECONDS FULL-SCREEN SPLASH OVERLAY -->
  <div class="splash-overlay">
      <div class="splash-title">RAMA ENTERPRISES</div>
      <div class="splash-sub">ABBOTT INDIA LTD, PATNA</div>
  </div>

  <!-- MAIN EMAIL BODY -->
  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; background-color: #0b132b; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
    <tr>
      <td style="padding: 24px; text-align: center;">
        <div style="background: linear-gradient(135deg, #00b4d8, #0077b6); border-radius: 12px; padding: 18px 10px; text-align: center; box-shadow: 0 0 20px rgba(0, 180, 216, 0.6);">
          <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 900; letter-spacing: 1px;">
            """ + str(email_title).upper() + """
          </h1>
        </div>
        <div style="margin-top: 12px; font-weight: bold; color: #90e0ef; font-size: 13px;">
          ✨ """ + str(cfa_title) + """
        </div>
      </td>
    </tr>
    <tr>
      <td style="padding: 0 28px 28px 28px;">
        <p style="color: #ffffff; font-size: 16px; margin-bottom: 8px;">Dear <b style="color: #00f5d4;">""" + str(party) + """</b>,</p>
        <p style="color: #caf0f8; font-size: 14px; margin-top: 0; margin-bottom: 22px;">Please find below the updated summary of your cheque records:</p>
        <table border="0" cellpadding="12" cellspacing="0" width="100%" style="border-collapse: collapse; background-color: #1c2541; border-radius: 10px; overflow: hidden;">
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td width="50%" style="color: #90e0ef; font-weight: bold; font-size: 14px;">📅 Date</td>
            <td width="50%" style="color: #00f5d4; font-weight: bold; font-size: 14px;">""" + str(date_val) + """</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">👤 Party Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">""" + str(party) + """</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🔢 Account Number</td>
            <td style="color: #48cae4; font-weight: bold; font-size: 14px;">""" + str(acc) + """</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">📍 Place</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">""" + str(place) + """</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🏦 Bank Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">""" + str(bank) + """</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AIL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">""" + str(u_ail) + """</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AHPL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">""" + str(u_ahpl) + """</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AIL</td>
            <td style="color: #00f5d4; font-weight: bold; font-size: 14px;">""" + str(h_ail) + """</td>
          </tr>
          <tr>
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AHPL</td>
            <td style="color: #00f5d4; font-weight: bold; font-size: 14px;">""" + str(h_ahpl) + """</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td style="background-color: #1c2541; padding: 20px; text-align: center; border-top: 1px solid #3a5a40;">
        <div style="color: #00f5d4; font-weight: 800; font-size: 14px;">""" + str(cfa_title) + """</div>
      </td>
    </tr>
  </table>
</body>
</html>"""
    return html_content

# ==========================================
# 12. INTERACTIVE EMAIL INBOX SIMULATOR
# ==========================================
st.markdown("### 👁️ Interactive Email Inbox Simulator")
sim_col1, sim_col2 = st.columns([1, 1], gap="large")

with sim_col1:
    st.markdown("#### 🧪 Test Data Controls")
    sim_party = st.text_input("Simulated Party Name", value="RAJVEER", key="sim_party")
    sim_acc = st.text_input("Simulated Account Number", value="351800949903", key="sim_acc")
    sim_place = st.text_input("Simulated Place", value="Patna", key="sim_place")
    sim_bank = st.text_input("Simulated Bank Name", value="State Bank of India", key="sim_bank")
    sim_u_ail = st.text_input("Used AIL Cheques", value="4", key="sim_u_ail")
    sim_u_ahpl = st.text_input("Used AHPL Cheques", value="2", key="sim_u_ahpl")
    sim_h_ail = st.text_input("Hand AIL Cheques", value="15", key="sim_h_ail")
    sim_h_ahpl = st.text_input("Hand AHPL Cheques", value="18", key="sim_h_ahpl")

with sim_col2:
    st.markdown("#### 📱 Live Rendered Email Preview")
    # Dynamically pass sidebar inputs to email generator for real-time reactive update
    preview_html = build_email_template(
        sim_party, datetime.now().strftime("%Y-%m-%d"), sim_acc, sim_place, sim_bank,
        sim_u_ail, sim_u_ahpl, sim_h_ail, sim_h_ahpl, custom_cfa_title, email_subject_prefix
    )
    st.components.v1.html(preview_html, height=500, scrolling=True)

# ==========================================
# 13. AUTOMATED DISPATCH EXECUTION ENGINE
# ==========================================
if start_dispatch_btn:
    st.session_state['stop_dispatch'] = False
    st.session_state['sent_count'] = 0
    st.session_state['failed_count'] = 0
    st.session_state['dispatch_logs'] = []

    if not sender_email or not app_password:
        st.error("⚠️ Sender Email ID or App Password is missing in the sidebar!")
    elif df is None or df.empty:
        st.error("⚠️ No data available to dispatch!")
    else:
        st.markdown("---")
        st.markdown("### 📡 Live Dispatch Stream")
        
        progress_bar = st.progress(0)
        status_box = st.empty()
        log_container = st.empty()

        try:
            # Establish SMTP Connection
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()
            server.login(sender_email.strip(), app_password.replace(" ", ""))

            for idx in range(len(df)):
                if st.session_state['stop_dispatch']:
                    st.warning("🛑 Dispatch process halted manually!")
                    st.session_state['dispatch_logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] STOP: Dispatch manually interrupted.")
                    break

                row = df.iloc[idx]
                rec_date = get_field_strict(row, ["Date", "Entry Date"], datetime.now().strftime("%Y-%m-%d"))
                party_name = get_field_strict(row, ["Party Name", "Party"], "Valued Customer")
                account_val = get_field_strict(row, ["Account Number", "Account No"], "N/A")
                target_email = get_field_strict(row, ["Email", "Email ID"], "").strip()
                place_val = get_field_strict(row, ["Place", "City"], "N/A")
                bank_val = get_field_strict(row, ["Bank Name", "Bank"], "N/A")
                
                used_ail = get_field_strict(row, ["Number of cheque used in AIL"], "0")
                used_ahpl = get_field_strict(row, ["Number of cheque used In AHPL"], "0")
                hand_ail = get_field_strict(row, ["Total cheque in hand AIL"], "0")
                hand_ahpl = get_field_strict(row, ["Total cheque in hand AHPL"], "0")

                timestamp_str = datetime.now().strftime('%H:%M:%S')

                if validate_email_address(target_email):
                    msg = MIMEMultipart('alternative')
                    msg['From'] = formataddr((custom_cfa_title, sender_email.strip()))
                    msg['To'] = target_email
                    msg['Subject'] = f"{email_subject_prefix} - {party_name} ({rec_date})"

                    full_body = build_email_template(
                        party_name, rec_date, account_val, place_val, bank_val,
                        used_ail, used_ahpl, hand_ail, hand_ahpl, custom_cfa_title, email_subject_prefix
                    )
                    msg.attach(MIMEText(full_body, 'html'))
                    
                    try:
                        server.sendmail(sender_email.strip(), target_email, msg.as_string())
                        st.session_state['sent_count'] += 1
                        status_msg = f"🔵 [{idx+1}/{len(df)}] Sent to {party_name} ({target_email})"
                        st.session_state['dispatch_logs'].append(f"[{timestamp_str}] SUCCESS: {status_msg}")
                        status_box.info(status_msg)
                    except Exception as send_err:
                        st.session_state['failed_count'] += 1
                        status_msg = f"🔴 [{idx+1}/{len(df)}] Failed sending to {target_email}: {send_err}"
                        st.session_state['dispatch_logs'].append(f"[{timestamp_str}] ERROR: {status_msg}")
                        status_box.error(status_msg)
                else:
                    st.session_state['failed_count'] += 1
                    status_msg = f"⚠️ [{idx+1}/{len(df)}] Skipped invalid email for: {party_name}"
                    st.session_state['dispatch_logs'].append(f"[{timestamp_str}] WARNING: {status_msg}")
                    status_box.warning(status_msg)

                # Progress & Logs Update
                progress = (idx + 1) / len(df)
                progress_bar.progress(progress)
                
                # Render Console Logs
                log_html = "<div class='log-box'>" + "<br>".join(st.session_state['dispatch_logs']) + "</div>"
                log_container.markdown(log_html, unsafe_allow_html=True)
                
                time.sleep(dispatch_delay)

            server.quit()
            st.balloons()
            st.success("🎉 Cheque Record Dispatch Completed Successfully!")

        except Exception as conn_err:
            st.error(f"❌ Connection Failure: {conn_err}")
            st.session_state['dispatch_logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] FATAL: {conn_err}")

# Display Historical Activity Logs if Available
if st.session_state['dispatch_logs']:
    st.markdown("### 📜 Dispatch Logs Console")
    st.markdown("<div class='log-box'>" + "<br>".join(st.session_state['dispatch_logs']) + "</div>", unsafe_allow_html=True)
