import streamlit as st
from utils.extractText import extractTextFromPdf
from matcher import calculateMatchScores, extractKeywords
from downloadReport import downloadReport
from datetime import date, datetime


st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="centered"
)

st.markdown("""
    <style>

        h1 {
            font-weight: 800;
            letter-spacing: -0.5px;
            text-align: center;
        }
            
        [data-testid="stCaptionContainer"] p {
            text-align: center !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            border: 1.5px dashed var(--text-color);
            border-radius: 12px;
            background-color: var(--secondary-background-color);
            opacity: 0.9;
        }

        textarea {
            border-radius: 10px !important;
        }

        .stButton button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.2rem;
            transition: all 0.15s ease-in-out;
        }
        .stButton button:hover {
            border-color: #6EE7B7;
            color: #6EE7B7;
        }

        /*Download button*/
        .stDownloadButton button {
            border-radius: 10px;
            font-weight: 600;
        }
        .stDownloadButton button:hover {
            border-color: #6EE7B7;
            color: #6EE7B7;
        }

        [data-testid="stFileUploader"] label p,
        [data-testid="stTextArea"] label p {
            font-size: 12px !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            color: #6EE7B7 !important;
            margin-bottom: 4px !important;
        }


        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: var(--secondary-background-color) !important;
            border-left: 3px solid #6EE7B7 !important;
            border-radius: 14px !important;
            padding: 0.5rem 0.5rem !important;
        }

        .step-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 0.6rem;
        }
        .step-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 26px;
            height: 26px;
            min-width: 26px;
            border-radius: 50%;
            background-color: #6EE7B7;
            color: #0E1117;
            font-weight: 800;
            font-size: 13px;
        }
        .step-title {
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }

        .step-sub {
            font-size: 12px;
            color: var(--text-color);
            opacity: 0.6;
            margin: -4px 0 10px 36px;
        }

        .step-divider {
            height: 1px;
            background-color: var(--text-color);
            opacity: 0.12;
            margin: 1.2rem 0 1.2rem 0;
        }
    </style>
""", unsafe_allow_html=True)


#makes home page the default
if "page" not in st.session_state:
    st.session_state["page"] = "home"


if st.session_state.get("page") == "home":

    #home page
    st.title("AI Resume Analyzer")
    st.caption("Smart resume screening powered by AI")


    with st.container(border=True):

  
        st.markdown(
            '<div class="step-row"><div class="step-badge">1</div>'
            '<div class="step-title">Upload your resume</div></div>'
            '<div class="step-sub">PDF format, used to extract your skills and experience</div>',
            unsafe_allow_html=True
        )
        uploadedFile = st.file_uploader("Upload your resume here", type=["pdf"], label_visibility="collapsed")
        extractedContent = None


        if uploadedFile:
        
            try:
                st.toast(f"Uploaded: {uploadedFile.name}")
                extractedContent = extractTextFromPdf(uploadedFile)

            except Exception as e:
                st.error(f"Failed to extract text from PDF: {str(e)}")
                extractedContent = None

 
        st.markdown('<div class="step-divider"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="step-row"><div class="step-badge">2</div>'
            '<div class="step-title">Paste the job description</div></div>'
            '<div class="step-sub">Copy the full posting — we\'ll compare it against your resume</div>',
            unsafe_allow_html=True
        )
        jobDescription = st.text_area("Enter the job description:", label_visibility="collapsed", height=160)

        canAnalyze = extractedContent is not None and jobDescription and jobDescription.strip()


        st.write("")

        #analyze button
        if st.button("Analyze", disabled=not canAnalyze, use_container_width=True):
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
                    border: 1px solid #6EE7B7;
                    border-radius: 12px;
                    font-size: 18px;
                    font-weight: 600;
                    text-align: center;
                    background-color: transparent;
                    color: #6EE7B7;
                    padding: 0.6rem 1.4rem;
                }
                    
                .st-key-seeResultsButton button:hover {
                    background-color: #6EE7B7;
                    color: #0E1117;
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
                        background: linear-gradient(135deg, #1F9D55, #16A34A);
                        color: white;
                        border: none;
                        border-radius: 16px;
                        font-size: 26px;
                        text-align: center;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        padding: 0.4rem 0;
                        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.25);
                    }
                </style>
            """, unsafe_allow_html=True)

            with st.container(key="scoreSubheader"):
                st.subheader(f"Your match score is: {score}%")
                st.caption("*NOTE: matched scores above 40% indicate a strong keyword match")

            st.write("")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Matched Keywords:")
   
                pills = " ".join([
                    f"<span style='background-color: #14301F; color: #6EE7B7; padding: 6px 12px; "
                    f"border-radius: 999px; margin: 4px; display: inline-block; font-size: 14px; "
                    f"border: 1px solid #1F9D55;'>{word}</span>"
                    for word in matched
                ])
                st.markdown(pills, unsafe_allow_html=True)

            with col2:
                st.subheader("Missing Keywords:")
 
                pills = " ".join([
                    f"<span style='background-color: #332016; color: #FCA5A5; padding: 6px 12px; "
                    f"border-radius: 999px; margin: 4px; display: inline-block; font-size: 14px; "
                    f"border: 1px solid #7F1D1D;'>{word}</span>"
                    for word in missing
                ])
                st.markdown(pills, unsafe_allow_html=True)

 
            st.write("")
            st.write("")

            st.download_button(
                label="Download Report",
                data = downloadReport(score, missing, matched),
                file_name = "match_report.pdf",
                mime="application/pdf",
            )


    if not canAnalyze:
        if extractedContent is None:
            st.info("Upload a PDF resume to enable analysis.")

        elif not jobDescription or not jobDescription.strip():
            st.info("Enter a job description to enable analysis.")