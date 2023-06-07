"""
1. pip install pdf2image
2. Download poppler
3. Get_path_to_poppler_bin
"""
import os
from pdf2image import convert_from_path

#change the following line to your poppler bin path
poppler_path = r"C:\Program Files\poppler-0.68.0\bin"

def save_image_from_pdf(pdf_path, image_path = None, image_name = 'page'):
    if image_path is None:
        image_path = os.path.join(os.path.dirname(pdf_path), 'temp/')
    # create images from pdf
    images = convert_from_path(pdf_path, poppler_path = poppler_path)

    # check if out path exist, create one if not
    if not os.path.isdir(image_path):
        os.makedirs(image_path)
    # save images
    for i in range(len(images)):
        if image_name is None:
            image_name = 'page_'
        images[i].save(image_path+f'{image_name}_{i}.jpg', 'JPEG')
    print('Pdf images successfully saved at ' + image_path)
