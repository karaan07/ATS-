import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

input_prompt = """
Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. 

Your task is to evaluate the resume based on the given job description (JD). 

You must consider that the job market is very competitive, and you should provide the best assistance for improving the resumes. Assign the percentage match based on the JD and identify the missing keywords with high accuracy.

Resume: {text}

Job Description: {id}

I want the response in a single string with the structure:

{{"JD Match": "%", "MissingKeywords": (), "Profile Summary": ""}}
"""

st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste your Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please Upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, id=jd))
        st.subheader(response)