import streamlit as st
import cohere

# Retrieve API key from Streamlit Secrets
try:
    cohere_api_key = st.secrets["cohere"]["api_key"]
except KeyError:
    st.error("🚨 COHERE_API_KEY not found in Streamlit Secrets.")
    st.stop()

# Initialize Cohere client
client = cohere.Client(cohere_api_key)

def get_career_advice(resume_text):
    prompt = f"""
    You are an expert AI Career Coach. Analyze the resume provided below and return a detailed, actionable response with the following:

    1. **Skill Gap Analysis**  
    2. **Suggested Career Roles**  
    3. **Free Learning Resources**  
    4. **A Personalized Career Development Roadmap**

    Resume:
    \"\"\"
    {resume_text}
    \"\"\"
    """
    try:
        response = client.chat(
            message=prompt,
            model="command-r-plus",
            temperature=0.7,
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error generating career advice: {str(e)}"