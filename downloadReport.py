from fpdf import FPDF
from matcher import calculateMatchScores, extractKeywords
from datetime import date
from datetime import datetime as dt



def downloadReport(matchScore, missingKeywords, matchedKeywords):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", size=20)

    timeStamp = dt.now().strftime("%Y-%m-%d %H:%M")
    titleText = "Resume Match Report"

    pdf.cell(0, 10, titleText, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)

    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, f"Datetime: {timeStamp}", new_x="LMARGIN", new_y="NEXT", align="L")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Match Score: {matchScore}%", 0, ln=True)
    pdf.ln(4)

    #matched keywords section
    pdf.set_font("Helvetica", "B", size=12)
    pdf.cell(0, 10, "Matched Keywords:", 0, ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 8, ", ".join(matchedKeywords))
    pdf.ln(2)

    #missing keywords section
    pdf.set_font("Helvetica", "B", size=12)
    pdf.cell(0, 10, "Missing Keywords:", 0, ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 8, ", ".join(missingKeywords))


    return bytes(pdf.output())