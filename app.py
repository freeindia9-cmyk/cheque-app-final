import streamlit as st
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime, timedelta
import random
import re
import io

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="8K Cyberpunk Cheque Dispatcher Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. Dynamic Cyberpunk & Smooth Neon CSS Setup
# ==========================================
st.markdown("""
<style>
    /* Global App Background */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at 50% 20%, #0d1b2a, #0b132b, #040814) !important;
        color: #e0e1dd !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Sidebar Dark Modern Theme */
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

    /* Replacing Pure Green Text with Cyan/Blue/Gold Neon Glow */
    h1, h2, h3, h4, h5, h6 {
        color: #48cae4 !important;
        text-shadow: 0 0 12px rgba(72, 202, 228, 0.6) !important;
        font-weight: 800 !important;
    }

    p, span, label {
        color: #e0e1dd !important;
    }

    /* Input Fields & Dropdowns Glow */
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

    /* Data Grid Container Styling */
    div[data-testid="stDataFrame"] {
        background-color: #0d1b2a !important;
        border: 2px solid #00b4d8 !important;
        border-radius: 16px !important;
        padding: 10px !important;
        box-shadow: 0 0 30px rgba(0, 180, 216, 0.3) !important;
    }

    div[data-testid="stDataFrame"] * {
        background-color: #0d1b2a !important;
        color: #ffffff !important;
    }

    /* Import File Box & Inner Button Neon Effect */
    [data-testid="stFileUploadDropzone"] {
        background: linear-gradient(135deg, #101d30, #0c1827) !important;
        border: 2px dashed #00b4d8 !important;
        border-radius: 16px !important;
        box-shadow: 0 0 20px rgba(0, 180, 216, 0.3) !important;
        transition: all 0.5s ease-in-out !important;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #00f5d4 !important;
        box-shadow: 0 0 35px rgba(0, 245, 212, 0.6) !important;
    }

    [data-testid="stFileUploadDropzone"] button {
        background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
        color: #ffffff !important;
        border: 2px solid #90e0ef !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        box-shadow: 0 0 15px rgba(0, 180, 216, 0.6) !important;
        transition: all 0.5s ease-in-out !important;
    }

    [data-testid="stFileUploadDropzone"] button:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 0 30px rgba(144, 224, 239, 0.9) !important;
    }

    /* Top Floating Header Box */
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
        font-size: 40px;
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

    /* Metric Cards System */
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
        font-size: 38px;
        font-weight: 900;
        margin-top: 8px;
        color: #ffffff !important;
        text-shadow: 0 0 18px rgba(255, 255, 255, 0.8) !important;
    }

    /* Slow & Attractive Glowing Action Buttons */
    div.stButton > button, div.stDownloadButton > button {
        font-weight: 900 !important;
        border-radius: 14px !important;
        padding: 16px 24px !important;
        font-size: 16px !important;
        letter-spacing: 1px !important;
        transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1) !important; /* Slow and silky animation */
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.8) !important;
    }

    /* Launch Dispatch Button (Emerald Cyan Glowing) */
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

    /* Emergency Stop Button (Neon Red/Pink Glowing) */
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

    /* Export CSV Button (Neon Royal Blue Glowing) */
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Helper Column Alias Extractor
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

# ==========================================
# 4. Default Records Generator
# ==========================================
@st.cache_data
def load_default_100_records():
    parties = ["Aarav Sharma", "Priya Patel", "Rahul Verma", "Ananya Iyer", "Amit Gupta", "Vikram Singh"]
    places = ["Patna", "Delhi", "Mumbai", "Kolkata", "Bangalore", "Ranchi"]
    banks = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank"]
    records = []
    base_date = datetime(2026, 8, 1)
    for i in range(1, 101):
        party_name = parties[(i - 1) % len(parties)]
        email_prefix = party_name.split()[0].lower() + str(i)
        entry_dt = base_date + timedelta(days=(i % 25))
        account_no = f"35{random.randint(1000000000, 9999999999)}"
        records.append({
            "Date": entry_dt.strftime("%Y-%m-%d"),
            "Party Name": party_name,
            "Account Number": account_no,
            "Email": f"{email_prefix}@clientdomain.com",
            "Place": random.choice(places),
            "Bank Name": random.choice(banks),
            "Number of cheque used in AIL": random.randint(1, 10),
            "Number of cheque used In AHPL": random.randint(1, 10),
            "Total cheque in hand AIL": random.randint(5, 20),
            "Total cheque in hand AHPL": random.randint(5, 20)
        })
    return pd.DataFrame(records)

if 'crm_data' not in st.session_state:
    st.session_state['crm_data'] = load_default_100_records()
if 'sent_count' not in st.session_state:
    st.session_state['sent_count'] = 0
if 'failed_count' not in st.session_state:
    st.session_state['failed_count'] = 0
if 'stop_dispatch' not in st.session_state:
    st.session_state['stop_dispatch'] = False

# ==========================================
# 5. Sidebar Controls
# ==========================================
with st.sidebar:
    st.markdown("### 🖼️ Branding Studio")
    logo_file = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])
    if logo_file:
        st.image(logo_file, use_container_width=True)
    
    st.divider()
    st.markdown("### 🔑 Secure SMTP Credentials")
    smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587)
    sender_email = st.text_input("Sender Email ID", placeholder="your_email@gmail.com")
    app_password = st.text_input("16-Digit App Password", type="password")
    dispatch_delay = st.slider("Dispatch Rate Delay (Sec)", 0.5, 5.0, 1.0)
    
    st.divider()
    st.markdown("### 📝 Email Template Customizer")
    email_subject_prefix = st.text_input("Custom Email Subject Prefix", value="💳 Buffer Cheque Details")
    custom_cfa_title = st.text_input("CFA Header Title", value="RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA")

# ==========================================
# 6. Main Top Header
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

# File Import Section with Smooth Cyber Effects
st.markdown("### 📁 Import Batch Data File")
uploaded_file = st.file_uploader("Upload Fresh Excel/CSV File", type=["xlsx", "csv"])
if uploaded_file is not None:
    try:
        new_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file, engine='openpyxl')
        new_df.columns = [str(c).strip() for c in new_df.columns]
        st.session_state['crm_data'] = new_df
        st.session_state['sent_count'] = 0
        st.session_state['failed_count'] = 0
        st.success(f"✅ Loaded {len(new_df)} records successfully!")
    except Exception as e:
        st.error(f"❌ File loading failed: {e}")

df = st.session_state['crm_data']
total_records = len(df)
pending_records = total_records - (st.session_state['sent_count'] + st.session_state['failed_count'])

# ==========================================
# 7. Live Metrics Panel
# ==========================================
st.markdown("### 📊 Live Dispatch Progress Analytics")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Total Records</div><div class="metric-value-num" style="color:#48cae4 !important;">{total_records}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Sent Success</div><div class="metric-value-num" style="color:#00f5d4 !important;">{st.session_state["sent_count"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Failed</div><div class="metric-value-num" style="color:#ff4d6d !important;">{st.session_state["failed_count"]}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Pending</div><div class="metric-value-num" style="color:#ffb703 !important;">{max(0, pending_records)}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 8. Interactive Data Grid with Multi-Column Layout
# ==========================================
st.markdown(f"### ✏️ Interactive Cheque Details Grid ({len(df)} Records)")
edited_df = st.data_editor(st.session_state['crm_data'], num_rows="dynamic", use_container_width=True, height=360)
st.session_state['crm_data'] = edited_df
df = st.session_state['crm_data']

st.markdown("<br>", unsafe_allow_html=True)

# Dispatch Control Action Buttons
st.markdown("### 🚀 Dispatch Control Actions")
c_start, c_stop, c_export = st.columns([1.8, 1.1, 1.1])
with c_start: start_btn = st.button("🚀 LAUNCH CHEQUE DETAILS DISPATCH", type="primary", use_container_width=True)
with c_stop: stop_btn = st.button("🛑 EMERGENCY STOP", type="secondary", use_container_width=True)
with c_export:
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button("📥 EXPORT CLEAN CSV", data=csv_buffer.getvalue(), file_name="Cheque_Details_Report.csv", mime="text/csv", use_container_width=True)

if stop_btn:
    st.session_state['stop_dispatch'] = True
    st.warning("🛑 Emergency Stop Triggered!")

st.markdown("---")

# ==========================================
# 9. HTML Email Template with Splash Screen
# ==========================================
def build_email_template(party, date_val, acc, place, bank, u_ail, u_ahpl, h_ail, h_ahpl, cfa_title):
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
            BUFFER CHEQUE DETAILS
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
# 10. Live Interactive Inbox Simulator
# ==========================================
st.markdown("### 👁️ Interactive Email Inbox Simulator")
col_test_input, col_test_render = st.columns([1, 1], gap="large")

with col_test_input:
    st.markdown("#### 🧪 Test Data Controls")
    sim_party = st.text_input("Simulated Party Name", value="RAJVEER")
    sim_acc = st.text_input("Simulated Account Number", value="351800949903")
    sim_place = st.text_input("Simulated Place", value="Patna")
    sim_bank = st.text_input("Simulated Bank Name", value="State Bank of India")

with col_test_render:
    st.markdown("#### 📱 Live Rendered Inbox View")
    rendered_html = build_email_template(
        sim_party, "2026-08-05", sim_acc, sim_place, sim_bank,
        "4", "2", "15", "18", custom_cfa_title
    )
    st.components.v1.html(rendered_html, height=480, scrolling=True)

# ==========================================
# 11. Automated Dispatch Engine
# ==========================================
if start_btn:
    st.session_state['stop_dispatch'] = False
    st.session_state['sent_count'] = 0
    st.session_state['failed_count'] = 0

    if not sender_email or not app_password:
        st.warning("⚠️ Please provide Sender Email ID and App Password in Sidebar!")
    else:
        st.markdown("---")
        progress_bar = st.progress(0)
        status_box = st.empty()

        try:
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()
            server.login(sender_email.strip(), app_password.replace(" ", ""))

            for idx in range(len(df)):
                if st.session_state['stop_dispatch']:
                    st.error("🛑 Process stopped manually!")
                    break

                row = df.iloc[idx]
                rec_date = get_field_strict(row, ["Date", "Entry Date"], "N/A")
                party_name = get_field_strict(row, ["Party Name", "Party"], "Valued Customer")
                account_val = get_field_strict(row, ["Account Number", "Account No"], "N/A")
                target_email = get_field_strict(row, ["Email", "Email ID"], "").strip()
                place_val = get_field_strict(row, ["Place", "City"], "N/A")
                bank_val = get_field_strict(row, ["Bank Name", "Bank"], "N/A")
                
                used_ail = get_field_strict(row, ["Number of cheque used in AIL"], "0")
                used_ahpl = get_field_strict(row, ["Number of cheque used In AHPL"], "0")
                hand_ail = get_field_strict(row, ["Total cheque in hand AIL"], "0")
                hand_ahpl = get_field_strict(row, ["Total cheque in hand AHPL"], "0")

                if "@" in target_email:
                    msg = MIMEMultipart('alternative')
                    msg['From'] = formataddr((custom_cfa_title, sender_email.strip()))
                    msg['To'] = target_email
                    msg['Subject'] = f"{email_subject_prefix} - {party_name} ({rec_date})"

                    full_body = build_email_template(
                        party_name, rec_date, account_val, place_val, bank_val,
                        used_ail, used_ahpl, hand_ail, hand_ahpl, custom_cfa_title
                    )
                    msg.attach(MIMEText(full_body, 'html'))
                    
                    try:
                        server.sendmail(sender_email.strip(), target_email, msg.as_string())
                        st.session_state['sent_count'] += 1
                        status_box.info(f"🔵 [{idx+1}/{len(df)}] Sent to **{party_name}** ({target_email})")
                    except Exception as send_err:
                        st.session_state['failed_count'] += 1
                        status_box.error(f"🔴 [{idx+1}/{len(df)}] Failed: {target_email}")
                else:
                    st.session_state['failed_count'] += 1
                    status_box.warning(f"⚠️ [{idx+1}/{len(df)}] Skipped invalid email for: **{party_name}**")

                progress = (idx + 1) / len(df)
                progress_bar.progress(progress)
                time.sleep(dispatch_delay)

            server.quit()
            st.balloons()
            st.success("🎉 Cheque Record Dispatch Completed Successfully!")

        except Exception as conn_err:
            st.error(f"❌ Connection Failure: {conn_err}")
