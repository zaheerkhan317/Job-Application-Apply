import streamlit as st
import os
import base64
from email_sender import EmailSender

# Ensure attachments folder
os.makedirs("attachments", exist_ok=True)

# Handle secrets if provided (for Streamlit Cloud deployment)
if "CREDENTIALS_JSON" in st.secrets:
    with open("credentials.json", "w", encoding="utf-8") as f:
        f.write(st.secrets["CREDENTIALS_JSON"])

if "TOKEN_PICKLE_B64" in st.secrets and not os.path.exists("token.pickle"):
    try:
        token_b64 = st.secrets["TOKEN_PICKLE_B64"]
        token_bytes = base64.b64decode(token_b64.encode("utf-8"))
        with open("token.pickle", "wb") as f:
            f.write(token_bytes)
    except Exception as e:
        st.warning("Failed to write token.pickle from secrets: " + str(e))

st.set_page_config(page_title="Job Application Sender", layout="centered")
st.title("📧 Automated Job Application Sender")

# Initialize state variables for form fields
if "hr_email" not in st.session_state:
    st.session_state.hr_email = ""
if "position" not in st.session_state:
    st.session_state.position = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

st.markdown("Enter the HR email, position, and job description, then click **Send Application**.")

with st.form("apply_form", clear_on_submit=True):
    hr_email = st.text_input("HR Email Address", value=st.session_state.hr_email, placeholder="hr@company.com")
    position = st.text_input("Position / Job Title", value=st.session_state.position, placeholder="Java Developer")
    job_description = st.text_area("Job Description (paste here)", value=st.session_state.job_description, height=200)
    submit = st.form_submit_button("Send Application")

if submit:
    if not hr_email or not job_description:
        st.error("Please fill HR email and job description.")
    else:
        email_sender = EmailSender()  # Uses default resume from email_sender.py
        with st.spinner("Sending email..."):
            success, message = email_sender.send_job_application(hr_email, job_description, position)
        if success:
            st.success(message)
            # Clear session state so fields reset
            st.session_state.hr_email = ""
            st.session_state.position = ""
            st.session_state.job_description = ""
        else:
            st.error(message)
