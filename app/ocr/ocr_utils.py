import cv2
import pytesseract
from utils.file_loader import load_file_image

pytesseract.pytesseract.tesseract_cmd = r"D:\home\[00]_Projects\Extractor\tesseract.exe"

def load_image(file_path):
    image = load_file_image(file_path)
    height, width = image.shape[:2]
