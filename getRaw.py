from src.getRaw.scrape_webpage import *
import sys
import os
import pandas as pd

def main():
    try:
        output_path = sys.argv[1]
    except:
        output_path = os.getcwd()
    url = input('Enter the url:\n')
    data_type = input('html/image?\n')
    if data_type == "html":
        # 	url test (successful): 'https://www.cctd.com.cn/show-46-167312-1.html'
        scrape_tables(url, output_path)
    if data_type == "image":
        # 	url test (successful): https://zhuanlan.zhihu.com/p/120926031
        # 	url test (successful): https://zhuanlan.zhihu.com/p/124225606
        download_images(url, output_path)


if  __name__ == '__main__':
    main()
