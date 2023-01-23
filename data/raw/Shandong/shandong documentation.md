# Firm level data documentation

The raw data is scraped from the pmos Shandong site (https://pmos.sd.sgcc.com.cn) using the script `pmos_download.py`. <br>

The script intakes the URL of the pmos site and automatically collects the link for every pdf document on the site. Since it takes some time for the server to respond to every request, scraping all the links can take up to 3 or 4 hours. The output of the script should be multiple folders with pdfs in them. The folder name corresponds to the post name and the pdf name corresponds to the file name. The files collected are under folder `/raw` .

The first step of processing is to manually screenshot the tables in the pdfs. Since the format of the tables varies in the file, it is difficult to use a script to detect the boundary of the table. The name of the screenshot should correspond to the time period of the file. Eg. `'2020_q3_planned.png'` for 2020 third quarter ‘计划' data. When the table spans multiple pages, a suffix should be added to the picture file such as `'_1'` and `'_2'`.

The second step is to use the `table_OCR` script to reads the picture from the previous step into xls format that is readable by scripts. The script takes in the directory of the folder that contains all the pictures. Since it uses the Baidu OCR API, the user needs to first create an account and configure the app_id and secret. One thing to note is that there is a limit to the daily free amount of OCR files. The result of this step is stored in `/clean`.

<br>


# Provincial level data documentation


The raw data is scraped from the pmos Shandong site (https://pmos.sd.sgcc.com.cn) using the script `pmos_download.py` using the same process as the firm level data. The data is manually distinguished and collected in the `/raw` folder. <br>

The script used for processing is `pdf_chinese_text_extraction`. It uses an offline OCR library to converts the entire pdf file into texts. The script also gets rid of the unnecessary format leaving only the strings.

A customized script is needed to work with the text extraction. How the script is developed should depend on the context of the text. One common way is to use signal words such as `'申报电量'` and `'申报电价'` to identify the position of the data. Another thing to note is that there could be multiple occurrences of the same signal words. It could be tricky to distinguish between them. The processed data is stored in `/cleaned`.

<br>


