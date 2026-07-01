# AI Resume Analyzer

An AI-powered web app that analyzes your resume against a job description, giving you a match score and actionable keyword feedback.

## Link

https://ai-resume-analyzer-kj.streamlit.app/

## Features

- Upload your resume as a PDF and paste a job description
- Get a match score based on TF-IDF vectorization and cosine similarity
- See matched and missing keywords side by side
- Download a PDF report of your analysis
- Track previous scans and monitor improvement over time

## Tech Stack

- Python, Streamlit
- Scikit-learn (TF-IDF, cosine similarity)
- SpaCy (lemmatization)
- pdfplumber (PDF text extraction)
- fpdf2 (PDF report generation)

## Setup

```bash
pip install streamlit scikit-learn spacy pdfplumber fpdf2
python -m spacy download en_core_web_sm
streamlit run app.py
```

## Usage

1. Upload your resume PDF
2. Paste the job description
3. Click Analyze
4. View your match score and keyword breakdown
5. Download the PDF report