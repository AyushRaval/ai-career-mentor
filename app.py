import streamlit as st
import sys
import json
import os
import cohere
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from resume_parser import parse_resume
from cohere_client import get_career_advice
from drive_upload import upload_to_drive
from insight_writer import save_insights_to_pdf

# Must be first Streamlit command in the script
st.set_page_config(page_title="AI Career Mentor", layout="wide")

st.write("Python executable:", sys.executable)
st.write("Python version:", sys.version)

st.title("🧠 AI Career Mentor")
st.markdown("Welcome to the AI Career Mentor! Upload your resume and get personalized career advice.")

# Retrieve API keys from Streamlit Secrets
try:
    cohere_api_key = st.secrets["cohere"]["api_key"]
except KeyError:
    st.error("🚨 COHERE_API_KEY not found in Streamlit Secrets.")
    st.stop()

# Initialize Cohere client
client = cohere.Client(cohere_api_key)

# Retrieve Google Service Account credentials
try:
    service_account_info = json.loads(st.secrets["google"]["gcp_service_account"])
    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    drive_service = build("drive", "v3", credentials=creds)
except KeyError:
    st.error("🚨 Google Service Account credentials missing in Streamlit Secrets.")
    st.stop()

uploaded_file = st.file_uploader("📄 Upload your resume (PDF format)", type=["pdf"])

if uploaded_file:
    # Parse resume
    text = parse_resume(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.write(text[:1000])  # Show first 1000 chars

    if st.button("Get Career Advice"):
        try:
            # Generate AI insights
            insights = get_career_advice(text)

            st.subheader("🧠 AI-Generated Career Insights")
            st.text_area("Career Advice", insights, height=300)

            # Save insights to a PDF
            insights_pdf_path = "resume_insights.pdf"
            save_insights_to_pdf(insights, filename=insights_pdf_path)

            # Upload resume to Drive
            resume_drive_link = upload_to_drive(uploaded_file)

            # Upload insights PDF to Drive
            with open(insights_pdf_path, "rb") as insight_file:
                insights_drive_link = upload_to_drive(insight_file, mimetype="application/pdf")

            # Show download links
            st.success(f"✅ Resume backed up to Drive: [View/Download Resume]({resume_drive_link})")
            st.success(f"📥 AI Career Insights: [View/Download PDF]({insights_drive_link})")

        except Exception as e:
            st.error(f"⚠️ Error processing career advice: {str(e)}")