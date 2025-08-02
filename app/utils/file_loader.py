import fitz
from PIL import Image
import io

def load_file_image(file_path):
    ext = file_path.lower().split(".")[-1] #file extension

    if ext == "pdf":
        doc = fitz.open(file_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes("png")))
        return image
    
    else:
        raise ValueError("Unsupported file type")
