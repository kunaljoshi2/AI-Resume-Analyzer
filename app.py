import streamlit as st

st.title("AI Resume Analyzer")
uploadedFile = st.file_uploader("Enter your resume here", type=["pdf"])


if uploadedFile:
    st.success(f"Uploaded: {uploadedFile.name}")