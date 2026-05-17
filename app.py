import streamlit as st
from utils.extractText import extractTextFromPdf
import previousScans
from matcher import calculateMatchScores


#makes home page the default
if "page" not in st.session_state:
    st.session_state["page"] = "home"

#nav bar (sidebar)
with st.sidebar:
    st.title("Navigation")
    
    if st.button("Home", use_container_width=True):
        st.session_state["page"] = "home"

    if st.button("Previous Scans", use_container_width=True):
        st.session_state["page"] = "previousScans"

    st.divider()



if st.session_state.get("page") == "home":

    #home page
    st.title("AI Resume Analyzer")
    st.caption("Smart resume screening powered by AI")
    uploadedFile = st.file_uploader("Upload your resume here", type=["pdf"])
    extractedContent = None


    if uploadedFile:
    
        try:
            st.success(f"Uploaded: {uploadedFile.name}")
            extractedContent = extractTextFromPdf(uploadedFile)

        except Exception as e:
            st.error(f"Failed to extract text from PDF: {str(e)}")
            extractedContent = None

    jobDescription = st.text_area("Enter the job description:")

    canAnalyze = extractedContent is not None and jobDescription and jobDescription.strip()

    #analyze button
    if st.button("Analyze", disabled=not canAnalyze):
        with st.spinner("Analyzing..."):
            score = calculateMatchScores(extractedContent, jobDescription)
        st.success(f"Analysis complete! Your match score is: {score}%")

    if not canAnalyze:
        if extractedContent is None:
            st.info("Upload a PDF resume to enable analysis.")

        elif not jobDescription or not jobDescription.strip():
            st.info("Enter a job description to enable analysis.")


elif st.session_state.get("page") == "previousScans":

    previousScans.show()