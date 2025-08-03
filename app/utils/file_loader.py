import fitz
from PIL import Image
import io
import cv2
import numpy as np
import re 

def load_file_image(file_path, zoom_x=4.0, zoom_y=4.0):
    '''
    This function takes the path to the pdf and returns a cv image.

    This function has scalability in case the are .docs, .txt, etc.
    '''
    ext = file_path.lower().split(".")[-1] #takes .pdf, .docs, etc

    if ext == "pdf":
        doc = fitz.open(file_path)
        page = doc.load_page(0) #First page of the pdf 

        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)

        image = Image.open(io.BytesIO(pix.tobytes("png"))) #PIL image
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(path, min_text_chars=100):
    """
    Extracts text from pdfs
    """
    full_text = []
    pdf = fitz.open(path)

    for page in pdf:
        text = page.get_text()
        if text.strip():
            full_text.append(text)

    extracted_text = "\n".join(full_text)
    return extracted_text

def extract_and_clean(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    raw = "".join(page.get_text("text") for page in doc)

    text = re.sub(r'-\n', '', raw)
    text = re.sub(r'\n(?=\w)', ' ', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.replace('\xa0', ' ').replace('\ufeff', '')
    text = re.sub(r'\n{3,}', '\n\n', text)

    return num_pages, text.strip()