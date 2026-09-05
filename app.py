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
# 2. Complete Dark Dynamic CSS (All White Backgrounds Overridden)
# ==========================================
st.markdown("""
<style>
    /* Global App Canvas */
    .stApp, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 20%, #064e3b, #022c22, #0f172a, #042f2e) !important;
        color: #ecfdf5 !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Sidebar Complete Dark Overhaul */
    section[data-testid="stSidebar"] {
        background-color: #022c22 !important;
        border-right: 2px solid #065f46 !important;
    }

    /* Override ALL Inputs & Text Areas White Background */
    input, select, textarea, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        color: #34d399 !important;
        border: 1px solid #059669 !important;
        border-radius: 8px !important;
    }
    
    /* File Uploader Container Fix */
    section[data-testid="stFileUploadDropzone"] {
        background: #0f172a !important;
        border: 2px dashed #34d399 !important;
        border-radius: 14px !important;
    }
    
    section[data-testid="stFileUploadDropzone"] * {
        color: #a7f3d0 !important;
    }

    /* Top Spaced Header */
    .header-wrapper {
        margin-top: 45px !important;
        margin-bottom: 25px;
        background: rgba(6, 78, 59, 0.85);
        border: 2px solid #34d399;
        box-shadow: 0 0 35px rgba(52, 211, 153, 0.5);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
    }

    .main-title {
        color: #34d399;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 1.2px;
        margin: 0;
        text-shadow: 0 0 18px rgba(52, 211, 153, 0.7);
    }

    .subtitle-badge {
        display: inline-block;
        background: #022c22;
        border: 1px solid #34d399;
        padding: 5px 20px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 800;
        color: #34d399;
        margin-top: 10px;
    }

    /* Metric Cards */
    .metric-card-box {
        background: #0f172a !important;
        border: 2px solid rgba(52, 211, 153, 0.6);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .metric-card-box:hover {
        transform: translateY(-6px) scale(1.05);
        border-color: #06b6d4;
        box-shadow: 0 0 35px rgba(6, 182, 212, 0.8);
    }

    .metric-label {
        font-size: 13px;
        color: #a7f3d0;
        font-weight: 800;
        text-transform: uppercase;
    }
    
    .metric-value-num {
        font-size: 36px;
        font-weight: 900;
        margin-top: 6px;
        color: #34d399;
        text-shadow: 0 0 12px rgba(52, 211, 153, 0.6);
    }

    /* ALL Streamlit Buttons Custom Styling (Fix White Export Button) */
    div.stButton > button, div.stDownloadButton > button {
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 14px 22px !important;
        transition: all 0.25s ease !important;
    }

    /* Primary Launch Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: #ffffff !important;
        font-size: 18px !important;
        border: 2px solid #34d399 !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.8) !important;
        width: 100% !important;
    }

    /* Emergency Stop Button */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        border: 2px solid #f87171 !important;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.8) !important;
        width: 100% !important;
    }

    /* Download Export Button (Replaced White Styling) */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        border: 2px solid #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.7) !important;
        width: 100% !important;
    }

    div.stDownloadButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 1) !important;
    }

    /* Data Table Dark Theme Styling */
    div[data-testid="stDataFrame"] {
        background-color: #0f172a !important;
        border: 1px solid #059669 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Strict Alias Field Matching Engine
# ==========================================
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

# ==========================================
# 4. Default 100 Records Cache Data
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

# Session State Setup
if 'crm_data' not in st.session_state:
    st.session_state['crm_data'] = load_default_100_records()
if 'sent_count' not in st.session_state:
    st.session_state['sent_count'] = 0
if 'failed_count' not in st.session_state:
    st.session_state['failed_count'] = 0
if 'stop_dispatch' not in st.session_state:
    st.session_state['stop_dispatch'] = False

# ==========================================
# 5. Sidebar Control Panel
# ==========================================
with st.sidebar:
    st.markdown("### 🖼️ Brand Logo Studio")
    logo_file = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])
    if logo_file:
        st.image(logo_file, use_container_width=True)
    
    st.divider()
    st.markdown("### 🔑 SMTP Server Engine")
    smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587)
    sender_email = st.text_input("Sender Email ID", placeholder="your_email@gmail.com")
    app_password = st.text_input("16-Digit App Password", type="password")
    dispatch_delay = st.slider("Dispatch Rate Delay (Seconds)", 0.5, 5.0, 1.0)
    
    # SMTP Status Check
    if sender_email and app_password:
        st.markdown("🟢 **Status**: SMTP Credentials Ready")
    else:
        st.markdown("🔴 **Status**: Credentials Required")

# ==========================================
# 6. Top Spaced Header Title
# ==========================================
st.markdown("""
<div class="header-wrapper">
    <h1 class="main-title">DHARMENDRA KUMAR (MISHRA)</h1>
    <span class="subtitle-badge">✨ ARCHITECT & DESIGNER: RAJVEER</span>
    <p style="color: #a7f3d0; margin-top: 12px; font-weight: 700; font-size: 16px;">
        ⚡ 8K ULTRA-DYNAMIC CHEQUE DISPATCHER & AUTOMATED EMAIL MANAGEMENT ENGINE
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. File Import & Progress Dashboard
# ==========================================
uploaded_file = st.file_uploader("📁 Upload Fresh Excel/CSV Data File", type=["xlsx", "csv"])
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

st.markdown("### 📊 Live Analytics & Dispatch Progress")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Total Records</div><div class="metric-value-num">{total_records}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Sent Success</div><div class="metric-value-num" style="color:#34d399;">{st.session_state["sent_count"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Failed</div><div class="metric-value-num" style="color:#f87171;">{st.session_state["failed_count"]}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Pending</div><div class="metric-value-num" style="color:#fbbf24;">{max(0, pending_records)}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 8. Data Grid & Interactive Email Simulator Split Layout
# ==========================================
col_grid, col_preview = st.columns([1.1, 0.9])

with col_grid:
    st.markdown(f"### ✏️ Editable Data Grid ({len(df)} Records)")
    edited_df = st.data_editor(st.session_state['crm_data'], num_rows="dynamic", use_container_width=True, height=380)
    st.session_state['crm_data'] = edited_df
    df = st.session_state['crm_data']

    st.markdown("### 🚀 Dispatch Control Actions")
    c_start, c_stop, c_export = st.columns([1.8, 1.2, 1.2])
    with c_start: start_btn = st.button("🚀 LAUNCH DISPATCH", type="primary", use_container_width=True)
    with c_stop: stop_btn = st.button("🛑 STOP", type="secondary", use_container_width=True)
    with c_export:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button("📥 EXPORT CSV", data=csv_buffer.getvalue(), file_name="Cheque_Report.csv", mime="text/csv", use_container_width=True)

    if stop_btn:
        st.session_state['stop_dispatch'] = True
        st.warning("🛑 Emergency Stop Triggered!")

# Email Template Generator Function
def generate_email_html(party, date_val, acc, place, bank, u_ail, u_ahpl, h_ail, h_ahpl):
    return f"""
    <div style="background-color: #f4f6f8; padding: 15px; border-radius: 12px; font-family: Arial, sans-serif;">
        <div style="max-width: 580px; margin: 0 auto; background-color: #064e3b; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
            <div style="padding: 20px; text-align: center;">
                <div style="background-color: #34d399; border-radius: 10px; padding: 14px; text-align: center;">
                    <h2 style="margin: 0; color: #022c22; font-size: 20px; font-weight: 900;">BUFFER CHEQUE DETAILS</h2>
                </div>
                <!-- Animated Auto-Fade Out Banner (3.5s) -->
                <div style="background: linear-gradient(90deg, #10b981, #06b6d4, #34d399); color: #022c22; font-weight: 900; font-size: 12px; border-radius: 6px; padding: 10px; margin-top: 10px; text-align: center; text-transform: uppercase;">
                    ✨ RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA
                </div>
            </div>
            <div style="padding: 0 20px 20px 20px;">
                <p style="color: #ffffff; font-size: 15px; margin-bottom: 5px;">Dear <b style="color: #34d399;">{party}</b>,</p>
                <p style="color: #a7f3d0; font-size: 13px; margin-top: 0; margin-bottom: 18px;">Summary of your registered cheque records:</p>
                <table border="0" cellpadding="10" cellspacing="0" width="100%" style="background-color: #022c22; border-radius: 8px; border-collapse: collapse; font-size: 13px;">
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">📅 Date</td><td style="color: #34d399; font-weight: bold;">{date_val}</td></tr>
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">👤 Party Name</td><td style="color: #ffffff;">{party}</td></tr>
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">🔢 Account Number</td><td style="color: #38bdf8; font-weight: bold;">{acc}</td></tr>
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">📍 Place</td><td style="color: #ffffff;">{place}</td></tr>
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">🏦 Bank Name</td><td style="color: #ffffff;">{bank}</td></tr>
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">🏷️ Cheques Used AIL</td><td style="color: #ffffff;">{u_ail}</td></tr>
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">🏷️ Cheques Used AHPL</td><td style="color: #ffffff;">{u_ahpl}</td></tr>
                    <tr style="border-bottom: 1px solid #065f46;"><td style="color: #a7f3d0; font-weight: bold;">📥 Total Hand AIL</td><td style="color: #34d399; font-weight: bold;">{h_ail}</td></tr>
                    <tr><td style="color: #a7f3d0; font-weight: bold;">📥 Total Hand AHPL</td><td style="color: #34d399; font-weight: bold;">{h_ahpl}</td></tr>
                </table>
            </div>
            <div style="background-color: #022c22; padding: 15px; text-align: center; border-top: 1px solid #065f46;">
                <div style="color: #34d399; font-weight: 800; font-size: 13px;">RAMA ENTERPRISES CFA</div>
                <div style="color: #a7f3d0; font-size: 11px;">ABBOTT INDIA LTD, PATNA</div>
            </div>
        </div>
    </div>
    """

# Live Email Simulator Column
with col_preview:
    st.markdown("### 👁️ Live Email Inbox Simulator")
    selected_row_idx = st.number_input("Select Record Index to Simulate Preview", min_value=0, max_value=max(0, len(df)-1), value=0)
    
    if len(df) > 0:
        row = df.iloc[selected_row_idx]
        p_name = get_field_strict(row, ["Party Name", "Party", "Name"], "Valued Customer")
        p_date = get_field_strict(row, ["Date", "Entry Date"], "2026-08-01")
        p_acc = get_field_strict(row, ["Account Number", "Account No"], "3500123499")
        p_place = get_field_strict(row, ["Place", "City"], "Patna")
        p_bank = get_field_strict(row, ["Bank Name", "Bank"], "State Bank of India")
        p_u_ail = get_field_strict(row, ["Number of cheque used in AIL"], "2")
        p_u_ahpl = get_field_strict(row, ["Number of cheque used In AHPL"], "3")
        p_h_ail = get_field_strict(row, ["Total cheque in hand AIL"], "12")
        p_h_ahpl = get_field_strict(row, ["Total cheque in hand AHPL"], "15")

        simulated_html = generate_email_html(p_name, p_date, p_acc, p_place, p_bank, p_u_ail, p_u_ahpl, p_h_ail, p_h_ahpl)
        st.components.v1.html(simulated_html, height=450, scrolling=True)

# ==========================================
# 9. Email Dispatch Engine Execution
# ==========================================
if start_btn:
    st.session_state['stop_dispatch'] = False
    st.session_state['sent_count'] = 0
    st.session_state['failed_count'] = 0

    if not sender_email or not app_password:
        st.warning("⚠️ Please fill Sender Email and App Password in Sidebar!")
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
                    custom_sender = "RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA"
                    msg['From'] = formataddr((custom_sender, sender_email.strip()))
                    msg['To'] = target_email
                    msg['Subject'] = f"💳 Buffer Cheque Details - {party_name} ({rec_date})"

                    full_mail_body = generate_email_html(party_name, rec_date, account_val, place_val, bank_val, used_ail, used_ahpl, hand_ail, hand_ahpl)
                    msg.attach(MIMEText(full_mail_body, 'html'))
                    
                    try:
                        server.sendmail(sender_email.strip(), target_email, msg.as_string())
                        st.session_state['sent_count'] += 1
                        status_box.info(f"🟢 [{idx+1}/{len(df)}] Sent to **{party_name}** ({target_email})")
                    except Exception as send_err:
                        st.session_state['failed_count'] += 1
                        status_box.error(f"🔴 [{idx+1}/{len(df)}] Failed: {target_email}")
                else:
                    st.session_state['failed_count'] += 1
                    status_box.warning(f"⚠️ [{idx+1}/{len(df)}] Invalid Email: **{party_name}**")

                progress = (idx + 1) / len(df)
                progress_bar.progress(progress)
                time.sleep(dispatch_delay)

            server.quit()
            st.balloons()
            st.success("🎉 Cheque Record Dispatch Completed Successfully!")

        except Exception as conn_err:
            st.error(f"❌ Connection Error: {conn_err}")
