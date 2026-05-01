# 📄 Smart ATS Resume Analyzer (Gemini API + Python)

## 🎯 Project Overview
The **Smart ATS Resume Analyzer** is an AI-powered web application that evaluates resumes against job descriptions using the **Google Gemini API**. It simulates an Applicant Tracking System (ATS) by extracting skills, comparing them semantically, and generating actionable insights.

The project is implemented using **Streamlit** for the UI and leverages LLM-based analysis to provide:
- 📊 Match percentage  
- ❌ Missing keywords  
- 🧠 Profile summary  

---

## 🚀 Key Features
- 🔍 Semantic comparison between Resume & Job Description  
- 📊 ATS Match Score calculation  
- ❌ Identification of missing keywords  
- 🧠 AI-generated profile summary  
- 📄 PDF resume parsing  
- ⚡ Real-time analysis using Gemini API  

---

## 🔧 Prompt Engineering Concepts Used

### 🧠 Prompt Design Strategy
The system uses a **structured prompt template** to guide the LLM toward deterministic and machine-readable output.

---

### 🚀 Key Techniques Applied

#### 1. Instruction-Based Prompting
- Clearly defines the role:
  > “You are an advanced ATS (Applicant Tracking System)”
- Forces the model into a **domain-specific mindset**

---

#### 2. Step-by-Step Reasoning (Hidden Chain-of-Thought)
- The prompt internally enforces reasoning steps:
  - Extract skills from Job Description  
  - Extract skills from Resume  
  - Perform semantic comparison  
  - Calculate match %  
- Improves **consistency and accuracy** without exposing reasoning in output

---

#### 3. Strict Output Formatting (JSON Enforcement)
- Hard constraints:
  - Output must be valid JSON  
  - No extra explanation  
- Ensures **machine-readable responses** for downstream parsing

---

#### 4. Few-Shot Learning
- Includes multiple examples:
  - Resume vs Job Description comparisons  
  - Expected outputs  
- Helps the model understand:
  - Output structure  
  - Matching logic  
  - Keyword extraction patterns  

---

#### 5. Semantic Matching Guidance
- Prompt explicitly instructs:
  > “Compare semantically”
- Encourages:
  - Context-aware matching (e.g., *Flask ≈ Backend frameworks*)  
  - Not just keyword overlap  

---

#### 6. Deterministic Output Control
- Advanced version uses:
  - Low temperature (0.3)  
  - `top_k` and `top_p` tuning  
- Reduces randomness → improves **repeatability**

---

#### 7. Prompt Injection Safety (Basic Level)
- Restricting output format reduces:
  - Irrelevant text  
  - Model hallucinations  

---

#### 8. Response Post-Processing
- **Cleaning:**
  - Removes ```json blocks  
- **Parsing:**
  - Converts response → structured JSON  
- Ensures:
  - Robust integration with UI  

---

## 🧠 How It Works
1. Extract text from uploaded PDF resume  
2. Take job description as input  
3. Send structured prompt to Gemini API  
4. Perform:
   - Skill extraction  
   - Semantic matching  
   - Gap analysis  
5. Return structured JSON output:

```json
{
  "JD Match": "75%",
  "MissingKeywords": ["AWS", "Docker"],
  "Profile Summary": "Strong backend skills but lacks cloud exposure."
}

```
### 📂 Project Structure
```
├── resume_parser_ats.py      # Basic version
├── resume_parser_adv.py      # Advanced version
├── .env                      # API key storage
├── requirements.txt
└── README.md
```
### ⚙️ Tech Stack
Python  
Streamlit   
Google Gemini API   
PyPDF2 / pdfplumber     
JSON Parsing    
dotenv

### 🆚 Comparison: Basic vs Advanced Version
```
| Feature           | Basic Version (`resume_parser_ats.py`) | Advanced Version (`resume_parser_adv.py`)         |
| ----------------- | -------------------------------------- | ------------------------------------------------- |
| PDF Extraction    | Uses PyPDF2                            | Uses pdfplumber (more accurate & reliable)        |
| Error Handling    | Minimal                                | Robust exception handling                         |
| API Configuration | Default settings                       | Controlled generation (temperature, top_p, top_k) |
| Response Cleaning | Not handled                            | Cleans markdown/code block noise                  |
| JSON Parsing      | Not enforced                           | Strict parsing with validation                    |
| UI Design         | Simple                                 | Improved UI with metrics & icons                  |
| User Feedback     | Basic output                           | Structured display (metrics, sections)            |
| Reliability       | Prone to format issues                 | Production-ready behavior                         |
```
### 🔍 Key Improvements in Advanced Version
✅ Cleaner and structured JSON parsing  
✅ Better PDF text extraction (handles complex resumes)     
✅ Stable LLM output using controlled parameters        
✅ Improved UI/UX with metrics and visual feedback
✅ Error handling for real-world robustness     

### 📸 Output Preview
📊 JD Match Score displayed using st.metric     
❌ Missing keywords shown as a list     
🧠 Profile summary generated by AI  

#### resume_parser_ats output
![Output_1](https://github.com/user-attachments/assets/4b3a618e-ec55-4823-b625-daec4b2cd817)


#### resume_parser_adv output
![Output_2](https://github.com/user-attachments/assets/2b5a1016-4b78-45cc-821d-41d9281b0406)

### 🧩 Use Cases
Resume optimization for job applications    
ATS score estimation before applying    
Skill gap identification    
Career guidance insights    

### 📌 Future Enhancements
Multi-format resume support (DOCX, TXT)     
Skill visualization dashboard       
Resume rewriting suggestions    
Batch resume analysis   
Integration with job portals
