from pdf_extractor.extractor import PDFExtractor

pdf = "my_pdf.pdf" 

e = PDFExtractor(pdf)
data = e.extract_all()

print("\n OCR TEXTS")
print(data.get("ocr", []))

print("\n ENGLISH TEXT")
print(data.get("text", {}).get("english", []))

print("\n ARABIC TEXT ")
print(data.get("text", {}).get("arabic", []))

print("\n TABLES ")
print(data.get("tables", []))

print("\n IMAGES COUNT ")
print(len(data.get("images", [])))
