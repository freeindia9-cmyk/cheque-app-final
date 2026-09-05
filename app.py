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

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="DHARMENDRA KUMAR (MISHRA) - 8K Dynamic Cheque Dispatcher",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 8K Ultra-Dynamic Cyberpunk Glassmorphic UI CSS
# ==========================================
st.markdown("""
<style>
    /* 8K Animated Dynamic Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #064e3b, #022c22, #0f172a, #042f2e, #065f46);
        background-size: 400% 400%;
        animation: gradient8K 12s ease infinite;
        color: #ecfdf5;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    @keyframes gradient8K {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating Hologram Header Box */
    .header-box {
        background: rgba(6, 78, 59, 0.45);
        border: 2px solid rgba(52, 211, 153, 0.7);
        box-shadow: 0 0 40px rgba(52, 211, 153, 0.4), inset 0 0 20px rgba(6, 182, 212, 0.3);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 26px;
        text-align: center;
        margin-bottom: 25px;
        animation: pulseHeader 3s infinite alternate;
    }

    @keyframes pulseHeader {
        0% { box-shadow: 0 0 25px rgba(52, 211, 153, 0.3); }
        100% { box-shadow: 0 0 50px rgba(6, 182, 212, 0.8); }
    }

    .floating-header {
        background: linear-gradient(90deg, #34d399, #10b981, #06b6d4, #a7f3d0, #34d399);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 44px;
        font-weight: 900;
        letter-spacing: -0.5px;
        animation: shine 5s linear infinite;
        margin: 0;
        filter: drop-shadow(0 0 20px rgba(52, 211, 153, 0.6));
    }

    @keyframes shine {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }

    .designer-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.3), rgba(6, 182, 212, 0.4));
        border: 1px solid rgba(52, 211, 153, 0.8);
        padding: 8px 22px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 1.5px;
        color: #34d399;
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.5);
        margin-top: 8px;
    }

    /* 8K Glass Cards with Interactive Hover Zoom */
    .metric-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(52, 211, 153, 0.4);
        border-radius: 20px;
        padding: 22px;
        text-align: center;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        transition: all 0.4s ease-in-out;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.04);
        border-color: #06b6d4;
        box-shadow: 0 0 35px rgba(6, 182, 212, 0.6);
    }

    .metric-title {
        font-size: 13px;
        color: #a7f3d0;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .metric-value {
        font-size: 38px;
        font-weight: 900;
        margin-top: 6px;
        background: linear-gradient(90deg, #34d399, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glowing Launch Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #059669, #06b6d4) !important;
        background-size: 200% 200% !important;
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        border: 1px solid #34d399 !important;
        border-radius: 16px !important;
        padding: 18px 30px !important;
        box-shadow: 0 0 35px rgba(16, 185, 129, 0.8) !important;
        transition: all 0.4s ease !important;
        animation: buttonGlow 3s infinite !important;
    }

    @keyframes buttonGlow {
        0% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
        50% { box-shadow: 0 0 50px rgba(6, 182, 212, 1); }
        100% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-4px) scale(1.03) !important;
    }

    /* Emergency Stop Button */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ef4444, #dc2626, #991b1b) !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border-radius: 16px !important;
        padding: 18px 24px !important;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Flexible Strict Field Matching Engine
# ==========================================
def get_field_strict(row, column_aliases, default_val="N/A"):
    clean_aliases = [re.sub(r'[^a-zA-Z0-9]', '', str(a)).lower() for a in column_aliases]
    # Exact Match First
    for col in row.index:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', str(col)).lower()
        if col_clean in clean_aliases:
            val = str(row[col]).strip()
            if val and val.lower() not in ["nan", "none", "n/a", "", "null"]:
                return val
    # Substring Match Fallback
    for col in row.index:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', str(col)).lower()
        for alias in clean_aliases:
            if alias in col_clean or col_clean in alias:
                val = str(row[col]).strip()
                if val and val.lower() not in ["nan", "none", "n/a", "", "null"]:
                    return val
    return default_val

# ==========================================
# 4. Default 100 Records Generator
# ==========================================
@st.cache_data
def load_default_100_records():
    parties = ["Aarav Sharma", "Priya Patel", "Rahul Verma", "Ananya Iyer", "Amit Gupta"]
    places = ["Patna", "Delhi", "Mumbai", "Kolkata", "Bangalore"]
    banks = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank"]
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

# Session State Initialization
if 'crm_data' not in st.session_state:
    st.session_state['crm_data'] = load_default_100_records()
if 'sent_count' not in st.session_state:
    st.session_state['sent_count'] = 0
if 'failed_count' not in st.session_state:
    st.session_state['failed_count'] = 0
if 'stop_dispatch' not in st.session_state:
    st.session_state['stop_dispatch'] = False

# ==========================================
# 5. Sidebar Controls & Credentials
# ==========================================
with st.sidebar:
    st.markdown("### 🖼️ Branding Studio")
    logo_file = st.file_uploader("Upload High-Res Logo", type=["png", "jpg", "jpeg"])
    st.divider()
    st.markdown("### 🔑 Secure SMTP Engine")
    smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587)
    sender_email = st.text_input("Sender Email ID", placeholder="your_email@gmail.com")
    app_password = st.text_input("16-Digit App Password", type="password")
    dispatch_delay = st.slider("Dispatch Rate Delay (Seconds)", 0.5, 5.0, 1.0)

# ==========================================
# 6. Floating Dynamic Header Box
# ==========================================
st.markdown("""
<div class="header-box">
    <h1 class="floating-header">DHARMENDRA KUMAR (MISHRA)</h1>
    <span class="designer-badge">✨ ARCHITECT & DESIGNER: RAJVEER</span>
    <p style="color: #a7f3d0; margin-top: 10px; font-weight: 700; font-size: 16px;">
        ⚡ 8K ULTRA-DYNAMIC CHEQUE DISPATCHER & AUTOMATED EMAIL MANAGEMENT ENGINE
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. File Import & Progress Dashboard
# ==========================================
uploaded_file = st.file_uploader("Upload fresh Excel/CSV file", type=["xlsx", "csv"])
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

st.markdown("### 📊 Live Dispatch Progress Dashboard")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-title">Total Records</div><div class="metric-value">{total_records}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-title">Sent Success</div><div class="metric-value" style="color:#34d399;">{st.session_state["sent_count"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-title">Failed</div><div class="metric-value" style="color:#f87171;">{st.session_state["failed_count"]}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div class="metric-title">Pending</div><div class="metric-value" style="color:#fbbf24;">{max(0, pending_records)}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 8. Interactive Data Grid (Editable / Removable)
# ==========================================
st.markdown(f"### ✏️ Interactive Cheque Details Grid ({len(df)} Records Ready)")
edited_df = st.data_editor(st.session_state['crm_data'], num_rows="dynamic", use_container_width=True, height=380)
st.session_state['crm_data'] = edited_df
df = st.session_state['crm_data']

# Dispatch Buttons
col_start, col_stop = st.columns([2, 1])
with col_start: start_btn = st.button("🚀 LAUNCH CHEQUE DETAILS DISPATCH", type="primary", use_container_width=True)
with col_stop: stop_btn = st.button("🛑 EMERGENCY STOP", type="secondary", use_container_width=True)

if stop_btn:
    st.session_state['stop_dispatch'] = True
    st.warning("🛑 Emergency Stop Triggered! Process halting...")

# ==========================================
# 9. Automated Email Dispatch Engine
# ==========================================
if start_btn:
    st.session_state['stop_dispatch'] = False
    st.session_state['sent_count'] = 0
    st.session_state['failed_count'] = 0

    if not sender_email or not app_password:
        st.warning("⚠️ Sidebar mein Sender Email ID aur App Password fill karein!")
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
                    st.error("🛑 Dispatch process stopped manually!")
                    break

                row = df.iloc[idx]
                rec_date = get_field_strict(row, ["Date", "Entry Date", "Cheque Date"], "N/A")
                party_name = get_field_strict(row, ["Party Name", "Party", "Customer Name", "Name"], "Valued Party")
                account_val = get_field_strict(row, ["Account Number", "Account No", "Account", "A/C No"], "N/A")
                target_email = get_field_strict(row, ["Email", "Email ID", "Mail", "Email Address"], "").strip()
                place_val = get_field_strict(row, ["Place", "City", "Location"], "N/A")
                bank_val = get_field_strict(row, ["Bank Name", "Bank"], "N/A")
                
                used_ail = get_field_strict(row, ["Number of cheque used in AIL", "Used AIL"], "0")
                used_ahpl = get_field_strict(row, ["Number of cheque used In AHPL", "Used AHPL"], "0")
                hand_ail = get_field_strict(row, ["Total cheque in hand AIL", "Hand AIL"], "0")
                hand_ahpl = get_field_strict(row, ["Total cheque in hand AHPL", "Hand AHPL"], "0")

                if "@" in target_email:
                    msg = MIMEMultipart('alternative')
                    custom_sender_name = "RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA"
                    msg['From'] = formataddr((custom_sender_name, sender_email.strip()))
                    msg['To'] = target_email
                    msg['Subject'] = f"💳 Buffer Cheque Details - {party_name} ({rec_date})"

                    # 🎨 Selection-Grade HTML Email Body with 3-Second Fade-Out Dynamic Banner
                    body_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            @keyframes fadeOutBanner {{
                                0% {{ opacity: 1; max-height: 60px; padding: 12px; margin-top: 10px; }}
                                70% {{ opacity: 1; max-height: 60px; padding: 12px; margin-top: 10px; }}
                                100% {{ opacity: 0; max-height: 0px; padding: 0px; margin-top: 0px; overflow: hidden; display: none; }}
                            }}
                            .animated-subbanner {{
                                background: linear-gradient(90deg, #10b981, #06b6d4, #34d399);
                                color: #022c22;
                                font-weight: 900;
                                font-size: 14px;
                                border-radius: 8px;
                                text-align: center;
                                letter-spacing: 1.2px;
                                text-transform: uppercase;
                                box-shadow: 0 0 15px rgba(52, 211, 153, 0.8);
                                animation: fadeOutBanner 3.5s forwards ease-in-out;
                            }}
                        </style>
                    </head>
                    <body style="margin:0; padding:20px; background-color:#f4f6f8; font-family: 'Segoe UI', Arial, sans-serif;">
                      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; background-color: #064e3b; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                        
                        <!-- HEADER SECTION -->
                        <tr>
                          <td style="padding: 24px; text-align: center;">
                            <div style="background-color: #34d399; border-radius: 12px; padding: 18px 10px; text-align: center; box-shadow: 0 0 20px rgba(52, 211, 153, 0.6);">
                              <h1 style="margin: 0; color: #022c22; font-size: 26px; font-weight: 900; letter-spacing: 1px; font-family: sans-serif;">
                                BUFFER CHEQUE DETAILS
                              </h1>
                            </div>

                            <!-- 3-SECOND FADE OUT GLOWING BANNER -->
                            <div class="animated-subbanner">
                              ✨ RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA
                            </div>
                          </td>
                        </tr>

                        <!-- CHEQUE DATA CONTENT -->
                        <tr>
                          <td style="padding: 0 28px 28px 28px;">
                            <p style="color: #ffffff; font-size: 16px; margin-bottom: 8px;">Dear <b style="color: #34d399;">{party_name}</b>,</p>
                            <p style="color: #a7f3d0; font-size: 14px; margin-top: 0; margin-bottom: 22px;">Please find below the updated summary of your cheque records:</p>
                            
                            <!-- DETAILS TABLE -->
                            <table border="0" cellpadding="12" cellspacing="0" width="100%" style="border-collapse: collapse; background-color: #022c22; border-radius: 10px; overflow: hidden;">
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td width="50%" style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📅 Date</td>
                                <td width="50%" style="color: #34d399; font-weight: bold; font-size: 14px;">{rec_date}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">👤 Party Name</td>
                                <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{party_name}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🔢 Account Number</td>
                                <td style="color: #38bdf8; font-weight: bold; font-size: 14px;">{account_val}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📍 Place</td>
                                <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{place_val}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🏦 Bank Name</td>
                                <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{bank_val}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AIL</td>
                                <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{used_ail}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AHPL</td>
                                <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{used_ahpl}<
