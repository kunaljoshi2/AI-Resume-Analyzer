from PyPDF2 import PdfReader


def extractTextFromPdf(uploadedFile):
    reader = PdfReader(uploadedFile)
    numberOfPages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()

    return text

