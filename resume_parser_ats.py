import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ## load oll the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Gemini Response
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-3.1-flash-lite-preview')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

##Prompt Template
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



##streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste your job description")
uploaded_file=st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        final_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(final_prompt)
        st.subheader(response)