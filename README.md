# scrapeAll
Overarching pipeline for scraping and cleaning web data
Consists of two part:
1. Collect raw data from website:
  - HTML Table
  - Image
  - Pdf (PMOS websites only)
2. Clean raw data:
  - Extract images from pdf
  - Extract tables from images
  - Combine and split tables

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
> 2. ```python getRaw.py data/2017年5月份中国电煤价格指数/```
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

*Example:*\
[This is a website that contains images](https://zhuanlan.zhihu.com/p/124225606)
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. ```python getRaw.py data/关于2020年2月广东电力市场结算情况的通告/```
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

*Example:*\
[This is a PMOS website](https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew)
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. ```python getRaw.py data/Shandong_PMOS/```
> 3. paste ```(https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew)```
> 4. type ```pdf```
> 5. press enter
> 6. type 3
> 7. type 工作日报


## Clean Raw Data
### Extract Images from PDF
*Required Packages:*
- [pdf2image](https://pypi.org/project/pdf2image/)
- From the above website, download the poppler for your laptop.
- Go to src/getClean/pdf_to_image.py and change the variable at line 10 to your poppler bin path


*How to use:*
> 1. open command prompt and cd to the folder that contains getClean.py.
> 2. ```python getRaw.py {the folder that you want to store the image}```
> 3. paste or type the pmos url
> 4. type ```pdf```
> 5. type the html class of the pdf element. (press enter to accept default value ```el-table__row```)
> 6. type the number of page you want to scrape. (press enter to accept default value 1)
> 7. type the search keyword. (press enter to accept default value None) (by giving a search keyword, you will only download pdf that contains such keyword.)
<br />

*Example:*\
[This is a PMOS website](https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew)
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. ```python getRaw.py data/Shandong_PMOS/```
> 3. paste ```(https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew)```
> 4. type ```pdf```
> 5. press enter
> 6. type 3
> 7. type 工作日报

### Extract Tables from Image

### Combine and Split Tables
