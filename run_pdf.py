from pdf_extractor.extractor import PDFExtractor, save_json
import os

PDF_PATH = r"C:\Users\LENOVO\pdf\my_pdf.pdf"   # ملف PDF
OUTPUT_JSON = "output.json"

print("🔍 Starting extraction...")

extractor = PDFExtractor(PDF_PATH)
data = extractor.extract_all()

save_json(data, OUTPUT_JSON)

print("✅ Done! JSON saved:", OUTPUT_JSON)