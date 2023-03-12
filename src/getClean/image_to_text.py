#https://github.com/stevenzheng33/pdf_chinese_text_extraction

"""
install tesseract-ocr
pip install tesseract
get tessseract path
"""

from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_image(iamge_name, lang_code):
    return pytesseract.image_to_string(Image.open(iamge_name), lang=lang_code)

def output_file(filename, data, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(data)
        f.close()

def save_text_from_image(image_path, txt_path = None, txt_name = 'jpg_text.txt'):
    if txt_path is None:
        txt_path = image_path
    # check if out path exist, create one if not
    if not os.path.isdir(txt_path):
        os.makedirs(txt_path)

    text_combined = ''
    image_ls = os.listdir(image_path)
    for image in image_ls:
        if image.endswith('.jpg') or image.endswith('.png'):
            text_combined += process_image(os.path.join(image_path, image), "chi_sim")
    text_combined = text_combined.replace("\n", "")
    text_combined = text_combined.replace("\x0c","")
    text_combined = text_combined.replace(" ","")

    out_path = os.path.join(txt_path, txt_name)
    output_file(out_path, text_combined)
    print("Imgae text successfully saved at " + out_path + '!')
    return
