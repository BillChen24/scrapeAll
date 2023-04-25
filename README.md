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
> 2. `python getRaw.py {the folder that you want to store the image}`
> 3. paste the url
> 4. type "table"  
<br />

*Example:*
[This is a website that contains a table](https://www.cctd.com.cn/show-46-167312-1.html)
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. `python getRaw.py data/2017年5月份中国电煤价格指数/`

### Image
*Required Packages:*
- [PIL](https://pillow.readthedocs.io/en/stable/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)\
*Example:*\
[This is a website that contains images](https://zhuanlan.zhihu.com/p/124225606)
> 1. open command prompt and cd to the folder that contains getRaw.py.
> 2. `python getRaw.py {the folder that you want to store the image}`
> 3. 
### Pdf (PMOS only)

## Clean Raw Data
### Extract Images


### Extract Tables
### Combine and Split Tables
