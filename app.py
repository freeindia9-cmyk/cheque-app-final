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

# ==============================================================================
# SECTION 1: GLOBAL SYSTEM PAGE CONFIGURATION & STATE INITIALIZATION
# ==============================================================================

st.set_page_config(
    page_title="8K Cyberpunk Cheque Dispatcher Engine Pro Ultra",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables for Persistent App Operations

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
    st.session_state['theme_color'] = "Electric Neon Cyan"

if 'show_inbox_popup' not in st.session_state:
    st.session_state['show_inbox_popup'] = False

if 'selected_record_for_popup' not in st.session_state:
    st.session_state['selected_record_for_popup'] = 0

if 'smtp_status' not in st.session_state:
    st.session_state['smtp_status'] = "Not Tested"

if 'column_mapping' not in st.session_state:
    st.session_state['column_mapping'] = {}

if 'custom_email_subject' not in st.session_state:
    st.session_state['custom_email_subject'] = "BUFFER CHEQUE DETAILS SUMMARY"

if 'custom_cfa_header' not in st.session_state:
    st.session_state['custom_cfa_header'] = "RAMA ENTERPRISES ABBOTT INDIA LTD CFA, PATNA"


# ==============================================================================
# SECTION 2: ADVANCED DYNAMIC ULTRA-GRAPHICS CSS & UI STYLING ENGINE
# ==============================================================================

def inject_custom_ultra_graphics_styles():
    """
    Injects high-definition cyberpunk CSS animations, glowing neon borders,
    popup modal styling, glassmorphism card components, dynamic overlay animation, and data grid overrides.
    """
    st.markdown("""
    <style>
        /* ---------------------------------------------------------------------- */
        /* GLOBAL BACKGROUND & GLASSMORPHISM CONTAINER STYLING                    */
        /* ---------------------------------------------------------------------- */
        
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: radial-gradient(circle at 50% 10%, #0a1128, #001f54, #03071e) !important;
            color: #e0e1dd !important;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        }

        /* ---------------------------------------------------------------------- */
        /* SIDEBAR CONTAINER AND COMPONENT STYLING                                */
        /* ---------------------------------------------------------------------- */
        
        section[data-testid="stSidebar"] {
            background-color: #03071e !important;
            border-right: 2px solid #00f5d4 !important;
            box-shadow: 8px 0 30px rgba(0, 245, 212, 0.3) !important;
        }

        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] h3 {
            color: #70e000 !important;
            font-weight: 800 !important;
            text-shadow: 0 0 10px rgba(112, 224, 0, 0.6) !important;
        }

        /* ---------------------------------------------------------------------- */
        /* HIGH VISIBILITY GLOWING HEADERS & TEXT ACCENTS                         */
        /* ---------------------------------------------------------------------- */
        
        h1, h2, h3, h4, h5, h6 {
            color: #00f5d4 !important;
            text-shadow: 0 0 15px rgba(0, 245, 212, 0.8) !important;
            font-weight: 900 !important;
            letter-spacing: 1px !important;
        }

        p, span, label {
            color: #e0e1dd !important;
        }

        /* ---------------------------------------------------------------------- */
        /* INPUT FIELD & FORM SELECTOR ULTRA STYLING                              */
        /* ---------------------------------------------------------------------- */
        
        input, select, textarea, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
            background-color: #0d1b2a !important;
            color: #00f5d4 !important;
            border: 2px solid #00b4d8 !important;
            border-radius: 12px !important;
            box-shadow: 0 0 18px rgba(0, 180, 216, 0.4) !important;
            font-weight: 700 !important;
            transition: all 0.4s ease-in-out !important;
        }

        input:focus, div[data-baseweb="input"]:focus-within {
            border-color: #70e000 !important;
            box-shadow: 0 0 30px rgba(112, 224, 0, 0.9) !important;
        }

        /* ---------------------------------------------------------------------- */
        /* DATA GRID TABLE ULTRA HIGH DEFINITION OVERRIDES                        */
        /* ---------------------------------------------------------------------- */
        
        div[data-testid="stDataFrame"] {
            background-color: #03071e !important;
            border: 2px solid #00f5d4 !important;
            border-radius: 16px !important;
            padding: 10px !important;
            box-shadow: 0 0 30px rgba(0, 245, 212, 0.7), inset 0 0 20px rgba(0, 245, 212, 0.3) !important;
        }

        div[data-testid="stDataFrame"] th, 
        div[data-testid="stDataFrame"] td,
        div[data-testid="stDataFrame"] [role="gridcell"] {
            background-color: #0d1b2a !important;
            color: #00f5d4 !important;
            font-family: 'Consolas', 'Courier New', monospace !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            border: 1px solid #00b4d8 !important;
            text-shadow: 0 0 8px rgba(0, 245, 212, 0.8) !important;
        }

        div[data-testid="stDataFrame"] tr:hover td {
            background-color: #1b263b !important;
            box-shadow: 0 0 12px rgba(0, 245, 212, 0.6) !important;
        }

        /* ---------------------------------------------------------------------- */
        /* FILE UPLOADER ULTRA GRAPHICS ZONE                                      */
        /* ---------------------------------------------------------------------- */
        
        [data-testid="stFileUploadDropzone"], div[data-testid="stFileUploader"] section {
            background: linear-gradient(135deg, #0d1b2a, #1b263b) !important;
            border: 2px dashed #00f5d4 !important;
            border-radius: 20px !important;
            box-shadow: 0 0 25px rgba(0, 245, 212, 0.4) !important;
            transition: all 0.5s ease-in-out !important;
        }

        [data-testid="stFileUploadDropzone"]:hover, div[data-testid="stFileUploader"] section:hover {
            border-color: #70e000 !important;
            box-shadow: 0 0 45px rgba(112, 224, 0, 0.8) !important;
        }

        [data-testid="stFileUploadDropzone"] button, div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
            color: #ffffff !important;
            border: 2px solid #70e000 !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            box-shadow: 0 0 20px rgba(0, 180, 216, 0.7) !important;
            transition: all 0.5s ease-in-out !important;
        }

        [data-testid="stFileUploadDropzone"] button:hover, div[data-testid="stFileUploader"] button:hover {
            transform: translateY(-3px) scale(1.03);
            background: linear-gradient(135deg, #70e000, #00f5d4) !important;
            color: #000000 !important;
            box-shadow: 0 0 35px rgba(112, 224, 0, 0.9) !important;
        }

        /* ---------------------------------------------------------------------- */
        /* MAIN HEADER ULTRA BRANDING CARD                                        */
        /* ---------------------------------------------------------------------- */
        
        .ultra-header-wrapper {
            margin-top: 10px !important;
            margin-bottom: 30px !important;
            background: rgba(13, 27, 42, 0.9);
            border: 3px solid #00f5d4;
            box-shadow: 0 0 50px rgba(0, 245, 212, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 30px;
            text-align: center;
        }

        .ultra-main-title {
            color: #00f5d4 !important;
            font-size: 42px;
            font-weight: 900;
            letter-spacing: 3px;
            margin: 0;
            text-shadow: 0 0 30px rgba(0, 245, 212, 0.9) !important;
        }

        .ultra-subtitle-badge {
            display: inline-block;
            background: #03071e;
            border: 2px solid #ffb703;
            padding: 8px 28px;
            border-radius: 30px;
            font-size: 15px;
            font-weight: 900;
            color: #ffb703 !important;
            margin-top: 15px;
            box-shadow: 0 0 20px rgba(255, 183, 3, 0.7);
        }

        /* ---------------------------------------------------------------------- */
        /* METRIC CARDS & GLASSMORPHISM CONTAINERS                                */
        /* ---------------------------------------------------------------------- */
        
        .metric-card-box {
            background: #0d1b2a !important;
            border: 2px solid #00b4d8;
            border-radius: 18px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 0 25px rgba(0, 180, 216, 0.4);
            transition: all 0.4s ease-in-out;
        }

        .metric-card-box:hover {
            transform: translateY(-6px);
            border-color: #00f5d4;
            box-shadow: 0 0 40px rgba(0, 245, 212, 0.8);
        }

        .metric-label {
            font-size: 13px;
            color: #90e0ef !important;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .metric-value-num {
            font-size: 38px;
            font-weight: 900;
            margin-top: 10px;
            color: #ffffff !important;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.9) !important;
        }

        /* ---------------------------------------------------------------------- */
        /* BUTTON STYLING AND HIGH VISIBILITY GLOW EFFECTS                        */
        /* ---------------------------------------------------------------------- */
        
        div.stButton > button, div.stDownloadButton > button {
            font-weight: 900 !important;
            border-radius: 16px !important;
            padding: 18px 26px !important;
            font-size: 16px !important;
            letter-spacing: 1.2px !important;
            transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1) !important;
            text-shadow: 0 0 12px rgba(255, 255, 255, 0.9) !important;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #00b4d8, #0077b6) !important;
            color: #ffffff !important;
            border: 2px solid #00f5d4 !important;
            box-shadow: 0 0 30px rgba(0, 245, 212, 0.7) !important;
            width: 100% !important;
        }

        div.stButton > button[kind="primary"]:hover {
            transform: translateY(-4px) scale(1.02);
            background: linear-gradient(135deg, #00f5d4, #70e000) !important;
            color: #000000 !important;
            box-shadow: 0 0 50px rgba(0, 245, 212, 1) !important;
        }

        div.stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #d90429, #ef233c) !important;
            color: #ffffff !important;
            border: 2px solid #ff4d6d !important;
            box-shadow: 0 0 30px rgba(239, 35, 60, 0.7) !important;
            width: 100% !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            transform: translateY(-4px) scale(1.02);
            background: linear-gradient(135deg, #ff4d6d, #b7094c) !important;
            box-shadow: 0 0 50px rgba(255, 77, 109, 1) !important;
        }

        div.stDownloadButton > button {
            background: linear-gradient(135deg, #3a0ca3, #4361ee) !important;
            color: #ffffff !important;
            border: 2px solid #4cc9f0 !important;
            box-shadow: 0 0 30px rgba(76, 201, 240, 0.7) !important;
            width: 100% !important;
        }

        div.stDownloadButton > button:hover {
            transform: translateY(-4px) scale(1.02);
            background: linear-gradient(135deg, #4cc9f0, #7209b7) !important;
            box-shadow: 0 0 50px rgba(76, 201, 240, 1) !important;
        }

        /* ---------------------------------------------------------------------- */
        /* SYSTEM TERMINAL CONSOLE LOG BOX                                        */
        /* ---------------------------------------------------------------------- */
        
        .log-box {
            background-color: #03071e;
            border: 2px solid #00b4d8;
            border-radius: 14px;
            padding: 18px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 13px;
            color: #00f5d4;
            box-shadow: inset 0 0 20px rgba(0, 180, 216, 0.4);
        }

        /* ---------------------------------------------------------------------- */
        /* BACKGROUND GLOW ANIMATION                                              */
        /* ---------------------------------------------------------------------- */
        
        @keyframes ultraBgGlow {
            0% { background-color: #0a1128 !important; }
            50% { background-color: #001f54 !important; }
            100% { background-color: #0a1128 !important; }
        }

        .stApp {
            animation: ultraBgGlow 7s infinite ease-in-out !important;
        }

        /* ---------------------------------------------------------------------- */
        /* FULL SELECTION POPUP MODAL STYLING                                     */
        /* ---------------------------------------------------------------------- */
        
        .popup-modal-overlay {
            background: linear-gradient(145deg, #03071e, #0d1b2a);
            border: 3px solid #00f5d4;
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 0 60px rgba(0, 245, 212, 0.6);
            margin-top: 25px;
            margin-bottom: 30px;
            position: relative;
        }

        .popup-modal-header {
            color: #00f5d4;
            font-size: 24px;
            font-weight: 900;
            border-bottom: 2px solid #00b4d8;
            padding-bottom: 12px;
            margin-bottom: 22px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_ultra_graphics_styles()


# ==============================================================================
# SECTION 3: UTILITY FUNCTIONS & DATA AUDIT ENGINES
# ==============================================================================

def get_field_strict(row, column_aliases, default_val="N/A"):
    """
    Extracts column values matching aliases regardless of case or spaces.
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
    Checks if an email string matches valid email format patterns.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email_str).strip()))


def perform_batch_data_audit(dataframe):
    """
    Audits the dataset for email validity, missing values, and data health.
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


def test_smtp_connection(host, port, user, password):
    """
    Tests SMTP connection health before starting bulk email dispatch.
    """
    try:
        server = smtplib.SMTP(host, int(port), timeout=5)
        server.starttls()
        if user and password:
            server.login(user.strip(), password.replace(" ", ""))
        server.quit()
        return True, "SMTP Connection Successful!"
    except Exception as e:
        return False, str(e)


# ==============================================================================
# SECTION 4: DEFAULT DATASET GENERATOR ENGINE
# ==============================================================================

@st.cache_data
def generate_default_100_records():
    """
    Generates 100 sample records for testing dispatch workflows.
    """
    parties = [
        "Aarav Sharma", "Priya Patel", "Rahul Verma", "Ananya Iyer", 
        "Amit Gupta", "Vikram Singh", "Neha Kapoor", "Sanjay Dutt",
        "Pooja Joshi", "Rajesh Kumar", "Meera Nair", "Deepak Chopra",
        "Karan Malhotra", "Rohan Mehta", "Simran Kaur", "Siddharth Rao"
    ]
    places = ["Patna", "Delhi", "Mumbai", "Kolkata", "Bangalore", "Ranchi", "Varanasi", "Ahmedabad", "Jaipur", "Lucknow"]
    banks = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Canara Bank", "Bank of Baroda"]
    
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


# ==============================================================================
# SECTION 5: SIDEBAR CONFIGURATION STUDIO
# ==============================================================================

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
    
    if st.button("🔌 Test SMTP Connection", use_container_width=True):
        if sender_email and app_password:
            is_ok, msg = test_smtp_connection(smtp_server, smtp_port, sender_email, app_password)
            if is_ok:
                st.sidebar.success(msg)
                st.session_state['smtp_status'] = "Connected"
            else:
                st.sidebar.error(f"Failed: {msg}")
                st.session_state['smtp_status'] = "Failed"
        else:
            st.sidebar.warning("Provide Email and App Password first!")

    st.divider()
    st.markdown("### 📝 Email Customization Studio")
    st.session_state['custom_email_subject'] = st.text_input(
        "Custom Email Subject Prefix", 
        value=st.session_state['custom_email_subject'], 
        key="sb_email_subject"
    )
    st.session_state['custom_cfa_header'] = st.text_input(
        "CFA Header Title", 
        value=st.session_state['custom_cfa_header'], 
        key="sb_cfa_title"
    )
    
    st.divider()
    st.markdown("### 🛠️ Data Management Tools")
    if st.button("🔄 Reset to Default 100 Sample Records", use_container_width=True):
        st.session_state['crm_data'] = generate_default_100_records()
        st.session_state['sent_count'] = 0
        st.session_state['failed_count'] = 0
        st.session_state['dispatch_logs'] = []
        st.rerun()


# ==============================================================================
# SECTION 6: MAIN APP HEADER BANNER
# ==============================================================================

st.markdown("""
<div class="ultra-header-wrapper">
    <h1 class="ultra-main-title">DHARMENDRA KUMAR (MISHRA)</h1>
    <span class="ultra-subtitle-badge">✨ ARCHITECT & DESIGNER: RAJVEER</span>
    <p style="color: #90e0ef; margin-top: 15px; font-weight: 800; font-size: 17px;">
        ⚡ 8K ULTRA-GRAPHICS CHEQUE DISPATCHER & AUTOMATED EMAIL MANAGEMENT ENGINE
    </p>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# SECTION 7: BATCH FILE IMPORT & DATA AUDIT
# ==============================================================================

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


# ==============================================================================
# SECTION 8: REAL-TIME METRICS & GRAPHICAL ANALYTICS DASHBOARD
# ==============================================================================

total_records = len(df) if df is not None else 0
sent_count = st.session_state['sent_count']
failed_count = st.session_state['failed_count']
pending_count = max(0, total_records - (sent_count + failed_count))

st.markdown("### 📊 Real-time Batch Metrics & Validation")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Total Records</div><div class="metric-value-num" style="color:#00f5d4 !important;">{total_records}</div></div>', unsafe_allow_html=True)

with col_m2:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Sent Success</div><div class="metric-value-num" style="color:#70e000 !important;">{sent_count}</div></div>', unsafe_allow_html=True)

with col_m3:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Failed / Invalid</div><div class="metric-value-num" style="color:#ff4d6d !important;">{failed_count}</div></div>', unsafe_allow_html=True)

with col_m4:
    st.markdown(f'<div class="metric-card-box"><div class="metric-label">Pending Dispatch</div><div class="metric-value-num" style="color:#ffb703 !important;">{pending_count}</div></div>', unsafe_allow_html=True)

# Analytics Visual Chart Tab
with st.expander("📈 Visual Analytics & Distribution Overview", expanded=False):
    if df is not None and not df.empty:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("##### Bank Distribution Analytics")
            bank_col = [c for c in df.columns if "bank" in c.lower()]
            if bank_col:
                bank_counts = df[bank_col[0]].value_counts()
                st.bar_chart(bank_counts)
            else:
                st.info("No bank column detected for chart.")

        with chart_col2:
            st.markdown("##### Dispatch Status Breakdown")
            status_df = pd.DataFrame({
                "Status": ["Sent", "Failed", "Pending"],
                "Count": [sent_count, failed_count, pending_count]
            }).set_index("Status")
            st.bar_chart(status_df)

with st.expander("🔍 System Data Audit & Health Report", expanded=False):
    for alert in st.session_state['validation_alerts']:
        st.write(alert)

st.markdown("---")


# ==============================================================================
# SECTION 9: INTERACTIVE DATA GRID & EDITING SUITE
# ==============================================================================

st.markdown("### ✏️ Interactive Data Grid & Dynamic Filters")

search_query = st.text_input("🔍 Quick Search Filter (Party Name, Email, or Bank)", placeholder="Type to filter records...")

if df is not None and not df.empty:
    if search_query:
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

display_df = filtered_df.drop(columns=["Record ID"], errors="ignore")
edited_df = st.data_editor(display_df, num_rows="dynamic", use_container_width=True)

st.session_state['crm_data'] = edited_df
filtered_df = st.session_state['crm_data']
df = st.session_state['crm_data']
st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 10: DISPATCH CONTROL ACTION PANEL & EXPORT OPTIONS
# ==============================================================================

st.markdown("### 🚀 Dispatch Control Actions & Data Exporters")
col_b1, col_b2, col_b3, col_b4 = st.columns([1.5, 1, 1, 1])

with col_b1:
    start_dispatch_btn = st.button("🚀 LAUNCH CHEQUE DISPATCH", type="primary", use_container_width=True)

with col_b2:
    stop_dispatch_btn = st.button("🛑 EMERGENCY STOP", type="secondary", use_container_width=True)

with col_b3:
    csv_buffer = io.StringIO()
    if df is not None:
        df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 EXPORT CSV",
        data=csv_buffer.getvalue(),
        file_name=f"Cheque_Dispatch_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_b4:
    json_buffer = io.StringIO()
    if df is not None:
        df.to_json(json_buffer, orient="records", indent=2)
    st.download_button(
        label="📄 EXPORT JSON",
        data=json_buffer.getvalue(),
        file_name=f"Cheque_Dispatch_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

if stop_dispatch_btn:
    st.session_state['stop_dispatch'] = True
    st.warning("🛑 Emergency Stop Triggered by User!")

st.markdown("---")


# ==============================================================================
# SECTION 11: HTML EMAIL TEMPLATE GENERATOR ENGINE (WITH NEON GLOW EFFECTS)
# ==============================================================================

def build_email_template(party, date_val, acc, place, bank, u_ail, u_ahpl, h_ail, h_ahpl, cfa_title, email_title):
    """
    Generates dynamic HTML email markup formatted for modern email clients,
    featuring glowing/un-glowing pulsing header animation, neon text shadows,
    and fully restored footer branding: RAMA ENTERPRISES ABBOTT INDIA LTD CFA, PATNA.
    """
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        /* Continuous Pulse/Glow Keyframes for Email Header */
        @keyframes headerPulseGlow {{
            0% {{
                box-shadow: 0 0 10px rgba(0, 245, 212, 0.4);
                border-color: #00b4d8;
                text-shadow: 0 0 5px rgba(0, 245, 212, 0.5);
            }}
            50% {{
                box-shadow: 0 0 35px rgba(0, 245, 212, 1), 0 0 15px rgba(112, 224, 0, 0.8);
                border-color: #00f5d4;
                text-shadow: 0 0 20px rgba(0, 245, 212, 1), 0 0 10px rgba(255, 255, 255, 0.9);
            }}
            100% {{
                box-shadow: 0 0 10px rgba(0, 245, 212, 0.4);
                border-color: #00b4d8;
                text-shadow: 0 0 5px rgba(0, 245, 212, 0.5);
            }}
        }}

        /* Fade-out Overlay Animation CSS */
        @keyframes fadeOutTransform {{
            0% {{
                opacity: 1;
                transform: scale(1);
                visibility: visible;
            }}
            75% {{
                opacity: 1;
                transform: scale(1);
            }}
            95% {{
                opacity: 0;
                transform: scale(0.92);
            }}
            100% {{
                opacity: 0;
                transform: scale(0.85);
                visibility: hidden;
                pointer-events: none;
            }}
        }}

        .fullscreen-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle at center, #0d1b2a, #03071e);
            z-index: 99999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            animation: fadeOutTransform 4s ease-in-out forwards;
            box-shadow: inset 0 0 100px rgba(0, 245, 212, 0.4);
        }}

        .overlay-popup-box {{
            background: #0b132b;
            border: 3px solid #00f5d4;
            border-radius: 20px;
            padding: 35px 50px;
            text-align: center;
            box-shadow: 0 0 50px rgba(0, 245, 212, 0.8);
        }}

        .overlay-title {{
            color: #00f5d4;
            font-size: 26px;
            font-weight: 900;
            margin-bottom: 15px;
            letter-spacing: 1px;
            text-shadow: 0 0 20px rgba(0, 245, 212, 0.9);
        }}

        .overlay-subtitle {{
            color: #ffb703;
            font-size: 18px;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-shadow: 0 0 12px rgba(255, 183, 3, 0.8);
        }}

        .email-top-header {{
            animation: headerPulseGlow 2.5s infinite ease-in-out;
            border: 2px solid #00f5d4;
        }}

        /* Neon Glowing Text Accents */
        .neon-glow-cyan {{
            color: #00f5d4 !important;
            text-shadow: 0 0 10px rgba(0, 245, 212, 0.8) !important;
        }}

        .neon-glow-blue {{
            color: #48cae4 !important;
            text-shadow: 0 0 10px rgba(72, 202, 228, 0.8) !important;
        }}

        .neon-glow-green {{
            color: #70e000 !important;
            text-shadow: 0 0 10px rgba(112, 224, 0, 0.8) !important;
        }}

        .neon-glow-white {{
            color: #ffffff !important;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.7) !important;
        }}
    </style>
</head>
<body style="margin:0; padding:20px; background-color:#03071e; font-family: 'Segoe UI', Arial, sans-serif;">

  <!-- 4-Second Full-Screen Fade-Out Overlay Pop-up -->
  <div class="fullscreen-overlay">
    <div class="overlay-popup-box">
      <div class="overlay-title">⚡ {str(email_title).upper()} ⚡</div>
      <div class="overlay-subtitle">RAMA ENTERPRISES ABBOTT INDIA LTD CFA, PATNA</div>
    </div>
  </div>

  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 640px; background-color: #0d1b2a; border-radius: 18px; overflow: hidden; border: 2px solid #00f5d4; box-shadow: 0 0 35px rgba(0, 245, 212, 0.4);">
    <tr>
      <td style="padding: 24px; text-align: center;">
        <div class="email-top-header" style="background: linear-gradient(135deg, #0d1b2a, #1b263b); border-radius: 14px; padding: 20px 12px; text-align: center;">
          <h1 class="neon-glow-cyan" style="margin: 0; font-size: 21px; font-weight: 900; letter-spacing: 1px;">
            RAMA ENTERPRISES ABBOTT INDIA LTD CFA, PATNA
          </h1>
          <div class="neon-glow-green" style="margin-top: 8px; font-size: 14px; font-weight: 800;">
            {str(email_title).upper()}
          </div>
        </div>
        <div class="neon-glow-blue" style="margin-top: 14px; font-weight: 800; font-size: 14px;">
          ✨ {str(cfa_title)}
        </div>
      </td>
    </tr>
    <tr>
      <td style="padding: 0 28px 28px 28px;">
        <p class="neon-glow-white" style="font-size: 16px; margin-bottom: 8px;">Dear <b class="neon-glow-cyan">{str(party)}</b>,</p>
        <p class="neon-glow-blue" style="font-size: 14px; margin-top: 0; margin-bottom: 22px;">Please find below the updated summary of your cheque records:</p>
        
        <table border="0" cellpadding="12" cellspacing="0" width="100%" style="border-collapse: collapse; background-color: #03071e; border-radius: 12px; border: 1px solid #00b4d8;">
          <tr style="border-bottom: 1px solid #1b263b;">
            <td width="50%" class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">📅 Date</td>
            <td width="50%" class="neon-glow-cyan" style="font-weight: bold; font-size: 14px;">{str(date_val)}</td>
          </tr>
          <tr style="border-bottom: 1px solid #1b263b;">
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">👤 Party Name</td>
            <td class="neon-glow-white" style="font-weight: bold; font-size: 14px;">{str(party)}</td>
          </tr>
          <tr style="border-bottom: 1px solid #1b263b;">
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">🔢 Account Number</td>
            <td class="neon-glow-green" style="font-weight: bold; font-size: 14px;">{str(acc)}</td>
          </tr>
          <tr style="border-bottom: 1px solid #1b263b;">
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">📍 Place</td>
            <td class="neon-glow-white" style="font-weight: bold; font-size: 14px;">{str(place)}</td>
          </tr>
          <tr style="border-bottom: 1px solid #1b263b;">
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">🏦 Bank Name</td>
            <td class="neon-glow-white" style="font-weight: bold; font-size: 14px;">{str(bank)}</td>
          </tr>
          <tr style="border-bottom: 1px solid #1b263b;">
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AIL</td>
            <td class="neon-glow-white" style="font-weight: bold; font-size: 14px;">{str(u_ail)}</td>
          </tr>
          <tr style="border-bottom: 1px solid #1b263b;">
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">🏷️ Cheques Used in AHPL</td>
            <td class="neon-glow-white" style="font-weight: bold; font-size: 14px;">{str(u_ahpl)}</td>
          </tr>
          <tr style="border-bottom: 1px solid #1b263b;">
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AIL</td>
            <td class="neon-glow-cyan" style="font-weight: bold; font-size: 14px;">{str(h_ail)}</td>
          </tr>
          <tr>
            <td class="neon-glow-blue" style="font-weight: bold; font-size: 14px;">📥 Total Cheque in Hand AHPL</td>
            <td class="neon-glow-cyan" style="font-weight: bold; font-size: 14px;">{str(h_ahpl)}</td>
          </tr>
        </table>
      </td>
    </tr>
    <!-- RESTORED FOOTER SECTION -->
    <tr>
      <td style="background-color: #03071e; padding: 22px; text-align: center; border-top: 2px solid #00f5d4;">
        <div class="neon-glow-cyan" style="font-weight: 900; font-size: 15px; letter-spacing: 1px;">
          RAMA ENTERPRISES ABBOTT INDIA LTD CFA, PATNA
        </div>
        <div class="neon-glow-blue" style="font-size: 12px; margin-top: 6px; font-weight: 700;">
          {str(cfa_title)}
        </div>
      </td>
    </tr>
  </table>
</body>
</html>"""
    return html_content


# ==============================================================================
# SECTION 12: RECORD SELECTION & FULL-SCREEN POPUP EMAIL PREVIEW ENGINE
# ==============================================================================

st.markdown("### 📩 Full-Selection Email Inbox Popup System")

pop_col1, pop_col2 = st.columns([1, 1])

with pop_col1:
    if st.button("👁️ TOGGLE LIVE SELECTION EMAIL POPUP MODAL", use_container_width=True):
        st.session_state['show_inbox_popup'] = not st.session_state['show_inbox_popup']

with pop_col2:
    if st.session_state['show_inbox_popup']:
        st.success("✨ Email Popup Window: ACTIVE")
    else:
        st.info("💡 Email Popup Window: COLLAPSED")

if st.session_state['show_inbox_popup']:
    st.markdown('<div class="popup-modal-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="popup-modal-header">📨 Interactive Email Popup Simulator</div>', unsafe_allow_html=True)
    
    if df is not None and not df.empty:
        party_list = df.apply(
            lambda r: f"{get_field_strict(r, ['Party Name', 'Party'], 'Unknown')} ({get_field_strict(r, ['Email', 'Email ID'], 'No Mail')})", 
            axis=1
        ).tolist()
        
        selected_index = st.selectbox(
            "🎯 Select Specific Party Record to Preview Email Popup Modal:", 
            options=range(len(party_list)), 
            format_func=lambda i: party_list[i],
            key="popup_record_selector"
        )
        
        sel_row = df.iloc[selected_index]
        
        p_name = get_field_strict(sel_row, ["Party Name", "Party"], "Valued Customer")
        p_date = get_field_strict(sel_row, ["Date", "Entry Date"], datetime.now().strftime("%Y-%m-%d"))
        p_acc = get_field_strict(sel_row, ["Account Number", "Account No"], "N/A")
        p_email = get_field_strict(sel_row, ["Email", "Email ID"], "N/A")
        p_place = get_field_strict(sel_row, ["Place", "City"], "N/A")
        p_bank = get_field_strict(sel_row, ["Bank Name", "Bank"], "N/A")
        p_u_ail = get_field_strict(sel_row, ["Number of cheque used in AIL"], "0")
        p_u_ahpl = get_field_strict(sel_row, ["Number of cheque used In AHPL"], "0")
        p_h_ail = get_field_strict(sel_row, ["Total cheque in hand AIL"], "0")
        p_h_ahpl = get_field_strict(sel_row, ["Total cheque in hand AHPL"], "0")

        preview_html = build_email_template(
            p_name, p_date, p_acc, p_place, p_bank,
            p_u_ail, p_u_ahpl, p_h_ail, p_h_ahpl,
            st.session_state['custom_cfa_header'], st.session_state['custom_email_subject']
        )
        
        st.markdown("#### 📱 Rendered Live Email Preview")
        st.components.v1.html(preview_html, height=480, scrolling=True)
    else:
        st.warning("No dataset loaded to preview emails.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ==============================================================================
# SECTION 13: AUTOMATED DISPATCH EXECUTION ENGINE
# ==============================================================================

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
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()
            server.login(sender_email.strip(), app_password.replace(" ", ""))

            for idx in range(len(df)):
                if st.session_state['stop_dispatch']:
                    st.warning("🛑 Dispatch process halted manually!")
                    st.session_state['dispatch_logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] STOP: Interrupted by user.")
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
                    msg['From'] = formataddr((st.session_state['custom_cfa_header'], sender_email.strip()))
                    msg['To'] = target_email
                    msg['Subject'] = f"{st.session_state['custom_email_subject']} - {party_name} ({rec_date})"

                    full_body = build_email_template(
                        party_name, rec_date, account_val, place_val, bank_val,
                        used_ail, used_ahpl, hand_ail, hand_ahpl, 
                        st.session_state['custom_cfa_header'], st.session_state['custom_email_subject']
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


# ==============================================================================
# SECTION 14: DISPATCH LOGS CONSOLE PANEL & AUDIT TRAIL
# ==============================================================================

if st.session_state['dispatch_logs']:
    st.markdown("### 📜 Dispatch Logs Console")
    st.markdown("<div class='log-box'>" + "<br>".join(st.session_state['dispatch_logs']) + "</div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 15: FOOTER SYSTEM INFORMATION & ARCHITECT CREDITS
# ==============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #90e0ef; padding: 22px; font-size: 14px;">
    ⚡ <b>DHARMENDRA KUMAR (MISHRA) BULK DISPATCHER ENGINE v4.0 PRO ULTRA</b><br>
    Designed & Built with Streamlit, Python & SMTP Services | Architect: <b>RAJVEER</b><br>
    <i>All rights reserved. Ready for high-performance enterprise deployments.</i>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# END OF FILE
# ==============================================================================
