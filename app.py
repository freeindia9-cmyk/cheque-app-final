import streamlit as st
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import random
import re

# 1. Page Configuration
st.set_page_config(
    page_title="DHARMENDRA KUMAR (MISHRA) - Cheque Detail Dispatcher",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fresh Cyberpunk Neon Emerald Dynamic CSS Theme
st.markdown("""
<style>
    /* Animated Gradient Background - Cyberpunk Emerald */
    .stApp {
        background: linear-gradient(-45deg, #022c22, #064e3b, #0f172a, #065f46, #022c22);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
        color: #ecfdf5;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .header-container {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .floating-header {
        background: linear-gradient(90deg, #34d399, #10b981, #06b6d4, #a7f3d0);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 900;
        letter-spacing: -1px;
        animation: gradientShift 6s ease infinite, floatTitle 3s ease-in-out infinite;
        margin: 0;
        display: inline-block;
    }

    .designer-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(6, 182, 212, 0.25));
        border: 1px solid rgba(52, 211, 153, 0.4);
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #34d399;
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.2);
        width: fit-content;
        margin-top: 4px;
        animation: pulseBadge 3s infinite alternate;
    }

    @keyframes pulseBadge {
        0% { border-color: rgba(52, 211, 153, 0.3); box-shadow: 0 0 10px rgba(52, 211, 153, 0.1); }
        100% { border-color: rgba(6, 182, 212, 0.7); box-shadow: 0 0 25px rgba(6, 182, 212, 0.4); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes floatTitle {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }

    .logo-frame {
        display: inline-block;
        padding: 8px;
        border-radius: 24px;
        background: linear-gradient(135deg, #34d399, #06b6d4, #10b981);
        animation: pulse4K 2.5s infinite alternate;
        box-shadow: 0 0 25px rgba(52, 211, 153, 0.6);
    }

    @keyframes pulse4K {
        0% { transform: scale(0.97); box-shadow: 0 0 15px rgba(52, 211, 153, 0.4); }
        100% { transform: scale(1.03); box-shadow: 0 0 35px rgba(6, 182, 212, 0.9); }
    }

    .metric-card {
        background: rgba(6, 78, 59, 0.45);
        border: 1px solid rgba(52, 211, 153, 0.25);
        border-radius: 20px;
        padding: 22px;
        text-align: center;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #34d399;
        box-shadow: 0 15px 45px rgba(52, 211, 153, 0.35);
    }

    .metric-title {
        font-size: 14px;
        color: #a7f3d0;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 900;
        margin-top: 8px;
        background: linear-gradient(90deg, #34d399, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Dynamic Emerald Glow Buttons */
    div.stButton > button[kind="primary"], div.stButton > button:first-child:not([kind="secondary"]) {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #06b6d4 100%) !important;
        background-size: 200% 200% !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 28px !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.5), 0 0 10px rgba(6, 182, 212, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        cursor: pointer !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        animation: glowShift 4s ease infinite !important;
    }

    @keyframes glowShift {
        0% { background-position: 0% 50%; box-shadow: 0 0 25px rgba(16, 185, 129, 0.5); }
        50% { background-position: 100% 50%; box-shadow: 0 0 35px rgba(6, 182, 212, 0.8); }
        100% { background-position: 0% 50%; box-shadow: 0 0 25px rgba(16, 185, 129, 0.5); }
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 10px 40px rgba(6, 182, 212, 0.9), 0 0 20px rgba(52, 211, 153, 0.8) !important;
        color: #ffffff !important;
    }

    div.stButton > button[kind="primary"]:active {
        transform: translateY(1px) scale(0.97) !important;
    }

    div.stButton > button:nth-child(2), div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        border: 1px solid rgba(239, 68, 68, 0.6) !important;
        border-radius: 14px !important;
        padding: 16px 24px !important;
        box-shadow: 0 0 18px rgba(239, 68, 68, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    div.stButton > button:nth-child(2):hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.8) !important;
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
    }

    [data-testid="stFileUploader"] section {
        background: rgba(6, 78, 59, 0.4) !important;
        border: 2px dashed #34d399 !important;
        border-radius: 18px !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"] section:hover {
        border-color: #06b6d4 !important;
        background: rgba(15, 23, 42, 0.8) !important;
        box-shadow: 0 0 25px rgba(52, 211, 153, 0.3) !important;
    }

    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #34d399, #059669) !important;
        color: #022c22 !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.5) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Flexible Field Matching Engine
def get_field_strict(row, column_aliases, default_val="N/A"):
    clean_aliases = [re.sub(r'[^a-zA-Z0-9]', '', str(a)).lower() for a in column_aliases]
    
    for col in row.index:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', str(col)).lower()
        if col_clean in clean_aliases:
            val = str(row[col]).strip()
            if val and val.lower() not in ["nan", "none", "n/a", "", "null"]:
                return val
                
    for col in row.index:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', str(col)).lower()
        for alias in clean_aliases:
            if alias in col_clean or col_clean in alias:
                val = str(row[col]).strip()
                if val and val.lower() not in ["nan", "none", "n/a", "", "null"]:
                    return val
                    
    return default_val

# 4. Default Records Generator for Cheque Details
@st.cache_data
def load_default_100_records():
    parties = [
        "Aarav Sharma", "Priya Patel", "Rahul Verma", "Ananya Iyer", "Amit Gupta",
        "Rohan Mehta", "Sneha Reddy", "Vikram Singh", "Pooja Joshi", "Karan Kapoor"
    ]
    places = ["Patna", "Delhi", "Mumbai", "Kolkata", "Bangalore", "Ranchi", "Varanasi"]
    banks = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Canara Bank"]
    records = []
    base_date = datetime(2026, 8, 1)

    for i in range(1, 101):
        party_name = parties[(i - 1) % len(parties)]
        email_prefix = party_name.split()[0].lower() + str(i)
        entry_dt = base_date + timedelta(days=(i % 25))
        used = random.randint(1, 15)
        unused = random.randint(2, 25)
        total = used + unused

        records.append({
            "Date": entry_dt.strftime("%Y-%m-%d"),
            "Party Name": party_name,
            "Email": f"{email_prefix}@clientdomain.com",
            "Place": random.choice(places),
            "Bank Name": random.choice(banks),
            "Number of Cheque Used": used,
            "Unused Cheque": unused,
            "Total Cheque": total
        })
    return pd.DataFrame(records)

# Session State Initialization
if 'crm_data' not in st.session_state:
    st.session_state['crm_data'] = load_default_100_records()
if 'sent_count' not in st.session_state:
    st.session_state['sent_count'] = 0
if 'failed_count' not in st.session_state:
    st.session_state['failed_count'] = 0

# 5. Sidebar Controls
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

# 6. Dynamic Header Section
col_logo, col_title = st.columns([1, 5])

with col_logo:
    if logo_file is not None:
        st.markdown('<div class="logo-frame">', unsafe_allow_html=True)
        st.image(logo_file, width=110)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="logo-frame" style="font-size: 55px; padding: 12px 24px;">💳</div>', unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div class="header-container">
        <h1 class="floating-header">DHARMENDRA KUMAR (MISHRA)</h1>
        <div>
            <span class="designer-badge">✨ ARCHITECT & DESIGNER: DHARMENDRA KUMAR (MISHRA)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("🚀 Automated Cheque Record Dispatcher & Email Management Engine")

st.divider()

# 7. Excel/CSV Import
st.markdown("### 📂 Import Cheque Details (Excel / CSV)")
uploaded_file = st.file_uploader(
    "Upload fresh Excel file to replace or update cheque records", 
    type=["xlsx", "csv"],
    help="Supported formats: .xlsx, .csv"
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            new_df = pd.read_csv(uploaded_file)
        else:
            new_df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        new_df.columns = [str(c).strip() for c in new_df.columns]
        st.session_state['crm_data'] = new_df
        st.session_state['sent_count'] = 0
        st.session_state['failed_count'] = 0
        st.success(f"✅ Successfully loaded {len(new_df)} cheque records!")
    except Exception as e:
        st.error(f"❌ File loading failed: {e}")

# 8. Live Dashboard Counters
df = st.session_state['crm_data']
total_records = len(df)
pending_records = total_records - (st.session_state['sent_count'] + st.session_state['failed_count'])

st.markdown("### 📊 Live Dispatch Progress Dashboard")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Total Cheque Records</div><div class="metric-value">{total_records}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Sent Success</div><div class="metric-value" style="color:#34d399;">{st.session_state["sent_count"]}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Failed / Bounces</div><div class="metric-value" style="color:#f87171;">{st.session_state["failed_count"]}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Queue Pending</div><div class="metric-value" style="color:#fbbf24;">{max(0, pending_records)}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# 9. Interactive Live Grid
st.markdown(f"### ✏️ Interactive Cheque Details Grid ({len(df)} Records Ready)")
st.caption("💡 Tip: Double click any cell to edit details directly.")

edited_df = st.data_editor(
    st.session_state['crm_data'],
    num_rows="dynamic",
    use_container_width=True,
    height=420,
    key="cheque_grid_editor"
)

st.session_state['crm_data'] = edited_df
df = st.session_state['crm_data']

# 10. Smart Bulk Dispatch Engine
if 'stop_dispatch' not in st.session_state:
    st.session_state['stop_dispatch'] = False

col_start, col_stop = st.columns([2, 1])

with col_start:
    start_btn = st.button("🚀 Launch Cheque Details Dispatch", type="primary", use_container_width=True)

with col_stop:
    stop_btn = st.button("🛑 Emergency Stop", use_container_width=True)

if stop_btn:
    st.session_state['stop_dispatch'] = True

if start_btn:
    st.session_state['stop_dispatch'] = False
    st.session_state['sent_count'] = 0
    st.session_state['failed_count'] = 0

    if not sender_email or not app_password:
        st.warning("⚠️ Kripya sidebar me Sender Email ID aur 16-digit App Password enter karein!")
    else:
        st.markdown("---")
        st.markdown("### 📡 Real-time Dispatch Monitor")
        progress_bar = st.progress(0)
        status_box = st.empty()

        try:
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()
            server.login(sender_email.strip(), app_password.replace(" ", ""))

            for idx in range(len(df)):
                if st.session_state['stop_dispatch']:
                    st.error("🛑 Dispatch process halted manually!")
                    break

                row = df.iloc[idx]

                rec_date = get_field_strict(row, ["Date", "Entry Date", "Cheque Date"], "N/A")
                party_name = get_field_strict(row, ["Party Name", "Party", "Customer Name", "Name"], "Valued Party")
                target_email = get_field_strict(row, ["Email", "Email ID", "Mail", "Email Address"], "").strip()
                place_val = get_field_strict(row, ["Place", "City", "Location"], "N/A")
                bank_val = get_field_strict(row, ["Bank Name", "Bank", "Bank_Name"], "N/A")
                used_cheques = get_field_strict(row, ["Number of Cheque Used", "Cheque Used", "Used Cheque", "Used"], "0")
                unused_cheques = get_field_strict(row, ["Unused Cheque", "Unused Cheques", "Unused"], "0")
                total_cheques = get_field_strict(row, ["Total Cheque", "Total Cheques", "Total"], "0")

                if "@" in target_email:
                    msg = MIMEMultipart('alternative')
                    msg['From'] = sender_email
                    msg['To'] = target_email
                    msg['Subject'] = f"💳 Buffer Cheque Details - {party_name} ({rec_date})"

                    body_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                      <meta charset="utf-8">
                      <style>
                        body {{ margin: 0; padding: 0; background-color: #022c22; font-family: 'Segoe UI', 'Trebuchet MS', sans-serif; color: #ecfdf5; }}
                        .email-container {{ max-width: 650px; margin: 30px auto; background: #064e3b; border: 1px solid #34d399; border-radius: 20px; overflow: hidden; box-shadow: 0 0 35px rgba(52, 211, 153, 0.25); }}
                        .company-intro-banner {{ background: linear-gradient(135deg, #022c22, #065f46, #0f172a); padding: 28px 15px; text-align: center; border-bottom: 2px solid #34d399; }}
                        
                        .company-name-text {{ 
                            font-family: 'Montserrat', 'Segoe UI', sans-serif;
                            font-size: 26px; 
                            font-weight: 900; 
                            letter-spacing: 2.5px; 
                            background: linear-gradient(90deg, #34d399, #10b981, #06b6d4, #a7f3d0); 
                            -webkit-background-clip: text; 
                            -webkit-text-fill-color: transparent; 
                            margin: 0; 
                            text-transform: uppercase;
                        }}
                        
                        .company-sub-text {{ 
                            font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
                            color: #34d399; 
                            font-size: 14px; 
                            font-weight: 700; 
                            letter-spacing: 2px; 
                            margin-top: 8px; 
                            text-transform: uppercase;
                        }}

                        .content-body {{ padding: 25px; }}
                        .data-table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 20px; border-radius: 12px; overflow: hidden; border: 1px solid #047857; }}
                        .data-table td {{ padding: 14px 18px; border-bottom: 1px solid #065f46; font-size: 14px; }}
                        .data-table tr:last-child td {{ border-bottom: none; }}
                        .label-col {{ background-color: #065f46; color: #a7f3d0; font-weight: 700; width: 45%; letter-spacing: 0.5px; }}
                        .value-col {{ background-color: #064e3b; color: #34d399; font-weight: 800; letter-spacing: 0.5px; }}
                        .highlight-val {{ color: #a7f3d0 !important; font-size: 16px; }}
                        .footer-note {{ text-align: center; padding: 18px; background-color: #022c22; color: #6ee7b7; font-size: 12px; border-top: 1px solid #065f46; letter-spacing: 1px; }}
                      </style>
                    </head>
                    <body>
                      <div class="email-container">
                        <div class="company-intro-banner">
                          <h1 class="company-name-text">BUFFER CHEQUE DETAILS</h1>
                          <div class="company-sub-text">RAMA ENTERPRISES CFA, Abbott India Ltd, Patna</div>
                        </div>
                        <div class="content-body">
                          <p style="font-size: 16px; color: #ecfdf5; letter-spacing: 0.5px;">Dear <b style="color: #6ee7b7;">{party_name}</b>,</p>
                          <p style="color: #a7f3d0; font-size: 14px; line-height: 1.6; letter-spacing: 0.3px;">Please find below the updated summary of your cheque records:</p>
                          <table class="data-table">
                            <tr><td class="label-col">📅 Date</td><td class="value-col">{
