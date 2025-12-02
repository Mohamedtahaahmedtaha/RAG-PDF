import base64
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

import fitz
import pdfplumber
import pandas as pd
import pytesseract
from PIL import Image, ImageFilter
import io
import re 

import arabic_reshaper
from bidi.algorithm import get_display

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

# Helper Functions

def is_arabic(text: str) -> bool:
    """
    Detect Arabic using extended Unicode ranges via regex.
    The ranges have been updated to include Arabic Presentation Forms 
    (FB50–FDFF and FE70–FEFF) to ensure the capture of text extracted from PDF.
    """
    if not text:
        return False
        
    arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    
    #Check any arabic letter 
    return bool(re.search(arabic_pattern, text))


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\u200f", "").replace("\u200e", "")
    return " ".join(text.split())


# PDF Extractor Class

class PDFExtractor:
    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        # final storage
        self.text_ar: List[str] = []
        self.text_en: List[str] = []
        self.tables: List[Any] = []
        self.images: List[Any] = []
        self.ocr_text: List[str] = []

    # Extract TEXT (AR + EN)
    def extract_text(self) -> None:
        logger.info("Extracting text...")
        doc = fitz.open(self.pdf_path)

        for page in doc:
            blocks = page.get_text("blocks")

            for block in blocks:
                if len(block) < 5:
                    continue

                raw = clean_text(block[4])
                if not raw:
                    continue

                # Detect Arabic
                if is_arabic(raw):
                    
                    raw_reversed_chars = raw[::-1] 
                    
                    reshaped = arabic_reshaper.reshape(raw_reversed_chars)
                    fixed = get_display(reshaped)
                    
                    self.text_ar.append(fixed)
                else:
                    self.text_en.append(raw)
        
        logger.info(f"Text extracted: {len(self.text_en)} EN | {len(self.text_ar)} AR")


    # Extract Tables
    def extract_tables(self):
        logger.info("Extracting tables...")

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                raw_tables = page.extract_tables()
                if not raw_tables:
                    continue

                for tbl in raw_tables:
                    df = pd.DataFrame(tbl).fillna("").astype(str)
                    self.tables.append(df.to_dict(orient="records"))

        logger.info(f"Tables extracted: {len(self.tables)}")

    # Extract Images + OCR
    def extract_images(self):
        logger.info("Extracting images + OCR...")
        doc = fitz.open(self.pdf_path)

        for page_idx, page in enumerate(doc):
            for img_idx, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                # fix color space
                if pix.n > 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                png = pix.tobytes("png")
                b64 = base64.b64encode(png).decode()

                # save image info
                self.images.append({
                    "page": page_idx + 1,
                    "index": img_idx + 1,
                    #"data_base64": b64 #
                })

                #  OCR Enhancement 
                try:
                    pil = Image.open(io.BytesIO(png))

                    # upscale
                    pil = pil.resize((pil.width * 3, pil.height * 3))

                    # convert to grayscale
                    pil = pil.convert("L")

                    # sharpen + threshold
                    pil = pil.filter(ImageFilter.SHARPEN) 
                    # pil = pil.point(lambda x: 255 if x > 150 else 0) 

                    # OCR on Arabic + English
                    text = pytesseract.image_to_string(
                        pil,
                        lang="eng+ara",
                        config="--oem 3 --psm 6"
                    )

                    text = clean_text(text)

                    if text.strip():
                        self.ocr_text.append(text)

                except Exception as e:
                    logger.warning(f"OCR failed for image {img_idx}: {e}")

        logger.info(f"OCR extracted: {len(self.ocr_text)} item(s)")

    # Extract Everything
    def extract_all(self) -> Dict[str, Any]:
        logger.info("Starting full extraction...")

        self.extract_text()
        self.extract_tables()
        self.extract_images()

        return {
            "source_pdf": self.pdf_path.name,
            "text": {
                "english": self.text_en,
                "arabic": self.text_ar,
            },
            "tables": self.tables,
            "images": self.images,
            "ocr": self.ocr_text
        }



# SAVE JSON
def save_json(data: Dict[str, Any], output_path="output.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Saved JSON → {output_path}")