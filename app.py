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

# 2. Ultra Dynamic Cyberpunk Neon Emerald & Extra Glowing Animations CSS
st.markdown("""
<style>
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #022c22, #064e3b, #0f172a, #065f46, #022c22);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
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
        background: linear-gradient(90deg, #34d399, #10b981, #06b6d4, #a7f3d0, #34d399);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -1px;
        animation: gradientShift 5s ease infinite, floatTitle 3s ease-in-out infinite;
        margin: 0;
        display: inline-block;
        filter: drop-shadow(0 0 15px rgba(52, 211, 153, 0.4));
    }

    .designer-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(6, 182, 212, 0.3));
        border: 1px solid rgba(52, 211, 153, 0.6);
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #34d399;
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.4), inset 0 0 10px rgba(52, 211, 153, 0.2);
        width: fit-content;
        margin-top: 4px;
        animation: pulseBadge 2.5s infinite alternate;
    }

    @keyframes pulseBadge {
        0% { border-color: rgba(52, 211, 153, 0.4); box-shadow: 0 0 10px rgba(52, 211, 153, 0.2); }
        100% { border-color: rgba(6, 182, 212, 0.9); box-shadow: 0 0 30px rgba(6, 182, 212, 0.6); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes floatTitle {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    .logo-frame {
        display: inline-block;
        padding: 8px;
        border-radius: 24px;
        background: linear-gradient(135deg, #34d399, #06b6d4, #10b981);
        animation: pulse4K 2s infinite alternate;
        box-shadow: 0 0 30px rgba(52, 211, 153, 0.8);
    }

    @keyframes pulse4K {
        0% { transform: scale(0.96); box-shadow: 0 0 15px rgba(52, 211, 153, 0.4); }
        100% { transform: scale(1.04); box-shadow: 0 0 40px rgba(6, 182, 212, 1); }
    }

    .metric-card {
        background: rgba(6, 78, 59, 0.45);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 20px;
        padding: 22px;
        text-align: center;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .metric-card:hover {
        transform: translateY(-8px) scale(1.03);
        border-color: #34d399;
        box-shadow: 0 15px 45px rgba(52, 211, 153, 0.5), inset 0 0 15px rgba(52, 211, 153, 0.2);
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

    /* Primary Button Styling */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 40%, #06b6d4 100%) !important;
        background-size: 200% 200% !important;
        color: #ffffff !important;
        font-size: 19px !important;
        font-weight: 900 !important;
        border: 1px solid #34d399 !important;
        border-radius: 14px !important;
        padding: 16px 28px !important;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.7), 0 0 15px rgba(6, 182, 212, 0.6) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        cursor: pointer !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        animation: extremeGlow 3s ease infinite !important;
    }

    @keyframes extremeGlow {
        0% { background-position: 0% 50%; box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
        50% { background-position: 100% 50%; box-shadow: 0 0 45px rgba(6, 182, 212, 0.9); }
        100% { background-position: 0% 50%; box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-4px) scale(1.04) !important;
        box-shadow: 0 0 55px rgba(6, 182, 212, 1) !important;
        color: #ffffff !important;
    }

    /* Secondary Emergency Stop Button Styling */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #991b1b 100%) !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: 1px solid rgba(239, 68, 68, 0.8) !important;
        border-radius: 14px !important;
        padding: 16px 24px !important;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.7) !important;
        transition: all 0.3s ease !important;
        animation: pulseRedGlow 2.5s infinite alternate !important;
        cursor: pointer !important;
    }

    @keyframes pulseRedGlow {
        0% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.5); }
        100% { box-shadow: 0 0 35px rgba(239, 68, 68, 1); }
    }

    div.stButton > button[kind="secondary"]:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 0 45px rgba(239, 68, 68, 1) !important;
    }

    /* Upload Area Styling */
    [data-testid="stFileUploader"] section {
        background: rgba(6, 78, 59, 0.4) !important;
        border: 2px dashed #34d399 !important;
        border-radius: 18px !important;
        padding: 20px !important;
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

# 4. Updated Default Records Generator
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
        used_ail = random.randint(1, 10)
        used_ahpl = random.randint(1, 10)
        hand_ail = random.randint(5, 20)
        hand_ahpl = random.randint(5, 20)
        account_no = f"35{random.randint(1000000000, 9999999999)}"
        records.append({
            "Date": entry_dt.strftime("%Y-%m-%d"),
            "Party Name": party_name,
            "Account Number": account_no,
            "Email": f"{email_prefix}@clientdomain.com",
            "Place": random.choice(places),
            "Bank Name": random.choice(banks),
            "Number of cheque used in AIL": used_ail,
            "Number of cheque used In AHPL": used_ahpl,
            "Total cheque in hand AIL": hand_ail,
            "Total cheque in hand AHPL": hand_ahpl
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
        <div><span class="designer-badge">✨ ARCHITECT & DESIGNER: DHARMENDRA KUMAR (MISHRA) AND HIS SON</span></div>
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

# 8. Dispatch & Stop Control Buttons
col_start, col_stop = st.columns([2, 1])
with col_start: 
    start_btn = st.button("🚀 Launch Cheque Details Dispatch", type="primary", use_container_width=True)
with col_stop: 
    stop_btn = st.button("🛑 Emergency Stop", type="secondary", use_container_width=True)

if stop_btn: 
    st.session_state['stop_dispatch'] = True
    st.warning("🛑 Stop request received. Halting current process...")

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
                account_val = get_field_strict(row, ["Account Number", "Account No", "Account", "A/C No"], "N/A")
                target_email = get_field_strict(row, ["Email", "Email ID", "Mail", "Email Address"], "").strip()
                place_val = get_field_strict(row, ["Place", "City", "Location"], "N/A")
                bank_val = get_field_strict(row, ["Bank Name", "Bank"], "N/A")
                
                # Fetch Updated Columns
                used_ail = get_field_strict(row, ["Number of cheque used in AIL", "Used AIL", "AIL Used"], "0")
                used_ahpl = get_field_strict(row, ["Number of cheque used In AHPL", "Used AHPL", "AHPL Used"], "0")
                hand_ail = get_field_strict(row, ["Total cheque in hand AIL", "Hand AIL", "AIL Hand"], "0")
                hand_ahpl = get_field_strict(row, ["Total cheque in hand AHPL", "Hand AHPL", "AHPL Hand"], "0")

                if "@" in target_email:
                    msg = MIMEMultipart('alternative')
                    
                    custom_sender_name = "RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA"
                    msg['From'] = formataddr((custom_sender_name, sender_email.strip()))
                    
                    msg['To'] = target_email
                    msg['Subject'] = f"💳 Buffer Cheque Details - {party_name} ({rec_date})"

                    # 🎨 HTML EMAIL TEMPLATE WITH UPDATED FIELDS
                    body_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                    </head>
                    <body style="margin:0; padding:20px; background-color:#f4f6f8; font-family: 'Segoe UI', Arial, sans-serif;">
                      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; background-color: #064e3b; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                        
                        <!-- HEADER BOX -->
                        <tr>
                          <td style="padding: 24px; text-align: center;">
                            <div style="background-color: #34d399; border-radius: 12px; padding: 18px 10px; text-align: center;">
                              <h1 style="margin: 0; color: #022c22; font-size: 26px; font-weight: 900; letter-spacing: 1px; font-family: sans-serif;">
                                BUFFER CHEQUE DETAILS
                              </h1>
                              <div style="color: #064e3b; font-size: 13px; font-weight: 800; margin-top: 8px; letter-spacing: 1.5px; text-transform: uppercase;">
                                RAMA ENTERPRISES CFA, ABBOTT INDIA LTD, PATNA
                              </div>
                            </div>
                          </td>
                        </tr>

                        <!-- BODY CONTENT -->
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
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">🏷️ Number of cheque used in AIL</td>
                                <td style="color: #f87171; font-weight: bold; font-size: 14px;">{used_ail}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📦 Number of cheque used In AHPL</td>
                                <td style="color: #f87171; font-weight: bold; font-size: 14px;">{used_ahpl}</td>
                              </tr>
                              <tr style="border-bottom: 1px solid #065f46;">
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📊 Total cheque in hand AIL</td>
                                <td style="color: #fbbf24; font-weight: 900; font-size: 15px;">{hand_ail}</td>
                              </tr>
                              <tr>
                                <td style="color: #a7f3d0; font-weight: bold; font-size: 14px;">📈 Total cheque in hand AHPL</td>
                                <td style="color: #34d399; font-weight: 900; font-size: 15px;">{hand_ahpl}</td>
                              </tr>
                            </table>
                          </td>
                        </tr>

                        <!-- FOOTER -->
                        <tr>
                          <td style="background-color: #021a14; padding: 14px; text-align: center; color: #34d399; font-size: 12px; font-weight: bold; border-top: 1px solid #065f46;">
                            ⚡ DISPATCH ENGINE BY DHARMENDRA KUMAR (MISHRA) AND HIS SON
                          </td>
                        </tr>
                      </table>
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

st.markdown("<br><hr><div style='text-align: center; color: #34d399; font-weight: 700;'>⚡ Designed & Developed by Dharmendra Kumar (Mishra) and His Son</div>", unsafe_allow_html=True)
