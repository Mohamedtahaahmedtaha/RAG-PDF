#pip install langchain_community openai langchain langchain-openai fastapi fitz faiss-cpu 
# pymupdf pdfplumber pytesseract pandas langdetect python-bidi pillow reportlab logging arabic_reshaper
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pathlib import Path
import logging
from PIL import Image
import io
import arabic_reshaper
from bidi.algorithm import get_display

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def generate_custom_pdf(
    output_path="custom_sample.pdf",
    english_paragraph="This is a long English paragraph for testing extraction from PDF. " * 5,
    arabic_paragraph="هذا نص عربي طويل للاختبار. " * 5,
    table_data=None,
    image_path=None,
    arabic_font_path="C:/Users/LENOVO/pdf/pdf_extractor/fonts/Amiri-Bold.ttf"
):
    """
    Generates a PDF document containing properly formatted Arabic text, English text, 
    a structured table, and an optional image (for testing purposes).
    """
    if table_data is None:
        table_data = [
            ["Name", "Country", "Score"],
            ["Mohamed", "Egypt", "92"],
            ["Taha", "UAE", "88"],
            ["Sara", "Saudi Arabia", "95"],
            ["Ali", "Kuwait", "89"],
        ]

    output_path = Path(output_path)
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    y = height - 50

    # Register Arabic font
    pdfmetrics.registerFont(TTFont("Amiri", arabic_font_path)) 

    # English paragraph
    c.setFont("Helvetica", 12)
    text_obj = c.beginText(50, y)
    for line in english_paragraph.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)
    y -= 100

    # Arabic paragraph
    c.setFont("Amiri", 12)
    arabic_lines = arabic_paragraph.split("\n")
    for line in arabic_lines:
        reshaped_text = arabic_reshaper.reshape(line)
        bidi_text = get_display(reshaped_text)
        c.drawRightString(width - 50, y, bidi_text)
        y -= 18
    y -= 20

    # Table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Sample Table:")
    x, y_table = 50, y - 25
    cell_width, cell_height = 150, 25
    for row in table_data:
        for col, cell in enumerate(row):
            c.rect(x + col * cell_width, y_table, cell_width, cell_height)
            c.drawString(x + col * cell_width + 5, y_table + 7, str(cell))
        y_table -= cell_height
    y = y_table - 20

    # User image (JPG/PNG)
    if image_path:
        img_path = Path(image_path)
        if img_path.exists():
            try:
                pil_img = Image.open(img_path).convert("RGB")

                #Resize
                max_width, max_height = 300, 200
                pil_img.thumbnail((max_width, max_height))

                bio = io.BytesIO()
                pil_img.save(bio, format="JPEG")
                bio.seek(0)

                # Axis
                draw_y = y - max_height
                if draw_y < 50:  # If you reach the end of the page create a new one
                    c.showPage()
                    draw_y = A4[1] - 50  # start from top page

                c.drawImage(ImageReader(bio), 50, draw_y, width=max_width, height=max_height)
            except Exception as e:
                logger.error("Error adding image: %s", e)
        else:
            logger.warning("Image path does not exist: %s", image_path)

    c.save()
    logger.info("Generated custom PDF at: %s", output_path)
    return str(output_path)