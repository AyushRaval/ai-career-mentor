import cohere
import os
from dotenv import load_dotenv

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

# Check if the API key is present
if not cohere_api_key:
    raise ValueError("❌ COHERE_API_KEY not found in environment variables.")

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
