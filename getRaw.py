from src.getRaw.scrape_webpage import *
from src.getRaw.download_pdf_pmos import *
import sys
import os
import pandas as pd

pmos_element_class = 'el-table__row'

def main():
    try:
        output_path = sys.argv[1]
        current = os.getcwd()
        output_path = os.path.join(current, output_path)
    except:
        #no output path provided
        output_path = os.getcwd()
    url = input('Enter the url:\n')
    data_type = input('table/image/pdf?\n')
    if data_type == "table":
        # 	url test (successful): 'https://www.cctd.com.cn/show-46-167312-1.html'
        scrape_tables(url, output_path)
    if data_type == "image":
        size_threshold = input('Enter the image size threshold to download:\n')
        # 	url test (successful): https://zhuanlan.zhihu.com/p/120926031
        # 	url test (successful): https://zhuanlan.zhihu.com/p/124225606
        # 	url test (successful): https://www.ne21.com/news/show-79555.html
        # 	url test (successful): https://www.schwr.com/article/8222
        download_images(url, output_path, size_threshold) #download only images with size larger than 30kb

    if data_type == "pdf":
        #url = input('Enter the pmos url:\n')
        element_class = input('Enter the element class (default el-table__row):\n')
        if element_class == '':
            element_class = pmos_element_class
        page_num = input('Enter the number of page to scrape (default 1):\n')
        if page_num == '':
            page_num = 1
        else:
            page_num = int(page_num)
        search_word = input('Enter the search keyword (default None):\n')
        pdfs = get_pdf_links_more_pages(url=url, element_class=element_class, page_num=page_num, search_word=search_word)
        save_pdf(pdfs, folder_path = output_path)
        #python getRaw.py data/Test/pmos_pdfs/
# Enter the url:
# https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew
# html/image/pdf?
# pdf
# Enter the element class (default el-table__row):
#
# el-table__row
# Enter the number of page to scrape (default 1):
# 3
# 3
# Enter the search keyword (default None):



if  __name__ == '__main__':
    main()
