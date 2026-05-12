import streamlit as st
from utils.extractText import extractTextFromPdf

st.title("AI Resume Analyzer")
uploadedFile = st.file_uploader("Upload your resume here", type=["pdf"])


if uploadedFile:
    st.success(f"Uploaded: {uploadedFile.name}")

    extractedContent = extractTextFromPdf(uploadedFile)

else:
    st.error("File not uploaded...")

