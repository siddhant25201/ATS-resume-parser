import streamlit as st
import google.generativeai as genai
import os
import pdfplumber
import json

from dotenv import load_dotenv

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -------------------------------
# Gemini API Call
# -------------------------------
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "top_p": 1,
                "top_k": 1
            }
        )

        # Clean response (VERY IMPORTANT)
        cleaned_response = response.text.strip()
        cleaned_response = cleaned_response.replace("```json", "").replace("```", "").strip()

        return cleaned_response

    except Exception as e:
        return f"Error in API call: {str(e)}"


# -------------------------------
# Improved PDF Text Extraction
# -------------------------------
def input_pdf_text(uploaded_file):
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        text = f"Error reading PDF: {str(e)}"
    return text


# -------------------------------
# Prompt Template (FIXED)
# -------------------------------
input_prompt = """
You are an advanced ATS (Applicant Tracking System).

Follow these internal steps silently:
1. Extract key skills from Job Description
2. Extract skills from Resume
3. Compare semantically
4. Calculate match %
5. Identify missing keywords
6. Generate concise summary

STRICT RULES:
- Output ONLY valid JSON
- No explanation text
- Format exactly as:
{{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}

---

Example 1:
Resume: Python developer with Flask, SQL
JD: Django, REST API, AWS
Output:
{{"JD Match":"65%","MissingKeywords":["Django","REST API","AWS"],"Profile Summary":"Strong Python base but missing backend frameworks and cloud skills."}}

---

Example 2:
Resume: Excel, SQL, Power BI
JD: Python, ML, Tableau
Output:
{{"JD Match":"70%","MissingKeywords":["Python","Machine Learning","Tableau"],"Profile Summary":"Good analytics skills but lacks ML and advanced tools."}}

---

Now Evaluate:

Resume:
{text}

Job Description:
{jd}
"""


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Smart ATS", layout="centered")

st.title("📄 Smart ATS Resume Analyzer")
st.markdown("Upload your resume and compare it with a job description.")

jd = st.text_area("📌 Paste Job Description")

uploaded_file = st.file_uploader(
    "📎 Upload Resume (PDF only)",
    type="pdf"
)

submit = st.button("🚀 Analyze Resume")

# -------------------------------
# Main Logic
# -------------------------------
if submit:
    if uploaded_file is None or jd.strip() == "":
        st.warning("Please upload a resume and enter a job description.")
    else:
        with st.spinner("Analyzing..."):

            # Extract text
            resume_text = input_pdf_text(uploaded_file)

            # Create prompt
            final_prompt = input_prompt.format(
                text=resume_text,
                jd=jd
            )

            # Get response
            response = get_gemini_response(final_prompt)

            # Try parsing JSON
            try:
                parsed = json.loads(response)

                st.success("Analysis Complete ✅")

                st.metric("📊 JD Match", parsed.get("JD Match", "N/A"))

                st.subheader("❌ Missing Keywords")
                st.write(parsed.get("MissingKeywords", []))

                st.subheader("🧠 Profile Summary")
                st.write(parsed.get("Profile Summary", ""))

            except:
                st.error("⚠️ Failed to parse response. Raw output below:")
                st.code(response)