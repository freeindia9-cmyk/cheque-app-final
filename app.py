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
    page_title="DHARMENDRA KUMAR (MISHRA) - Bulk Dispatcher",
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

# ==========================================
# 2. ADVANCED DYNAMIC CSS & UI STYLING ENGINE
# ==========================================
def inject_custom_styles():
    st.markdown("""
    <style>
        /* Global Canvas Styling */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #070d18 !important;
            color: #e0e1dd !important;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        }

        /* Sidebar Customization */
        section[data-testid="stSidebar"] {
            background-color: #0b132b !important;
            border-right: 2px solid #00b4d8 !important;
            box-shadow: 5px 0 25px rgba(0, 180, 216, 0.25);
        }

        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] h3 {
            color: #90e0ef !important;
            font-weight: 700 !important;
        }

        /* Accent Text & Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #48cae4 !important;
            font-weight: 800 !important;
        }

        p, span, label {
            color: #e0e1dd !important;
        }

        /* Form Text Inputs & Input Boxes */
        input, select, textarea, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
            background-color: #0f1c32 !important;
            color: #00f5d4 !important;
            border: 1px solid #00b4d8 !important;
            border-radius: 8px !important;
        }

        /* Cyber File Uploader & Dropzone Area */
        div[data-testid="stFileUploader"] {
            background-color: #0b1528 !important;
            border: 2px dashed #00b4d8 !important;
            border-radius: 12px !important;
            padding: 16px !important;
        }

        [data-testid="stFileUploadDropzone"] {
            background-color: #091222 !important;
            border: 1px dashed #00b4d8 !important;
            border-radius: 10px !important;
        }

        /* Custom Unified Button Styling (Upload, Browse & Standard Buttons) */
        div[data-testid="stFileUploader"] button, 
        div[data-testid="stFileUploader"] label[role="button"],
        [data-testid="stFileUploadDropzone"] button,
        button[data-testid="baseButton-secondary"],
        button[data-testid="baseButton-primary"],
        .stButton > button {
            background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
            color: #ffffff !important;
            border: 1px solid #00f5d4 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            padding: 8px 18px !important;
            box-shadow: 0 0 12px rgba(0, 180, 216, 0.4) !important;
            transition: all 0.3s ease-in-out !important;
        }

        div[data-testid="stFileUploader"] button:hover, 
        div[data-testid="stFileUploader"] label[role="button"]:hover,
        [data-testid="stFileUploadDropzone"] button:hover,
        button[data-testid="baseButton-secondary"]:hover,
        button[data-testid="baseButton-primary"]:hover,
        .stButton > button:hover {
            background: linear-gradient(135deg, #00b4d8, #00f5d4) !important;
            color: #070d18 !important;
            box-shadow: 0 0 22px rgba(0, 245, 212, 0.8) !important;
            transform: translateY(-1px);
        }

        /* Emergency Stop Button Special Override */
        div.stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #d90429, #ef233c) !important;
            color: #ffffff !important;
            border: 1px solid #ff4d6d !important;
            box-shadow: 0 0 15px rgba(239, 35, 60, 0.5) !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #ff4d6d, #b7094c) !important;
            color: #ffffff !important;
            box-shadow: 0 0 25px rgba(255, 77, 109, 0.8) !important;
        }

        /* Data Grid & Interactive Table Fixes */
        div[data-testid="stDataEditor"] {
            background-color: #0b132b !important;
            border: 1px solid #00b4d8 !important;
            border-radius: 10px !important;
        }

        /* Header Canvas Frame */
        .header-wrapper {
            margin-top: 5px !important;
            margin-bottom: 25px !important;
            background: #0b132b;
            border: 2px solid #00b4d8;
            box-shadow: 0 0 30px rgba(0, 180, 216, 0.4);
            border-radius: 16px;
            padding: 22px;
            text-align: center;
        }

        .main-title {
            color: #00f5d4 !important;
            font-size: 34px;
            font-weight: 900;
            margin: 0;
            text-shadow: 0 0 20px rgba(0, 245, 212, 0.7) !important;
        }

        .subtitle-badge {
            display: inline-block;
            background: #0d1b2a;
            border: 1px solid #ffb703;
            padding: 4px 20px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 800;
            color: #ffb703 !important;
            margin-top: 10px;
        }

        /* Live Analytics Metric Cards */
        .metric-card-box {
            background: #0b132b !important;
            border: 1px solid #00b4d8;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 0 15px rgba(0, 180, 216, 0.2);
        }

        .metric-label {
            font-size: 12px;
            color: #90e0ef !important;
            font-weight: 800;
            text-transform: uppercase;
        }

        .metric-value-num {
            font-size: 32px;
            font-weight: 900;
            margin-top: 6px;
            color: #ffffff !important;
        }

        /* Console Log Window */
        .log-box {
            background-color: #040812;
            border: 1px solid #00b4d8;
            border-radius: 10px;
            padding: 14px;
            max-height: 250px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 13px;
            color: #48cae4;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_styles()

# ==========================================
# 3. DATA HELPERS & AUDIT VALIDATORS
# ==========================================
def get_field_strict(row, column_aliases, default_val="N/A"):
    clean_aliases = [re.sub(r'[^a-zA-Z0-9]', '', str(a)).lower() for a in column_aliases]
    for col in row.index:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', str(col)).lower()
        if col_clean in clean_aliases:
            val = str(row[col]).strip()
            if val and val.lower() not in ["nan", "none", "n/a", "", "null"]:
                return val
    return default_val

def validate_email_address(email_str):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email_str).strip()))

def perform_batch_data_audit(dataframe):
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
# 4. DEFAULT 100 SAMPLE RECORDS GENERATOR
# ==========================================
@st.cache_data
def generate_default_100_records():
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
# 5. SIDEBAR BRANDING & CONFIGURATION STUDIO
# ==========================================
with st.sidebar:
    st.markdown("### 🖼️ Branding Studio")
    logo_file = st.file_uploader("Upload High-Res Logo", type=["png", "jpg", "jpeg"], key="logo_uploader")
    if logo_file:
        st.image(logo_file, use_container_width=True)
    
    st.divider()
    st.markdown("### 🔑 Secure SMTP Engine")
    smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587, min_value=1, max_value=65535)
    sender_email = st.text_input("Sender Email ID", placeholder="your_email@gmail.com")
    app_password = st.text_input("16-Digit App Password", type="password")
    dispatch_delay = st.slider("Dispatch Delay (Sec)", 0.2, 5.0, 0.8, step=0.1)
    
    st.divider()
    st.markdown("### 📝 Custom Email Header Settings")
    email_subject_prefix = st.text_input("Custom Email Subject Prefix", value="BUFFER CHEQUE DETAILS", key="sb_email_subject")
    custom_cfa_title = st.text_input("CFA Header Title", value="RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA", key="sb_cfa_title")
    
    st.divider()
    st.markdown("### 🛠️ Data Management Tools")
    if st.button("🔄 Reset Sample Data (100 Records)", use_container_width=True):
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
    <p style="color: #90e0ef; margin-top: 10px; font-weight: 700; font-size: 15px;">
        ⚡ ULTRA-FAST AUTOMATED DISPATCHER & DYNAMIC EMAIL ENGINE
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. BATCH EXCEL/CSV FILE UPLOADER
# ==========================================
st.markdown("### 📁 Raw Excel / CSV Import (Data Preserved)")
uploaded_file = st.file_uploader("Upload fresh Excel file to replace or update active queue", type=["xlsx", "csv"], key="batch_uploader")

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
        st.success(f"✅ Loaded {len(imported_df)} records successfully!")
    except Exception as err:
        st.error(f"❌ File import error: {err}")

df = st.session_state['crm_data']
st.session_state['validation_alerts'] = perform_batch_data_audit(df)

# ==========================================
# 8. LIVE ANALYTICS DASHBOARD
# ==========================================
total_records = len(df) if df is not None else 0
sent_count = st.session_state['sent_count']
failed_count = st.session_state['failed_count']
pending_count = max(0, total_records - (sent_count + failed_count))

st.markdown("### 📊 Live Processing Dashboard")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Total Records</div><div class="metric-value-num" style="color:#48cae4 !important;">{total_records}</div></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Sent Success</div><div class="metric-value-num" style="color:#00f5d4 !important;">{sent_count}</div></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Failed / Bounces</div><div class="metric-value-num" style="color:#ff4d6d !important;">{failed_count}</div></div>', unsafe_allow_html=True)
with col_m4:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Queue Pending</div><div class="metric-value-num" style="color:#ffb703 !important;">{pending_count}</div></div>', unsafe_allow_html=True)

with st.expander("🔍 System Data Audit & Integrity Report", expanded=False):
    for alert in st.session_state['validation_alerts']:
        st.write(alert)

st.markdown("---")

# ==========================================
# 9. INTERACTIVE LIVE DATA GRID
# ==========================================
st.markdown("### ✏️ Interactive Live Grid (100 Records Ready)")

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
# 10. DISPATCH CONTROL ACTIONS
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
# 11. HTML DYNAMIC EMAIL TEMPLATE BUILDER
# ==========================================
def build_email_template(party, date_val, acc, place, bank, u_ail, u_ahpl, h_ail, h_ahpl, cfa_title, email_title):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @keyframes fullSplashAnimation {{
            0% {{ opacity: 1; visibility: visible; }}
            80% {{ opacity: 1; visibility: visible; }}
            100% {{ opacity: 0; visibility: hidden; height: 0; padding: 0; margin: 0; }}
        }}

        .splash-overlay {{
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
        }}

        .splash-title {{
            color: #00f5d4;
            font-size: 26px;
            font-weight: 900;
            font-family: Arial, sans-serif;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(0, 245, 212, 0.9);
            margin: 0;
        }}

        .splash-sub {{
            color: #caf0f8;
            font-size: 14px;
            font-weight: bold;
            margin-top: 12px;
            letter-spacing: 1px;
            font-family: Arial, sans-serif;
        }}
    </style>
</head>
<body style="margin:0; padding:20px; background-color:#f4f6f8; font-family: 'Segoe UI', Arial, sans-serif;">

  <div class="splash-overlay">
      <div class="splash-title">RAMA ENTERPRISES</div>
      <div class="splash-sub">ABBOTT INDIA LTD, PATNA</div>
  </div>

  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; background-color: #0b132b; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
    <tr>
      <td style="padding: 24px; text-align: center;">
        <div style="background: linear-gradient(135deg, #00b4d8, #0077b6); border-radius: 12px; padding: 18px 10px; text-align: center; box-shadow: 0 0 20px rgba(0, 180, 216, 0.6);">
          <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 900; letter-spacing: 1px;">
            {str(email_title).upper()}
          </h1>
        </div>
        <div style="margin-top: 12px; font-weight: bold; color: #90e0ef; font-size: 13px;">
          ✨ {cfa_title}
        </div>
      </td>
    </tr>
    <tr>
      <td style="padding: 0 28px 28px 28px;">
        <p style="color: #ffffff; font-size: 16px; margin-bottom: 8px;">Dear <b style="color: #00f5d4;">{party}</b>,</p>
        <p style="color: #caf0f8; font-size: 14px; margin-top: 0; margin-bottom: 22px;">Please find below the updated summary of your cheque records:</p>
        <table border="0" cellpadding="12" cellspacing="0" width="100%" style="border-collapse: collapse; background-color: #1c2541; border-radius: 10px; overflow: hidden;">
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td width="50%" style="color: #90e0ef; font-weight: bold; font-size: 14px;">📅 Date</td>
            <td width="50%" style="color: #00f5d4; font-weight: bold; font-size: 14px;">{date_val}</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">👤 Party Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{party}</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🔢 Account Number</td>
            <td style="color: #48cae4; font-weight: bold; font-size: 14px;">{acc}</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">📍 Place</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{place}</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🏦 Bank Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{bank}</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AIL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{u_ail}</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AHPL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{u_ahpl}</td>
          </tr>
          <tr style="border-bottom: 1px solid #3a5a40;">
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AIL</td>
            <td style="color: #00f5d4; font-weight: bold; font-size: 14px;">{h_ail}</td>
          </tr>
          <tr>
            <td style="color: #90e0ef; font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AHPL</td>
            <td style="color: #00f5d4; font-weight: bold; font-size: 14px;">{h_ahpl}</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td style="background-color: #1c2541; padding: 20px; text-align: center; border-top: 1px solid #3a5a40;">
        <div style="color: #00f5d4; font-weight: 800; font-size: 14px;">{cfa_title}</div>
      </td>
    </tr>
  </table>
</body>
</html>"""

# ==========================================
# 12. INTERACTIVE EMAIL INBOX SIMULATOR
# ==========================================
st.markdown("### 👁️ Live Rendered Inbox View")
sim_col1, sim_col2 = st.columns([1, 1], gap="large")

with sim_col1:
    st.markdown("#### Test Data Controls")
    sim_party = st.text_input("Simulated Party Name", value="RAJVEER", key="sim_party")
    sim_acc = st.text_input("Simulated Account Number", value="351800949903", key="sim_acc")
    sim_place = st.text_input("Simulated Place", value="Patna", key="sim_place")
    sim_bank = st.text_input("Simulated Bank Name", value="State Bank of India", key="sim_bank")
    sim_u_ail = st.text_input("Used AIL Cheques", value="4", key="sim_u_ail")
    sim_u_ahpl = st.text_input("Used AHPL Cheques", value="2", key="sim_u_ahpl")
    sim_h_ail = st.text_input("Hand AIL Cheques", value="15", key="sim_h_ail")
    sim_h_ahpl = st.text_input("Hand AHPL Cheques", value="18", key="sim_h_ahpl")

with sim_col2:
    st.markdown("#### 📱 Live Email Preview")
    preview_html = build_email_template(
        sim_party, datetime.now().strftime("%Y-%m-%d"), sim_acc, sim_place, sim_bank,
        sim_u_ail, sim_u_ahpl, sim_h_ail, sim_h_ahpl, custom_cfa_title, email_subject_prefix
    )
    st.components.v1.html(preview_html, height=500, scrolling=True)

# ==========================================
# 13. REAL-TIME BULK EMAIL DISPATCH ENGINE
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
        st.markdown("### 📡 Live Dispatch Console Stream")
        
        progress_bar = st.progress(0)
        status_box = st.empty()
        log_container = st.empty()

        try:
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

                progress = (idx + 1) / len(df)
                progress_bar.progress(progress)
                
                log_html = "<div class='log-box'>" + "<br>".join(st.session_state['dispatch_logs']) + "</div>"
                log_container.markdown(log_html, unsafe_allow_html=True)
                
                time.sleep(dispatch_delay)

            server.quit()
            st.balloons()
            st.success("🎉 Cheque Record Dispatch Completed Successfully!")

        except Exception as conn_err:
            st.error(f"❌ Connection Failure: {conn_err}")
            st.session_state['dispatch_logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] FATAL: {conn_err}")

if st.session_state['dispatch_logs']:
    st.markdown("### 📜 Dispatch Logs Console")
    st.markdown("<div class='log-box'>" + "<br>".join(st.session_state['dispatch_logs']) + "</div>", unsafe_allow_html=True)
