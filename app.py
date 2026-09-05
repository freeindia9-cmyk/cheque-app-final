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
# 2. Complete Dark Theme CSS (Zero White Elements)
# ==========================================
st.markdown("""
<style>
    /* Global App Canvas Background */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at 50% 20%, #064e3b, #022c22, #0f172a, #042f2e) !important;
        color: #ecfdf5 !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Sidebar Dark Overhaul */
    section[data-testid="stSidebar"] {
        background-color: #022c22 !important;
        border-right: 2px solid #065f46 !important;
    }

    /* Override ALL Inputs Backgrounds & Texts */
    input, select, textarea, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        color: #34d399 !important;
        border: 1px solid #059669 !important;
        border-radius: 10px !important;
    }

    /* Force Table Header & Cell Backgrounds to Dark Emerald Slate */
    div[data-testid="stDataFrame"] {
        background-color: #0f172a !important;
        border: 2px solid #059669 !important;
        border-radius: 14px !important;
        padding: 10px !important;
    }

    div[data-testid="stDataFrame"] * {
        background-color: #0f172a !important;
        color: #ecfdf5 !important;
    }

    /* File Uploader Container Fix */
    section[data-testid="stFileUploadDropzone"] {
        background: #0f172a !important;
        border: 2px dashed #34d399 !important;
        border-radius: 16px !important;
        margin-bottom: 25px !important;
    }

    section[data-testid="stFileUploadDropzone"] * {
        color: #a7f3d0 !important;
    }

    /* Header Spacing Container */
    .header-wrapper {
        margin-top: 40px !important;
        margin-bottom: 35px !important;
        background: rgba(6, 78, 59, 0.85);
        border: 2px solid #34d399;
        box-shadow: 0 0 35px rgba(52, 211, 153, 0.5);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
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
        padding: 6px 22px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 800;
        color: #34d399;
        margin-top: 12px;
    }

    /* Metric Analytics Cards Spacing */
    .metric-card-box {
        background: #0f172a !important;
        border: 2px solid rgba(52, 211, 153, 0.6);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 25px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .metric-card-box:hover {
        transform: translateY(-6px) scale(1.04);
        border-color: #06b6d4;
        box-shadow: 0 0 35px rgba(6, 182, 212, 0.85);
    }

    .metric-label {
        font-size: 13px;
        color: #a7f3d0;
        font-weight: 800;
        text-transform: uppercase;
    }
    
    .metric-value-num {
        font-size: 38px;
        font-weight: 900;
        margin-top: 8px;
        color: #34d399;
        text-shadow: 0 0 12px rgba(52, 211, 153, 0.6);
    }

    /* High Visibility Buttons Custom Styling */
    div.stButton > button, div.stDownloadButton > button {
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        transition: all 0.25s ease !important;
    }

    /* Launch Dispatch Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: #ffffff !important;
        font-size: 18px !important;
        border: 2px solid #34d399 !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.85) !important;
        width: 100% !important;
    }

    /* Emergency Stop Button */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        border: 2px solid #f87171 !important;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.85) !important;
        width: 100% !important;
    }

    /* Fix Export CSV Button (Neon Cyan Dark Theme) */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        border: 2px solid #38bdf8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.8) !important;
        width: 100% !important;
    }

    div.stDownloadButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 35px rgba(56, 189, 248, 1) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Strict Column Alias Matching Engine
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
# 4. Default 100 Records Generator
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
# 5. Sidebar Controls Panel
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
# 6. Top Spaced Floating Header
# ==========================================
st.markdown("""
<div class="header-wrapper">
    <h1 class="main-title">DHARMENDRA KUMAR (MISHRA)</h1>
    <span class="subtitle-badge">✨ ARCHITECT & DESIGNER: RAJVEER</span>
    <p style="color: #a7f3d0; margin-top: 14px; font-weight: 700; font-size: 16px;">
        ⚡ 8K ULTRA-DYNAMIC CHEQUE DISPATCHER & AUTOMATED EMAIL MANAGEMENT ENGINE
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. File Import & Data Dashboard
# ==========================================
uploaded_file = st.file_uploader("📁 Upload Fresh Excel/CSV Batch File", type=["xlsx", "csv"])
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

st.markdown("### 📊 Live Dispatch Progress Analytics")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Total Records</div><div class="metric-value-num">{total_records}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Sent Success</div><div class="metric-value-num" style="color:#34d399;">{st.session_state["sent_count"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Failed</div><div class="metric-value-num" style="color:#f87171;">{st.session_state["failed_count"]}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Pending</div><div class="metric-value-num" style="color:#fbbf24;">{max(0, pending_records)}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 8. Interactive Data Grid
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
# 9. Dynamic Live Email Simulator Panel (No Mail Sent Needed)
# ==========================================
st.markdown("### 👁️ Interactive Email Inbox Simulator (Test Layout Within App)")

def build_email_template(party, date_val, acc, place, bank, u_ail, u_ahpl, h_ail, h_ahpl, cfa_title):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @keyframes autoFadeOutBanner {{
            0% {{ opacity: 1; max-height: 80px; padding: 12px; margin-top: 10px; }}
            70% {{ opacity: 1; max-height: 80px; padding: 12px; margin-top: 10px; }}
            100% {{ opacity: 0; max-height: 0px; padding: 0px; margin-top: 0px; overflow: hidden; display: none; }}
        }}
        .fade-banner {{
            background: linear-gradient(90deg, #10b981, #06b6d4, #34d399);
            color: #022c22;
            font-weight: 900;
            font-size: 13px;
            border-radius: 8px;
            text-align: center;
            letter-spacing: 1px;
            text-transform: uppercase;
            box-shadow: 0 0 15px rgba(52, 211, 153, 0.8);
            animation: autoFadeOutBanner 3.5s forwards ease-in-out;
        }}
    </style>
</head>
<body style="margin:0; padding:20px; background-color:#f4f6f8; font-family: 'Segoe UI', Arial, sans-serif;">
  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; background-color: #064e3b; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
    <tr>
      <td style="padding: 24px; text-align: center;">
        <div style="background-color: #34d399; border-radius: 12px; padding: 18px 10px; text-align: center; box-shadow: 0 0 20px rgba(52, 211, 153, 0.6);">
          <h1 style="margin: 0; color: #022c22; font-size: 24px; font-weight: 900; letter-spacing: 1px;">
            BUFFER CHEQUE DETAILS
          </h1>
        </div>
        
        <!-- Interactive Banner (Fades out 3.5s after opening email) -->
        <div class="fade-banner">
          ✨ {cfa_title}
        </div>
      </td>
    </tr>
    <tr>
      <td style="padding: 0 28px 28px 28px;">
        <p style="color: #ffffff; font-size: 16px; margin-bottom: 8px;">Dear <b style="color: #34d399;">{party}</b>,</p>
        <p style="color: #a7f3d0; font-size: 14px; margin-top: 0; margin-bottom: 22px;">Please find below the updated summary of your cheque records:</p>
        <table border="0" cellpadding="12" cellspacing="0" width="100%" style="border-collapse: collapse; background-color: #022c22; border-radius: 10px; overflow: hidden;">
          <tr style="border-bottom: 1px solid #065f46;">
            <td width="50%" style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📅 Date</td>
            <td width="50%" style="color: #34d399; font-weight: bold; font-size: 14px;">{date_val}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">👤 Party Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{party}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🔢 Account Number</td>
            <td style="color: #38bdf8; font-weight: bold; font-size: 14px;">{acc}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📍 Place</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{place}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🏦 Bank Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{bank}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AIL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{u_ail}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AHPL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 14px;">{u_ahpl}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AIL</td>
            <td style="color: #34d399; font-weight: bold; font-size: 14px;">{h_ail}</td>
          </tr>
          <tr>
            <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AHPL</td>
            <td style="color: #34d399; font-weight: bold; font-size: 14px;">{h_ahpl}</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td style="background-color: #022c22; padding: 20px; text-align: center; border-top: 1px solid #065f46;">
        <div style="color: #34d399; font-weight: 800; font-size: 14px;">{cfa_title}</div>
      </td>
    </tr>
  </table>
</body>
</html>"""

col_test_input, col_test_render = st.columns([1, 1], gap="large")

with col_test_input:
    st.markdown("#### 🧪 Test Data Controls")
    sim_party = st.text_input("Simulated Party Name", value="Aarav Sharma")
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
# 10. Main Email Dispatch Execution
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
                        status_box.info(f"🟢 [{idx+1}/{len(df)}] Sent to **{party_name}** ({target_email})")
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
