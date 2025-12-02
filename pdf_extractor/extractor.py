import base64
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

import fitz
import pdfplumber
import pandas as pd
from langdetect import detect
import pytesseract
from PIL import Image
import io

import arabic_reshaper
from bidi.algorithm import get_display

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def is_arabic(text: str) -> bool:
    """Detect if text is Arabic."""
    if not text or not text.strip():
        return False
    try:
        return detect(text) == "ar"
    except Exception:
        return False


def clean_text(text: str) -> str:
    """Normalize and clean extracted text."""
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

        self.text_ar: List[str] = []
        self.text_en: List[str] = []
        self.tables: List[List[Dict[str, Any]]] = []
        self.images: List[Dict[str, Any]] = []
        self.ocr_text: List[str] = []


    def extract_text(self) -> None:
        """Extract Arabic/English text from PDF."""
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

                # Arabic reshaping
                if is_arabic(raw):
                    reshaped = arabic_reshaper.reshape(raw)
                    fixed = get_display(reshaped)
                    self.text_ar.append(fixed)
                else:
                    self.text_en.append(raw)

        logger.info(f"Text extracted: {len(self.text_ar)} AR | {len(self.text_en)} EN")


    def extract_tables(self) -> None:
        """Extract tables using pdfplumber."""
        logger.info("Extracting tables...")

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                try:
                    tables = page.extract_tables()
                except Exception:
                    continue

                for tbl in tables:
                    df = pd.DataFrame(tbl).fillna("").astype(str)
                    self.tables.append(df.to_dict(orient="records"))

        logger.info(f"Tables extracted: {len(self.tables)}")


    def extract_images(self) -> None:
        """Extract images and run OCR on them."""
        logger.info("Extracting images and running OCR...")
        doc = fitz.open(self.pdf_path)

        for page_idx, page in enumerate(doc):
            for img_idx, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                if pix.n > 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                png_bytes = pix.tobytes("png")
                b64 = base64.b64encode(png_bytes).decode("utf-8")

                self.images.append({
                    "page": page_idx + 1,
                    "index": img_idx + 1,
                    "data_base64": b64,
                })

                # OCR Enhancements
                try:
                    # Load and prepare image
                    img_pil = Image.open(io.BytesIO(png_bytes)).convert("RGB")

                    # High-quality preprocessing
                    img_pil = img_pil.resize((img_pil.width * 3, img_pil.height * 3))
                    img_pil = img_pil.convert("L")
                    img_pil = img_pil.filter(Image.Filter.SMOOTH_MORE)
                    img_pil = img_pil.point(lambda x: 255 if x > 160 else 0)

                    # OCR (Arabic + English)
                    custom_config = "--oem 3 --psm 6"
                    text = pytesseract.image_to_string(img_pil, lang="eng+ara", config=custom_config)

                    cleaned = clean_text(text)


                    if cleaned:
                        self.ocr_text.append(cleaned)

                except Exception as e:
                    logger.warning(f"OCR failed for image p{page_idx+1}_i{img_idx+1}: {e}")

        logger.info(f"OCR texts extracted: {len(self.ocr_text)}")


    def extract_all(self) -> Dict[str, Any]:
        """Run full extraction sequence."""
        logger.info(f"Starting full PDF extraction: {self.pdf_path.name}")

        self.extract_text()
        self.extract_tables()
        self.extract_images()

        # Show OCR for debugging
        print("\n OCR TEXT:")
        for line in self.ocr_text:
            print("-", line)

        return {
            "source_pdf": self.pdf_path.name,
            "text": {
                "arabic": self.text_ar,
                "english": self.text_en,
            },
            "tables": self.tables,
            "images": self.images,
            "ocr": self.ocr_text
        }


# Save JSON

def save_json(data: Dict[str, Any], output_path: str = "output.json") -> None:
    """Save JSON output."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info(f"Saved JSON → {output_path}")
