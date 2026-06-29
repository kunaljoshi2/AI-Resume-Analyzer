import pdfplumber

def extractTextFromPdf(uploadedFile):
    text = ""
    with pdfplumber.open(uploadedFile) as pdf:
        for page in pdf.pages:
            pageText = page.extract_text()
            if pageText:
                text += pageText + "\n"
    return text
