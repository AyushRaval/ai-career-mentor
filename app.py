import streamlit as st
import sys
from resume_parser import parse_resume
from cohere_client import get_career_advice
from drive_upload import upload_to_drive
from insight_writer import save_insights_to_pdf
import os
from dotenv import load_dotenv

load_dotenv()

# Must be first Streamlit command in the script
st.set_page_config(page_title="AI Career Mentor", layout="wide")

st.write("Python executable:", sys.executable)
st.write("Python version:", sys.version)

st.title("🧠 AI Career Mentor")
st.markdown("Welcome to the AI Career Mentor! Upload your resume and get personalized career advice.")

uploaded_file = st.file_uploader("📄 Upload your resume (PDF format)", type=["pdf"])

if uploaded_file:
    # Parse resume
    text = parse_resume(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.write(text[:1000])  # Show first 1000 chars

    if st.button("Get Career Advice"):
        # Generate AI insights
        insights = get_career_advice(text)

        st.subheader("🧠 AI-Generated Career Insights")
        st.text_area("Career Advice", insights, height=300)

        # Save insights to a PDF
        insights_pdf_path = "resume_insights.pdf"
        save_insights_to_pdf(insights, filename=insights_pdf_path)

        # Upload resume to Drive (Streamlit file has .type)
        resume_drive_link = upload_to_drive(uploaded_file)

        # Upload insights PDF to Drive (regular file, no .type, so specify MIME)
        with open(insights_pdf_path, "rb") as insight_file:
            insights_drive_link = upload_to_drive(insight_file, mimetype="application/pdf")

        # Show download links
        st.success(f"✅ Resume backed up to Drive: [View/Download Resume]({resume_drive_link})")
        st.success(f"📥 AI Career Insights: [View/Download PDF]({insights_drive_link})")
