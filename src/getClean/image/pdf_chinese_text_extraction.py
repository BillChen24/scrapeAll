#https://github.com/stevenzheng33/pdf_chinese_text_extraction
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

#images = convert_from_path('关于发布山东省2019年5月份电力直接交易（集中竞价）结果的公告.pdf.pdf')

for i in range(len(images)):

    images[i].save('page'+ str(i) +'.jpg', 'JPEG')

def process_image(iamge_name, lang_code):
	return pytesseract.image_to_string(Image.open(iamge_name), lang=lang_code)

def print_data(data):
	print(data)

def output_file(filename, data):
	file = open(filename, "w+")
	file.write(data)
	file.close()

def main():
    num_page = len(images)
    text_combined = ''
    for i in range(num_page):

        text_combined += process_image("page"+str(i)+".jpg", "chi_sim")



    text_combined = text_combined.replace("\n", "")
    text_combined = text_combined.replace("\x0c","")
    text_combined = text_combined.replace(" ","")
    text_combined

    print_data(text_combined)


if  __name__ == '__main__':
	main()