# scrapeAll
An overarching pipeline for scraping and cleaning web data.

## Overview
The scrapeAll project provides a convenient and modular solution for collecting raw data from websites and cleaning the obtained data. It consists of two main parts: [collecting raw data](#collect-raw-data) and [cleaning raw data](#clean-raw-data).

**1. Collect raw data from website:**
  - [HTML Table](#html-table)
  - [Image](#image)
  - [Pmos Pdf](#pmos-pdf)


**2. Clean raw data:**
  - [Extract tables from pdf](#extract-tables-from-pdf)
  - [Extract tables from images](#extract-tables-from-images)

---

## Collect Raw Data
1. ### HTML Table
    *Required Packages:*
    - [PIL](https://pillow.readthedocs.io/en/stable/)
    - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

    *How to use:*
    > 1. open command prompt and cd to the folder that contains getRaw.py.
    > 2. ```python getRaw.py {the folder that you want to store the image}```
    > 3. paste or type the url
    > 4. type ```table```  
    <br />
    
    *Example:*
    [This is a website that contains a table](https://www.cctd.com.cn/show-46-167312-1.html)
    ```bash
    cd Desktop\scrapeAll\
    python getRaw.py data/raw/2017年5月份中国电煤价格指数/
    Enter the url:
    https://www.cctd.com.cn/show-46-167312-1.html
    table/image/pdf/pmos?
    table
    ```

---
2. ## Image
    *Required Packages:*
    - [PIL](https://pillow.readthedocs.io/en/stable/)
    - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

    *How to use:*
    > 1. open command prompt and cd to the folder that contains getRaw.py.
    > 2. ```python getRaw.py {the folder that you want to store the image}```
    > 3. paste or type the url
    > 4. type ```image```
    > 5. type the threshold of the size of the image to download. (eg. to download images larger than 25kb type 25000)  
    <br />
    
    *Example:*
    [This is a website that contains images](https://zhuanlan.zhihu.com/p/124225606)
    ```bash
    cd Desktop\scrapeAll\
    python getRaw.py data/raw/关于2020年2月广东电力市场结算情况的通告/
    Enter the url:
    https://zhuanlan.zhihu.com/p/124225606
    table/image/pdf/pmos?
    image
    Enter the minimum image size (in bytes) (press enter to accept default value: 15000 bytes):
    25000
    ```
---
3. ## Pmos Pdf
    *Required Packages:*
    - [selenium](https://pypi.org/project/selenium/)

    *How to use:*
    > 1. open command prompt and cd to the folder that contains getRaw.py.
    > 2. ```python getRaw.py {the folder that you want to store the image}```
    > 3. paste or type the pmos url
    > 4. type ```pmos```
    > 5. type the html class of the pdf element. (press enter to accept default value ```el-table__row```)
    > 6. type the number of page you want to scrape. (press enter to accept default value 1)
    > 7. type the search keyword. (press enter to accept default value None) (by giving a search keyword, you will only download pdf that contains such keyword.)
    <br />

    *Example:*
    [This is a PMOS website](https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew)
    ```bash
    cd Desktop\scrapeAll\
    python python getRaw.py data/raw/Shandong_PMOS/
    Enter the url:
    https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew
    table/image/pdf/pmos?
    pmos
    Enter the element class (press enter to accept default value: el-table__row):
    
    Enter the number of page to scrape (press enter to accept default value: 1):
    2
    Enter the search keyword (press enter to accept default value: None)
    工作日报
    ```
    **Note: This script will open a window that scrape each pdf from the PMOS website. It will also create a json file that store the url link of each pdf. The json file will help the script to recognize the pdf information that it has already collected, so that it will avoid re-scraping these pdfs.**
<br />


## Clean Raw Data
*Required Packages:*
For text extraction: (attribute to [Steven Zheng](https://github.com/stevenzheng33/pdf_chinese_text_extraction))
- [tesseract-ocr](https://pypi.org/project/pytesseract/)
- Go to src/getClean/image_to_text.py and change the variable at line 14 to your tesseract path
For image extraction:
- [pdf2image](https://pypi.org/project/pdf2image/)
- From the above website, download the poppler for your laptop.
- Go to src/getClean/pdf_to_image.py and change the variable at line 10 to your poppler bin path
---
1. ### Extract Tables from PDF
    *How to use:*
    > 1. open command prompt and cd to the folder that contains getClean.py.
    > 2. ```python getClean.py {the path to the pdf} {the path to the folder that you want to store the table}```
    > Note: if {the path to the folder that you want to store the table} is omitted, then the path to the pdf is used with 'raw' replaced with 'clean'. (eg. if path to the pdf is data/raw/xxxx.pdf then       the cleaned table would be stored in data/clean/xxxx/)
    > Note: Images of the pdf would be created and stored in a temporary folder in the same folder as the pdf.
    > 3. type ```pdf```
    <br />

    *Example:*
    ```bash
    cd Desktop\scrapeAll\
    python getClean.py data/raw/山东工作日报.pdf data/clean/山东工作日报/
    What type of data? image/pdf/table
    pdf
    ```
    **Note: If you want to convert a folder of pdfs, simply put the folder path as the input path. (eg. python getClean.py data/folder_with_multiple_pdfs/ data/folder_to_store_clean_table)**
---

2. ### Extract Tables from Images
    *How to use:*
    > 1. open command prompt and cd to the folder that contains getClean.py.
    > 2. ```python getClean.py {the path to the folder that contains images} {the path to the folder that you want to store the table}```
    > Note: if {the path to the folder that you want to store the table} is omitted, then the path to the pdf is used with 'raw' replaced with 'clean'. (eg. if path to the folder that contains images is      data/raw/xxxx/ then the cleaned table would be stored in data/clean/xxxx/)
    > 3. type ```image```
    <br />

    *Example:*
    ```bash
    cd Desktop\scrapeAll\
    python getClean.py data/raw/website_image data/clean/website_table/
    What type of data? image/pdf/table
    image
    ```

