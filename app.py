import streamlit as st

st.title("AI Resume Analyzer")
uploadedFile = st.file_uploader("Upload your resume here", type=["pdf"])


if uploadedFile:
    st.success(f"Uploaded: {uploadedFile.name}")