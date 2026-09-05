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
import json

# ==========================================
# 1. Page Config & Layout Setup
# ==========================================
st.set_page_config(
    page_title="8K Cyberpunk Cheque Dispatcher Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. Perfect High-Contrast 8K Cyberpunk CSS
# ==========================================
st.markdown("""
<style>
    /* App Base Cyberpunk Background */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at 50% 10%, #064e3b, #022c22, #051a1e, #020b0e) !important;
        color: #ecfdf5 !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Sidebar Dark Emerald Theme */
    section[data-testid="stSidebar"] {
        background-color: #031c17 !important;
        border-right: 2px solid #059669 !important;
    }

    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span {
        color: #34d399 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 6px rgba(52, 211, 153, 0.4);
    }

    /* Fix All Input Boxes & Selects */
    input, select, textarea, div[data-baseweb="input"] > div {
        background-color: #0b2228 !important;
        color: #a7f3d0 !important;
        border: 1px solid #10b981 !important;
        border-radius: 8px !important;
    }

    /* Fix White File Uploader Container */
    [data-testid="stFileUploadDropzone"] {
        background-color: #091a1d !important;
        border: 2px dashed #10b981 !important;
        border-radius: 14px !important;
    }
    
    [data-testid="stFileUploadDropzone"] * {
        color: #a7f3d0 !important;
        background: transparent !important;
    }

    /* Top Floating Cyber Banner */
    .header-wrapper {
        margin-top: 10px !important;
        margin-bottom: 25px !important;
        background: rgba(4, 47, 38, 0.85);
        border: 2px solid #34d399;
        box-shadow: 0 0 30px rgba(52, 211, 153, 0.5);
        backdrop-filter: blur(12px);
        border-radius: 18px;
        padding: 24px;
        text-align: center;
    }

    .main-title {
        color: #34d399;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 1.5px;
        margin: 0;
        text-shadow: 0 0 15px rgba(52, 211, 153, 0.8);
    }

    .subtitle-badge {
        display: inline-block;
        background: #031c17;
        border: 1px solid #34d399;
        padding: 5px 20px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 800;
        color: #6ee7b7;
        margin-top: 10px;
        box-shadow: 0 0 10px rgba(52, 211, 153, 0.3);
    }

    /* Real-Time Analytics Cards */
    .metric-card-box {
        background: #072126 !important;
        border: 2px solid #059669;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .metric-card-box:hover {
        transform: translateY(-4px);
        border-color: #34d399;
        box-shadow: 0 0 25px rgba(52, 211, 153, 0.6);
    }

    .metric-label {
        font-size: 12px;
        color: #a7f3d0;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .metric-value-num {
        font-size: 36px;
        font-weight: 900;
        margin-top: 6px;
        color: #34d399;
        text-shadow: 0 0 12px rgba(52, 211, 153, 0.6);
    }

    /* Table Canvas Styling Fix (Streamlit DataFrame) */
    div[data-testid="stDataFrame"] {
        background-color: #072126 !important;
        border: 2px solid #059669 !important;
        border-radius: 12px !important;
        padding: 8px !important;
        box-shadow: 0 0 20px rgba(5, 150, 105, 0.3);
    }

    /* Force Table Text and Headers Visibility */
    div[data-testid="stDataFrame"] * {
        color: #ecfdf5 !important;
    }

    /* Solid Neon High Visibility Action Buttons */
    div.stButton > button {
        font-weight: 900 !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        font-size: 15px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.25s ease-in-out !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #047857) !important;
        color: #ffffff !important;
        border: 2px solid #34d399 !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.7) !important;
        width: 100% !important;
    }

    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(52, 211, 153, 1) !important;
        transform: scale(1.02);
    }

    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
        color: #ffffff !important;
        border: 2px solid #f87171 !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.7) !important;
        width: 100% !important;
    }

    div.stDownloadButton > button {
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.7) !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Flexible Field Extractor
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
# 4. Default 100 Demo Dataset Generator
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
# 5. Cyberpunk Sidebar Controls
# ==========================================
with st.sidebar:
    st.markdown("### 🖼️ Branding Studio")
    logo_file = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])
    if logo_file:
        st.image(logo_file, use_container_width=True)
    
    st.divider()
    st.markdown("### 🔑 Secure SMTP Setup")
    smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587)
    sender_email = st.text_input("Sender Email ID", placeholder="your_email@gmail.com")
    app_password = st.text_input("16-Digit App Password", type="password")
    dispatch_delay = st.slider("Dispatch Delay (Sec)", 0.2, 5.0, 0.8)
    
    st.divider()
    st.markdown("### ⚙️ Dispatch Settings")
    email_subject_prefix = st.text_input("Email Subject Title", value="💳 Buffer Cheque Details Notice")
    custom_cfa_title = st.text_input("CFA Header Title", value="RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA")

# ==========================================
# 6. Main Top Cyber Header
# ==========================================
st.markdown("""
<div class="header-wrapper">
    <h1 class="main-title">DHARMENDRA KUMAR (MISHRA)</h1>
    <span class="subtitle-badge">✨ ARCHITECT & DESIGNER: RAJVEER</span>
    <p style="color: #a7f3d0; margin-top: 10px; font-weight: 700; font-size: 15px;">
        ⚡ 8K CHEQUE DISPATCHER & AUTOMATED EMAIL MANAGEMENT ENGINE
    </p>
</div>
""", unsafe_allow_html=True)

# Custom File Import Dropzone
uploaded_file = st.file_uploader("📁 Import Custom Excel/CSV Data File", type=["xlsx", "csv"])
if uploaded_file is not None:
    try:
        new_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file, engine='openpyxl')
        new_df.columns = [str(c).strip() for c in new_df.columns]
        st.session_state['crm_data'] = new_df
        st.session_state['sent_count'] = 0
        st.session_state['failed_count'] = 0
        st.success(f"✅ Loaded {len(new_df)} records successfully!")
    except Exception as e:
        st.error(f"❌ File loading error: {e}")

df = st.session_state['crm_data']

# ==========================================
# 7. Real-time Metrics & Data Health Checks
# ==========================================
st.markdown("### 📊 Real-time Batch Metrics & Validation")
c1, c2, c3, c4 = st.columns(4)

total_records = len(df)
pending_records = total_records - (st.session_state['sent_count'] + st.session_state['failed_count'])

# Data Health Audit
missing_emails = 0
if 'Email' in df.columns:
    missing_emails = int(df['Email'].isnull().sum() + (df['Email'] == '').sum())

with c1: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Total Records</div><div class="metric-value-num">{total_records}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Sent Success</div><div class="metric-value-num" style="color:#34d399;">{st.session_state["sent_count"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Failed/Invalid</div><div class="metric-value-num" style="color:#f87171;">{st.session_state["failed_count"]}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card-box"><div class="metric-label">Missing Email Alerts</div><div class="metric-value-num" style="color:#fbbf24;">{missing_emails}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Feature 1: Quick Search Filter
search_term = st.text_input("🔍 Quick Search Filter (Party Name, Email, or Bank)", "")
if search_term:
    filtered_df = df[df.apply(lambda r: search_term.lower() in str(r.values).lower(), axis=1)]
else:
    filtered_df = df

# ==========================================
# 8. Interactive Grid View
# ==========================================
st.markdown(f"### ✏️ Interactive Cheque Details Grid ({len(filtered_df)} Records Visible)")

edited_df = st.data_editor(
    filtered_df,
    num_rows="dynamic",
    use_container_width=True,
    height=360
)
st.session_state['crm_data'] = edited_df

st.markdown("<br>", unsafe_allow_html=True)

# Dispatch Controls
st.markdown("### 🚀 Dispatch Control Actions")
c_start, c_stop, c_export_csv, c_export_json = st.columns([1.8, 1.1, 1.1, 1.1])

with c_start: start_btn = st.button("🚀 LAUNCH DISPATCH", type="primary", use_container_width=True)
with c_stop: stop_btn = st.button("🛑 EMERGENCY STOP", type="secondary", use_container_width=True)

with c_export_csv:
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button("📥 EXPORT CSV", data=csv_buffer.getvalue(), file_name="Cheque_Details.csv", mime="text/csv", use_container_width=True)

with c_export_json:
    json_buffer = df.to_json(orient="records", indent=2)
    st.download_button("📜 EXPORT JSON", data=json_buffer, file_name="Cheque_Details.json", mime="application/json", use_container_width=True)

if stop_btn:
    st.session_state['stop_dispatch'] = True
    st.warning("🛑 Emergency Stop Triggered!")

st.markdown("---")

# ==========================================
# 9. HTML Email Template & Single Test Mail Tool
# ==========================================
def build_email_template(party, date_val, acc, place, bank, u_ail, u_ahpl, h_ail, h_ahpl, cfa_title):
    return f"""<!DOCTYPE html>
<html>
<body style="margin:0; padding:20px; background-color:#f4f6f8; font-family: Arial, sans-serif;">
  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #064e3b; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
    <tr>
      <td style="padding: 20px; text-align: center;">
        <div style="background-color: #34d399; border-radius: 8px; padding: 14px; text-align: center;">
          <h2 style="margin: 0; color: #022c22; font-size: 20px; font-weight: 900;">
            BUFFER CHEQUE DETAILS
          </h2>
        </div>
        <p style="color: #a7f3d0; font-size: 12px; font-weight: bold; margin-top: 10px;">✨ {cfa_title}</p>
      </td>
    </tr>
    <tr>
      <td style="padding: 0 24px 24px 24px;">
        <p style="color: #ffffff; font-size: 15px;">Dear <b style="color: #34d399;">{party}</b>,</p>
        <p style="color: #a7f3d0; font-size: 13px;">Please review your updated cheque summary details below:</p>
        <table border="0" cellpadding="10" cellspacing="0" width="100%" style="background-color: #022c22; border-radius: 8px;">
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">📅 Date</td>
            <td style="color: #34d399; font-weight: bold; font-size: 13px;">{date_val}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">👤 Party Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 13px;">{party}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">🔢 Account Number</td>
            <td style="color: #38bdf8; font-weight: bold; font-size: 13px;">{acc}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">📍 Place</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 13px;">{place}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">🏦 Bank Name</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 13px;">{bank}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">🏷️ Cheques Used in AIL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 13px;">{u_ail}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">🏷️ Cheques Used in AHPL</td>
            <td style="color: #ffffff; font-weight: bold; font-size: 13px;">{u_ahpl}</td>
          </tr>
          <tr style="border-bottom: 1px solid #065f46;">
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">📥 Total Cheque in Hand AIL</td>
            <td style="color: #34d399; font-weight: bold; font-size: 13px;">{h_ail}</td>
          </tr>
          <tr>
            <td style="color: #a7f3d0; font-weight: bold; font-size: 13px;">📥 Total Cheque in Hand AHPL</td>
            <td style="color: #34d399; font-weight: bold; font-size: 13px;">{h_ahpl}</td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

# Single Email Tester Feature
st.markdown("### 🧪 Direct Single-Client Email Tester")
col_t1, col_t2 = st.columns([2.2, 1])
with col_t1:
    test_target_email = st.text_input("Enter Test Email Address", placeholder="testclient@gmail.com")
with col_t2:
    st.markdown("<br>", unsafe_allow_html=True)
    send_test_btn = st.button("✉️ SEND TEST MAIL NOW")

if send_test_btn:
    if not sender_email or not app_password or not test_target_email:
        st.warning("⚠️ Please fill in SMTP credentials & recipient email!")
    else:
        try:
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()
            server.login(sender_email.strip(), app_password.replace(" ", ""))
            
            msg = MIMEMultipart('alternative')
            msg['From'] = formataddr((custom_cfa_title, sender_email.strip()))
            msg['To'] = test_target_email
            msg['Subject'] = f"TEST: {email_subject_prefix}"
            
            test_html = build_email_template("Sample Client", "2026-08-05", "359421736530", "Patna", "State Bank of India", "2", "3", "12", "14", custom_cfa_title)
            msg.attach(MIMEText(test_html, 'html'))
            server.sendmail(sender_email.strip(), test_target_email, msg.as_string())
            server.quit()
            st.success(f"✅ Test email successfully dispatched to {test_target_email}!")
        except Exception as te:
            st.error(f"❌ Test dispatch failed: {te}")

# ==========================================
# 10. Automated Email Dispatch Engine Loop
# ==========================================
if start_btn:
    st.session_state['stop_dispatch'] = False
    st.session_state['sent_count'] = 0
    st.session_state['failed_count'] = 0

    if not sender_email or not app_password:
        st.warning("⚠️ Please provide Sender Email ID and App Password in the Sidebar!")
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
                    st.error("🛑 Dispatch Stopped Manually!")
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
                        status_box.info(f"🟢 [{idx+1}/{len(df)}] Sent: **{party_name}** ({target_email})")
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
            st.success("🎉 Cheque Details Email Dispatch Sequence Completed!")

        except Exception as conn_err:
            st.error(f"❌ Connection Error: {conn_err}")
