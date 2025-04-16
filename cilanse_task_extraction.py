# import os
# import pytesseract
# from pdf2image import convert_from_path
# import cv2
# import numpy as np
# from PIL import Image

# # Set path to tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # CONFIG
# pdf_path = r"D:\PROGRAMS\python\streamlit\cilans_env\cilans company task\005A Kamandakya - Nitisara english translation-1-50 (1).pdf"
# output_dir = r"D:\PROGRAMS\python\streamlit\cilans_env\output_cilanse"
# lang_code = "guj+san+eng"

# os.makedirs(output_dir, exist_ok=True)

# def preprocess_image(image):
#     image = np.array(image)
#     gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#     blur = cv2.GaussianBlur(gray, (3,3), 0)
#     thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
#     return Image.fromarray(thresh)

# pages = convert_from_path(pdf_path, dpi=300)

# for i, page in enumerate(pages):
#     processed = preprocess_image(page)
#     extracted_text = pytesseract.image_to_string(processed, lang=lang_code)
#     with open(f"{output_dir}/page_{i+1}.txt", "w", encoding="utf-8") as f:
#         f.write(extracted_text)

# print(f"OCR complete. Extracted {len(pages)} pages to {output_dir}/")





import os
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image

# -----------------------------
# CONFIG
pdf_path = "D:\\PROGRAMS\\python\\streamlit\\cilans_env\\cilans company task\\005A Kamandakya - Nitisara english translation-1-50 (1).pdf"
output_dir = "D:\\PROGRAMS\\python\\streamlit\\cilans_env\\output_cilanse"
lang_code = "guj+san+eng"  # Gujarati + Sanskrit + English

os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Structuring Heuristic for Markdown-style Text
def structure_text(raw_text):
    lines = raw_text.split("\n")
    md_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Treat all-uppercase or short lines as section headings
        if line.isupper() or len(line) < 40:
            md_lines.append(f"### {line}")
        else:
            md_lines.append(line)
    return "\n".join(md_lines)

# -----------------------------
# Preprocessing Function for Better OCR
def preprocess_image(image):
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return Image.fromarray(thresh)

# -----------------------------
# Convert PDF Pages to Images
pages = convert_from_path(pdf_path, dpi=300)

extracted_pages = []

for i, page in enumerate(pages):
    processed = preprocess_image(page)
    
    # OCR with Tesseract
    extracted_text = pytesseract.image_to_string(processed, lang=lang_code)

    # ✨ Apply structuring
    structured_text = structure_text(extracted_text)

    # Save structured OCR text
    with open(f"{output_dir}/page_{i+1}.txt", "w", encoding="utf-8") as f:
        f.write(structured_text)
    
    extracted_pages.append({"page": i+1, "text": structured_text})

print(f"✅ OCR complete. Extracted and saved {len(extracted_pages)} pages to '{output_dir}'")
