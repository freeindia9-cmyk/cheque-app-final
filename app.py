import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Cheque Record Management System",
    page_icon="💳",
    layout="wide"
)

# Custom Cyberpunk Emerald Gradient CSS
st.markdown("""
<style>
    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #022c22 0%, #064e3b 50%, #022c22 100%);
        color: #ecfdf5;
    }
    
    /* Input Fields Styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {
        background-color: #065f46 !important;
        color: #ecfdf5 !important;
        border: 1px solid #34d399 !important;
        border-radius: 8px !important;
    }
    
    /* Dynamic Glow Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #059669, #10b981) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.4);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(52, 211, 153, 0.8);
        transform: translateY(-2px);
    }
    
    /* Header Styling */
    .main-title {
        font-family: 'Montserrat', sans-serif;
        text-align: center;
        background: linear-gradient(90deg, #34d399, #10b981, #6ee7b7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 20px;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #34d399;
        font-size: 0.9rem;
        border-top: 1px solid #065f46;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<h1 class="main-title">💳 Cheque Record Management System</h1>', unsafe_allow_html=True)

# Excel Data Storage Setup
DATA_FILE = "cheque_records.xlsx"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "Date", "Party Name", "Place", "Bank Name", 
        "Used Cheques", "Unused Cheques", "Total Cheques", "Email"
    ])
    df_init.to_excel(DATA_FILE, index=False)

# Form Section
st.subheader("📝 Record Entry & Email Dispatch")

with st.form("cheque_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        rec_date = st.date_input("Date", datetime.today())
        party_name = st.text_input("Party Name*")
        place_val = st.text_input("Place")
        bank_val = st.text_input("Bank Name")
        
    with col2:
        used_cheques = st.number_input("Number of Cheques Used", min_value=0, step=1)
        unused_cheques = st.number_input("Unused Cheques", min_value=0, step=1)
        total_cheques = used_cheques + unused_cheques
        st.markdown(f"**Total Cheques:** `{total_cheques}`")
        party_email = st.text_input("Party Email (Optional for Dispatch)")

    # Email Settings (Expandable)
    with st.expander("⚙️ Email Configuration (SMTP Details)"):
        sender_email = st.text_input("Sender Email", value="freeindia9cmyk@gmail.com")
        sender_password = st.text_input("App Password", type="password")

    submit_btn = st.form_submit_button("Save & Dispatch Record 🚀")

# Form Submission Logic
if submit_btn:
    if not party_name:
        st.error("Please enter the Party Name!")
    else:
        # Save to Excel
        new_data = {
            "Date": str(rec_date),
            "Party Name": party_name,
            "Place": place_val,
            "Bank Name": bank_val,
            "Used Cheques": used_cheques,
            "Unused Cheques": unused_cheques,
            "Total Cheques": total_cheques,
            "Email": party_email
        }
        
        df_existing = pd.read_excel(DATA_FILE)
        df_updated = pd.concat([df_existing, pd.DataFrame([new_data])], ignore_index=True)
        df_updated.to_excel(DATA_FILE, index=False)
        st.success("✅ Record successfully saved to Excel database!")

        # Send Email if Email ID is provided
        if party_email and sender_password:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f"💳 Buffer Cheque Details - {party_name} ({rec_date})"
                msg['From'] = sender_email
                msg['To'] = party_email

                # HTML Email Template with "BUFFER CHEQUE DETAILS" Header
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
                        <tr><td class="label-col">📅 Date</td><td class="value-col">{rec_date}</td></tr>
                        <tr><td class="label-col">👤 Party Name</td><td class="value-col" style="color: #6ee7b7;">{party_name}</td></tr>
                        <tr><td class="label-col">📍 Place</td><td class="value-col">{place_val}</td></tr>
                        <tr><td class="label-col">🏦 Bank Name</td><td class="value-col" style="color: #38bdf8;">{bank_val}</td></tr>
                        <tr><td class="label-col">🏷️ Number of Cheque Used</td><td class="value-col">{used_cheques}</td></tr>
                        <tr><td class="label-col">📦 Unused Cheque</td><td class="value-col">{unused_cheques}</td></tr>
                        <tr><td class="label-col">📊 Total Cheque</td><td class="value-col highlight-val">{total_cheques}</td></tr>
                      </table>
                      <p style="margin-top: 25px; color: #a7f3d0; font-size: 13px; letter-spacing: 0.5px;">Thank you for your business!</p>
                    </div>
                    <div class="footer-note">⚡ Designed & Developed by Dharmendra Kumar (Mishra)</div>
                  </div>
                </body>
                </html>
                """

                msg.attach(MIMEText(body_html, 'html'))

                # Connect to Gmail SMTP Server
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, party_email, msg.as_string())
                server.quit()

                st.success(f"📧 Email successfully dispatched to {party_email}!")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")

# View Saved Records Table
st.markdown("---")
st.subheader("📊 Saved Records Database")
if os.path.exists(DATA_FILE):
    df_display = pd.read_excel(DATA_FILE)
    st.dataframe(df_display, use_container_width=True)

# Footer Sign-off
st.markdown("""
<div class="footer">
    ⚡ Designed & Developed by <b>Dharmendra Kumar (Mishra)</b>
</div>
""", unsafe_allow_html=True)
