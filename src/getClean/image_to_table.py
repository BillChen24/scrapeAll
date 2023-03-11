#https://github.com/stevenzheng33/table_OCR
import pandas as pd
import numpy as np
import requests
import os
import time

from aip import AipOcr

"""
1. Follow instruction on https://cloud.baidu.com/doc/OCR/s/dk3iqnq51
2. pip install baidu-aip
"""

""" Your APPID AK SK """
APP_ID = '30505345'
API_KEY = 'PlF6csVBFlGKyZzxMd1AzVCP'
SECRET_KEY = 'MIwiRQRpwQhKU01KtGqo4yl0z3VvofuS'

if APP_ID == 'Your App ID' or API_KEY == 'Your Api Key' or SECRET_KEY == 'Your Secret Key':
    print('Make sure you input the APP information')

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def read_image_to_xls(filepath, newfile_name, outputpath):
    result = client.tableRecognition(
    get_file_content(filepath),
        {
            'result_type': 'excel',
        },
    )
    #print(filepath)
    #print(result)
    result_url = result['result']['result_data']
    excel_file = requests.get(result_url, allow_redirects=True)

    open(os.path.join(outputpath, newfile_name) , 'wb').write(excel_file.content)


def convert_all_images(inputpath, outputpath=None):
    if outputpath is None:
        outputpath = os.path.join(inputpath, 'temp/')
    if not os.path.exists(outputpath):
         os.mkdir(outputpath)
    for filename in os.listdir(inputpath):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            completeName = os.path.join(inputpath, filename)
            read_image_to_xls(completeName, filename[:-4]+'.xls', outputpath)
            time.sleep(3)
    print('Temporary tables successfully saved at ' + outputpath)
