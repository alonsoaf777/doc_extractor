import cv2
import pytesseract
import json
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load ROIs
def load_normalized_rois(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def structure_output(results):
    return {
        "Medical and dental expenses (1)": results.get("roi_1", "0"),
        "Form 1040 or 1040-SR (2)": results.get("roi_2", "0"),
        "Line 2 times 7.5% (3)": results.get("roi_3", "0"),
        "Line 3 minus line 1 or 0 (4)": results.get("roi_4", "0"),
        "State and local taxes": {
            "State and local income taxes (5a)": results.get("roi_5", "0"),
            "State and local real estate taxes (5b)": results.get("roi_6", "0"),
            "State and local personal property taxes (5c)": results.get("roi_7", "0"),
            "Lines 5a plus 5b plus 5c (5d)": results.get("roi_8", "0"),
            "Smaller of 5d or 10,000 (5e)": results.get("roi_9", "0")
        },
        "Other taxes (6)" : results.get("roi_10", "0"),
        "Lines 5e plus 6 (7)" : results.get("roi_11", "0"),
        "Home mortage interest and points" : {
            "Home mortage and points reported (8a)" : results.get("roi_12", "0"),
            "Home mortage not reported (8b)" : results.get("roi_13", "0"),
            "Points not reported (8c)" : results.get("roi_14", "0"),
            "Reserved for future use (8d)" : results.get("roi_15", "0"),
            "Lines 8a plus 8b plus 8c (8e)" : results.get("roi_16", "0")
        },
        "Investment interest (9)" : results.get("roi_17", "0"),
        "Lines 8e plus 9 (10)" : results.get("roi_18", "0"),
        "Gifts by cash or check (11)" : results.get("roi_19", "0"),
        "Other than by cash or check (12)" : results.get("roi_20", "0"),
        "Carryover from prior year (13)" : results.get("roi_21", "0"), 
        "Lines 11 plus 12 plus 13 (14)" : results.get("roi_22", "0"),
        "Casualty and theft loss(es) (15)" : results.get("roi_23", "0"),
        "Other-from list in instructions (16)" : results.get("roi_24", "0"),
        "Add amounts from lines 4 to 16 (17)" : results.get("roi_25", "0")
    }

def extract_text_from_rois(image):
    '''
    This function takes the generated pdf -> image as input and returns a formatted json with the extracted data.
    
    Transformation and filters:
    -The ROIs in rois.json are normalized, therefore the current roi must be scaled with the image shape.
    -A rezising of the frame is applied. 
    -The image is converted to gray
    -Adaptive threshold generates a binary image (gray -> black and white) based on different regions or neighborhoods values.
    -Dilate method is a morphological transformation, higher kernel is a thinner number.
    
    Tesseract config:
    - --oem3: 
    - --psm6:
    - tessedit_char_whitelist=0123456789: 
    '''
    rois = load_normalized_rois(r"app\ocr\rois.json")
    results = {}
    height, width = image.shape[:2]

    for idx, roi in enumerate(rois):
        x = int(roi[0] * width)
        y = int(roi[1] * height)
        w = int(roi[2] * width)
        h = int(roi[3] * height)

        roi_img = image[y:y+h, x:x+w]
        scale_factor = 3
        roi_img = cv2.resize(roi_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)

        kernel = np.ones((1, 1), np.uint8) ## Increasing kernel display thinner numbers
        thresh = cv2.dilate(thresh, kernel, iterations=1)

        # cv2.imshow("window", thresh)
        # cv2.waitKey(0)

        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(thresh, config=custom_config).strip()

        results[f"roi_{idx+1}"] = text if text else "0" #Save each value

    formatted_json = structure_output(results)
    return formatted_json
