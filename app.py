import streamlit as st
from utils.extractText import extractTextFromPdf
import previousScans
from matcher import calculateMatchScores, extractKeywords


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
            st.toast(f"Uploaded: {uploadedFile.name}")
            extractedContent = extractTextFromPdf(uploadedFile)

        except Exception as e:
            st.error(f"Failed to extract text from PDF: {str(e)}")
            extractedContent = None

    jobDescription = st.text_area("Enter the job description:")

    canAnalyze = extractedContent is not None and jobDescription and jobDescription.strip()

    #analyze button
    if st.button("Analyze", disabled=not canAnalyze):
        with st.spinner("Analyzing..."):
            st.session_state["score"] = calculateMatchScores(extractedContent, jobDescription)
            st.session_state["matched"], st.session_state["missing"] = extractKeywords(extractedContent, jobDescription)
            st.session_state["analyzed"] = True
            st.session_state["showResults"] = False

        st.success(f"Analysis complete!")

    if st.session_state.get("analyzed"):

        st.markdown("""
            <style>
                .st-key-seeResultsButton button{
                    border: 3px solid black;
                    border-radius: 15px;
                    font-size: 20px;
                    text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)

        if not st.session_state.get("showResults"):
            if st.button("See Results", key="seeResultsButton"):
                st.session_state["showResults"] = True 
                st.rerun()

        if st.session_state.get("showResults"):
            score = st.session_state.get("score")
            matched = st.session_state.get("matched")
            missing = st.session_state.get("missing")

            st.markdown("""
                <style>
                    .st-key-scoreSubheader h3 {
                        background-color: green;
                        color: white;
                        border: 3px solid black;
                        border-radius: 15px;
                        font-size: 30px;
                        text-align: center;
                        text-transform: uppercase;
                    }
                </style>
            """, unsafe_allow_html=True)

            with st.container(key="scoreSubheader"):
                st.subheader(f"Your match score is: {score}%")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Matched Keywords:")
                pills = " ".join([f"<span style='background-color: white; color: black; padding: 6px 10px; border-radius: 10px; margin: 4px; display: inline-block'>{word}</span>" for word in matched])
                st.markdown(pills, unsafe_allow_html=True)

            with col2:
                st.subheader("Missing Keywords:")
                pills = " ".join([f"<span style='background-color: white; color: black; padding: 6px 10px; border-radius: 10px; margin: 4px; display: inline-block'>{word}</span>" for word in missing])
                st.markdown(pills, unsafe_allow_html=True)


    if not canAnalyze:
        if extractedContent is None:
            st.info("Upload a PDF resume to enable analysis.")

        elif not jobDescription or not jobDescription.strip():
            st.info("Enter a job description to enable analysis.")


elif st.session_state.get("page") == "previousScans":

    previousScans.show()