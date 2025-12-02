# pdf_extractor/api.py
from pdf_extractor.extractor import PDFExtractor

def process_pdf(path):
    extractor = PDFExtractor(path)
    return extractor.extract_all()
