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
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    except:
        #no output path provided
        output_path = os.getcwd()

    url = input('Enter the url or the path to the json file that contains multiple urls:\n')

    #if path to json file
    if os.path.isdir(url):
        url = os.path.join(url, 'urls_info.json')
    if os.path.isfile(url):
        print(f'{url} located.')
        data_type = input('table/image/pdf?\n')
        with open(url, 'r', encoding = 'utf8') as f:
            url_dict = json.load(f)
    else:
        data_type = input('urls/table/image/pmos_pdf?\n')
        url_dict = None

    if data_type == 'urls':
        div_class = input('Enter the class of the div that contains the urls: \n')
        keyword = input('Enter the search keyword (press enter to accept default value: None):\n')
        next_page_xpath = input('Enter the XPATH of the next-page-button (press enter if not applicable): \n')
        if next_page_xpath != '':
            page_num = input('Enter the number of page to scrape (press enter to accept default value: 1):\n')
        else:
            page_num = 1
        urls_dict = scrape_urls(url=url, div_class=div_class, keyword=keyword, page_num=int(page_num), next_page_xpath=next_page_xpath)
        store_urls_as_json(urls_dict, output_path)


    if data_type == "table":
        min_rows = input('Enter the minimum number of rows for table to scrape (press enter to accept default value: 2):\n')
        if min_rows == '':
            min_rows = 2
        if url_dict is not None:
            for title, link in url_dict.items():
                #ensure not confusing path
                title = title.replace('/', '')
                try:
                    scrape_tables(link, output_path, name = title, min_rows = int(min_rows))
                except:
                    print(title + " failed to convert to table.")
                    continue
        else:
            scrape_tables(url, output_path)
        # 	url test (successful): 'https://www.cctd.com.cn/show-46-167312-1.html'

    if data_type == "image":
        size_threshold = input('Enter the minimum image size (in bytes) (press enter to accept default value: 15000 bytes):\n')
        image_format = input('Enter the extension (png/jpg/both) of target image (press enter to accept default value: both):\n')
        # 	url test (successful): https://zhuanlan.zhihu.com/p/120926031
        # 	url test (successful): https://zhuanlan.zhihu.com/p/124225606
        # 	url test (successful): https://www.ne21.com/news/show-79555.html
        # 	url test (successful): https://www.schwr.com/article/8222
        if url_dict is not None:
            for title, link in url_dict.items():
                title = title.replace('/', '')
                try:
                    download_images(link, output_path, size_threshold, name = title, image_format = image_format)
                except:
                    continue
        else:
            download_images(url, output_path, size_threshold, image_format = image_format) #download only images with size larger than 15kb

    if data_type == "pdf":
        if os.path.exists(url):
            save_pdf(pdf_dict_file = url, folder_path = output_path)
        else:
            pdf = requests.get(url, verify = False).content
            with open(output_path, 'wb') as file:
                file.write(pdf)
                print('save at '+ output_path)



    if data_type == "pmos_pdf":
        element_class = input('Enter the element class (press enter to accept default value: el-table__row):\n')
        if element_class == '':
            element_class = pmos_element_class
        page_num = input('Enter the number of page to scrape (press enter to accept default value: 1):\n')
        if page_num == '':
            page_num = 1
        else:
            page_num = int(page_num)
        search_word = input('Enter the search keyword (press enter to accept default value: None):\n')
        get_pdf_links_more_pages(url=url, element_class=element_class, page_num=page_num, search_word=search_word, pdf_dict_file= 'pdf_link.json', output_path = output_path)
        save_pdf(pdf_dict_file = os.path.join(output_path, 'pdf_link.json'), folder_path = output_path)

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
