from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import io

# إنشاء PDF جديد
c = canvas.Canvas("test_image.pdf", pagesize=A4)
width, height = A4

# مسار الصورة
image_path = r"C:\Users\LENOVO\pdf\ocr.png"

# فتح الصورة وتحويلها لـ RGB
pil_img = Image.open(image_path).convert("RGB")

# إعادة تحجيم الصورة لو كبيرة
max_width, max_height = 300, 200
pil_img.thumbnail((max_width, max_height))

# تحويل الصورة لبايتات PDF
bio = io.BytesIO()
pil_img.save(bio, format="JPEG")
bio.seek(0)

# رسم الصورة في الـ PDF
c.drawImage(ImageReader(bio), 50, height - 250, width=max_width, height=max_height)

c.save()
print("PDF generated with image only.")
