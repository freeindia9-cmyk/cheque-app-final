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
    .header-container { display: flex; flex-direction: column; gap: 6px; }
    .floating-header {
        background: linear-gradient(90deg, #34d399, #10b981, #06b6d4, #a7f3d0);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px; font-weight: 900; letter-spacing: -1px;
        animation: gradientShift 6s ease infinite, floatTitle 3s ease-in-out infinite;
        margin: 0; display: inline-block;
    }
    .designer-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(6, 182, 212, 0.25));
        border: 1px solid rgba(52, 211, 153, 0.4); padding: 6px 16px; border-radius: 30px;
        font-size: 14px; font-weight: 700; letter-spacing: 1.2px; color: #34d399;
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.2); width: fit-content; margin-top: 4px;
    }
    .logo-frame {
        display: inline-block; padding: 8px; border-radius: 24px;
        background: linear-gradient(135deg, #34d399, #06b6d4, #10b981);
        box-shadow: 0 0 25px rgba(52, 211, 153, 0.6);
    }
    .metric-card {
        background: rgba(6, 78, 59, 0.45); border: 1px solid rgba(52, 211, 153, 0.25);
        border-radius: 20px; padding: 22px; text-align: center; backdrop-filter: blur(16px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }
    .metric-title { font-size: 14px; color: #a7f3d0; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }
    .metric-value { font-size: 36px; font-weight: 900; margin-top: 8px; background: linear-gradient(90deg, #34d399, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #06b6d4 100%) !important;
        color: #ffffff !important; font-size: 18px !important; font-weight: 800 !important;
        border-radius: 14px !important; padding: 16px 28px !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.5) !important;
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

# 4. Default Records Generator (With Account Number Added)
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
        used = random.randint(1, 15)
        unused = random.randint(2, 25)
        account_no = f"35{random.randint(1000000000, 9999999999)}"
        records.append({
            "Date": entry_dt.strftime("%Y-%m-%d"),
            "Party Name": party_name,
            "Account Number": account_no,  # <-- Added Account Number Column
            "Email": f"{email_prefix}@clientdomain.com",
            "Place": random.choice(places),
            "Bank Name": random.choice(banks),
            "Number of Cheque Used": used,
            "Unused Cheque": unused,
            "Total Cheque": used + unused
        })
    return pd.DataFrame(records)

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
        <div><span class="designer-badge">✨ ARCHITECT & DESIGNER: DHARMENDRA KUMAR (MISHRA)</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("🚀 Automated Cheque Record Dispatcher & Email Management Engine")

st.divider()

# 7. Excel/CSV Import
st.markdown("### 📂 Import Cheque Details (Excel / CSV)")
uploaded_file = st.file_uploader("Upload fresh Excel file", type=["xlsx", "csv"])

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
st.markdown(f"### ✏️ Interactive Cheque Details Grid ({len(df)} Records Ready)")
edited_df = st.data_editor(st.session_state['crm_data'], num_rows="dynamic", use_container_width=True, height=420)
st.session_state['crm_data'] = edited_df
df = st.session_state['crm_data']

if 'stop_dispatch' not in st.session_state:
    st.session_state['stop_dispatch'] = False

col_start, col_stop = st.columns([2, 1])
with col_start: start_btn = st.button("🚀 Launch Cheque Details Dispatch", type="primary", use_container_width=True)
with col_stop: stop_btn = st.button("🛑 Emergency Stop", use_container_width=True)

if stop_btn: st.session_state['stop_dispatch'] = True

if start_btn:
    st.session_state['stop_dispatch'] = False
    st.session_state['sent_count'] = 0
    st.session_state['failed_count'] = 0

    if not sender_email or not app_password:
        st.warning("⚠️ Kripya sidebar me Sender Email ID aur App Password enter karein!")
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
                account_val = get_field_strict(row, ["Account Number", "Account No", "Account", "A/C No"], "N/A") # <-- Extracting Account Number
                target_email = get_field_strict(row, ["Email", "Email ID", "Mail", "Email Address"], "").strip()
                place_val = get_field_strict(row, ["Place", "City", "Location"], "N/A")
                bank_val = get_field_strict(row, ["Bank Name", "Bank"], "N/A")
                used_cheques = get_field_strict(row, ["Number of Cheque Used", "Used"], "0")
                unused_cheques = get_field_strict(row, ["Unused Cheque", "Unused"], "0")
                total_cheques = get_field_strict(row, ["Total Cheque", "Total"], "0")

                if "@" in target_email:
                    msg = MIMEMultipart('alternative')
                    
                    custom_sender_name = "CFA ABBOTT INDIA LTD,PATNA"
                    msg['From'] = formataddr((custom_sender_name, sender_email.strip()))
                    
                    msg['To'] = target_email
                    msg['Subject'] = f"💳 Buffer Cheque Details - {party_name} ({rec_date})"

                    body_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <body style="margin: 0; padding: 0; background-color: #022c22; font-family: 'Segoe UI', sans-serif; color: #ecfdf5;">
                      <div style="max-width: 650px; margin: 30px auto; background: #064e3b; border: 1px solid #34d399; border-radius: 20px; overflow: hidden;">
                        <div style="background: linear-gradient(135deg, #022c22, #065f46); padding: 28px; text-align: center; border-bottom: 2px solid #34d399;">
                          <h1 style="color: #34d399; font-size: 26px; font-weight: 900; margin: 0;">BUFFER CHEQUE DETAILS</h1>
                          <div style="color: #6ee7b7; font-size: 14px; margin-top: 8px;">CFA, Abbott India Ltd, Patna</div>
                        </div>
                        <div style="padding: 25px;">
                          <p>Dear <b>{party_name}</b>,</p>
                          <p>Please find below the updated summary of your cheque records:</p>
                          <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                            <tr><td style="background: #065f46; padding: 10px;">📅 Date</td><td style="background: #064e3b; padding: 10px;">{rec_date}</td></tr>
                            <tr><td style="background: #065f46; padding: 10px;">👤 Party Name</td><td style="background: #064e3b; padding: 10px;">{party_name}</td></tr>
                            <tr><td style="background: #065f46; padding: 10px;">🔢 Account Number</td><td style="background: #064e3b; padding: 10px; color: #38bdf8; font-weight: bold;">{account_val}</td></tr>
                            <tr><td style="background: #065f46; padding: 10px;">📍 Place</td><td style="background: #064e3b; padding: 10px;">{place_val}</td></tr>
                            <tr><td style="background: #065f46; padding: 10px;">🏦 Bank Name</td><td style="background: #064e3b; padding: 10px;">{bank_val}</td></tr>
                            <tr><td style="background: #065f46; padding: 10px;">🏷️ Used Cheques</td><td style="background: #064e3b; padding: 10px;">{used_cheques}</td></tr>
                            <tr><td style="background: #065f46; padding: 10px;">📦 Unused Cheques</td><td style="background: #064e3b; padding: 10px;">{unused_cheques}</td></tr>
                            <tr><td style="background: #065f46; padding: 10px;">📊 Total Cheques</td><td style="background: #064e3b; padding: 10px;">{total_cheques}</td></tr>
                          </table>
                        </div>
                        <div style="text-align: center; padding: 15px; background: #022c22; font-size: 12px; color: #6ee7b7;">⚡ Dispatch Engine by Dharmendra Kumar (Mishra)</div>
                      </div>
                    </body>
                    </html>
                    """
                    msg.attach(MIMEText(body_html, 'html'))

                    try:
                        server.sendmail(sender_email.strip(), target_email, msg.as_string())
                        st.session_state['sent_count'] += 1
                        status_box.info(f"⚡ [{idx+1}/{len(df)}] Dispatched as '{custom_sender_name}' to: {target_email}")
                    except Exception as err:
                        st.session_state['failed_count'] += 1
                        status_box.warning(f"⚠️ [{idx+1}/{len(df)}] Failed for {target_email}: {err}")
                else:
                    st.session_state['failed_count'] += 1
                    status_box.warning(f"⚠️ [{idx+1}/{len(df)}] Invalid/Missing Email for {party_name}")

                progress_bar.progress((idx + 1) / len(df))
                time.sleep(dispatch_delay)

            server.quit()
            st.success("🎉 Bulk Dispatch Completed!")
        except Exception as conn_err:
            st.error(f"❌ SMTP Connection Error: {conn_err}")

st.markdown("<br><hr><div style='text-align: center; color: #34d399; font-weight: 700;'>⚡ Designed & Developed by Dharmendra Kumar (Mishra)</div>", unsafe_allow_html=True)
