import fitz
from PIL import Image
import io
import cv2
import numpy as np

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
