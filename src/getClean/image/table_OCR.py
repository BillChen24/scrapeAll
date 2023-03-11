#https://github.com/stevenzheng33/table_OCR
import pandas as pd
import numpy as np
import requests
import os
import time

from aip import AipOcr


""" Your APPID AK SK """
APP_ID = 'Your App ID'
API_KEY = 'Your Api Key'
SECRET_KEY = 'Your Secret Key'

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
    print(filepath)
    print(result)
    result_url = result['result']['result_data']
    excel_file = requests.get(result_url, allow_redirects=True)

    open(os.path.join(outputpath, newfile_name) , 'wb').write(excel_file.content)


def convert_all_images(inputpath, outputpath):
    for filename in os.listdir(inputpath):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            completeName = os.path.join(inputpath, filename)
            read_image_to_xls(completeName, filename[:-4]+'.xls', outputpath)
            time.sleep(10)