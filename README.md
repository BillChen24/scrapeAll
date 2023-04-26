# scrapeAll
Overarching pipeline for scraping and cleaning web data
Consists of two part:
1. Collect raw data from website:
  - HTML Table
  - Image
  - Pdf (PMOS websites only)
2. Clean raw data:
  - Extract tables from pdf
  - Extract tables from images

## Collect Raw Data
### HTML Table
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
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. ```python getRaw.py data/raw/2017年5月份中国电煤价格指数/```
> 3. paste ```https://www.cctd.com.cn/show-46-167312-1.html```
> 4. type ```table```

### Image
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
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. ```python getRaw.py data/raw/关于2020年2月广东电力市场结算情况的通告/```
> 3. paste ```https://zhuanlan.zhihu.com/p/124225606```
> 4. type ```image```
> 5. type ```50000```
### Pdf (PMOS only)
*Required Packages:*
- [selenium](https://pypi.org/project/selenium/)

*How to use:*
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. ```python getRaw.py {the folder that you want to store the image}```
> 3. paste or type the pmos url
> 4. type ```pdf```
> 5. type the html class of the pdf element. (press enter to accept default value ```el-table__row```)
> 6. type the number of page you want to scrape. (press enter to accept default value 1)
> 7. type the search keyword. (press enter to accept default value None) (by giving a search keyword, you will only download pdf that contains such keyword.)
<br />

*Example:*
[This is a PMOS website](https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew)
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. ```python getRaw.py data/raw/Shandong_PMOS/```
> 3. paste ```(https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew)```
> 4. type ```pdf```
> 5. press enter
> 6. type 3
> 7. type 工作日报


## Clean Raw Data
*Required Packages:*
For text extraction: (attribute to [Steven Zheng](https://github.com/stevenzheng33/pdf_chinese_text_extraction))
- [tesseract-ocr](https://pypi.org/project/pytesseract/)
- Go to src/getClean/image_to_text.py and change the variable at line 14 to your tesseract path
For image extraction:
- [pdf2image](https://pypi.org/project/pdf2image/)
- From the above website, download the poppler for your laptop.
- Go to src/getClean/pdf_to_image.py and change the variable at line 10 to your poppler bin path

### Extract Tables from PDF
*How to use:*
> 1. open command prompt and cd to the folder that contains getClean.py.
> 2. ```python getClean.py {the path to the pdf} {the path to the folder that you want to store the table}```
> Note: if {the path to the folder that you want to store the table} is omitted, then the path to the pdf is used with 'raw' replaced with 'clean'. (eg. if path to the pdf is data/raw/xxxx.pdf then the cleaned table would be stored in data/clean/xxxx/)
> Note: Images of the pdf would be created and stored in a temporary folder in the same folder as the pdf.
> 3. type ```pdf```
<br />

*Example:*
> 1. open command prompt and cd to the folder that contains getClean.py.
> 2. ```python getClean.py data/raw/Shandong_PMOS/山东电力现货市场2023年4月结算试运行工作日报(4月7日).pdf```
> 3. type ```pdf```
> 4. All tables would be stored at data/clean/Shandong_PMOS/山东电力现货市场2023年4月结算试运行工作日报(4月7日)/


### Extract Tables from Images
*How to use:*
> 1. open command prompt and cd to the folder that contains getClean.py.
> 2. ```python getClean.py {the path to the folder that contains images} {the path to the folder that you want to store the table}```
> Note: if {the path to the folder that you want to store the table} is omitted, then the path to the pdf is used with 'raw' replaced with 'clean'. (eg. if path to the folder that contains images is data/raw/xxxx/ then the cleaned table would be stored in data/clean/xxxx/)
> 3. type ```image```
<br />

*Example:*
> 1. open command prompt and cd to the folder that contains getClean.py.
> 2. ```python getClean.py data/raw/website_images/```
> 3. type ```image```
> > 4. All tables would be stored at data/clean/website_images/
