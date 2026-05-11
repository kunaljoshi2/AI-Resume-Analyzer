from PyPDF2 import PdfReader


reader = PdfReader("test.pdf")
numberOfPages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

print(text)
