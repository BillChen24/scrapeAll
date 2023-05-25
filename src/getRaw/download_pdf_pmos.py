import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import os
import json
import base64

pmos_element_class = 'el-table__row'

def get_pdf_links_one_page(url, element_class=pmos_element_class, driver=None, button_xpath=None, pdf_dict={}, search_word=None, pdf_dict_file='pdf_link.json', output_path = None):
    if driver is None:
        driver = webdriver.Chrome()

    if not driver.current_url == url:
        print(url)
        driver.get(url)

    if output_path is None:
        output_path = os.curdir

    pdf_dict_file = os.path.join(output_path, pdf_dict_file)

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, element_class)))

    elements = driver.find_elements(By.CLASS_NAME, element_class)

    existing_elements = set()
    try:
        with open(pdf_dict_file, 'r', encoding = 'utf8') as f:
            existing_pdf_dict = json.load(f)
            existing_elements = set(existing_pdf_dict.keys())
    except FileNotFoundError:
        existing_pdf_dict = {}
        pass

    for element in elements:
        pdf_name = element.find_element(By.TAG_NAME, 'span').text
        if pdf_name in existing_elements:
            print(f"Skipping element '{pdf_name}' (already exists in pdf_link.json)")
            continue
        if not search_word is None and search_word not in pdf_name:
            continue
        if len(pdf_name) < 3:
            continue

        try:
            element.find_element(By.TAG_NAME, 'span').click()
        except WebDriverException:
            print(pdf_name + " is not clickable")
            continue

        time.sleep(5)

        if button_xpath is None:
            pdf_button = driver.find_elements(By.TAG_NAME, 'button')[-1]
        else:
            pdf_button = driver.find_element(By.XPATH, button_xpath)

        try:
            pdf_button.click()
        except WebDriverException:
            try:
                img = driver.find_elements(By.TAG_NAME, 'div')[-3].screenshot_as_base64
                pdf_link = base64.decodebytes(img.encode('utf-8'))
                print(pdf_name + ' has screenshot saved')
            except WebDriverException:
                pdf_link = None
                print(pdf_name + ' has no Link and cannot screenshot')
            existing_pdf_dict.update({pdf_name: pdf_link})

            try:
                driver.find_elements(By.CSS_SELECTOR, "[aria-label=Close]")[1].find_element(By.TAG_NAME, 'i').click()
                time.sleep(3)
            except:
                ...

            continue

        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        pdf_link = driver.current_url
        driver.close()

        try:
            driver.switch_to.window(driver.window_handles[0])
        except:
            ...

        time.sleep(5)
        driver.find_elements(By.CSS_SELECTOR, "[aria-label=Close]")[1].find_element(By.TAG_NAME, 'i').click()
        time.sleep(3)
        existing_pdf_dict.update({pdf_name: pdf_link})

        # Save pdf_dict after processing each element
        save_interval = 1
        if len(pdf_dict) % save_interval == 0:
            save_pdf_dict(existing_pdf_dict, pdf_dict_file, output_path)

    return driver


def save_pdf_dict(pdf_dict, pdf_dict_file, output_path):
    if output_path is None:
        output_path = os.path.curdir

    if pdf_dict_file is None:
        pdf_dict_file = 'pdf_link.json'
    pdf_dict_file = os.path.join(output_path, pdf_dict_file)
    with open(pdf_dict_file, 'w', encoding='utf8') as f:
        json.dump(pdf_dict, f, ensure_ascii=False)


def get_pdf_links_more_pages(url, element_class=pmos_element_class, driver=None, page_num=1, search_word=None, pdf_dict_file=None, output_path = None):
    for _ in range(page_num):
        driver = get_pdf_links_one_page(url, element_class, driver=driver, search_word=search_word, pdf_dict_file=pdf_dict_file, output_path = output_path)
        if driver.find_element(By.CLASS_NAME, 'btn-next').is_enabled():
            driver.find_element(By.CLASS_NAME, 'btn-next').click()
            time.sleep(5)
    driver.close()
    print("All done!")

def save_pdf(pdf_dict_file = 'pdf_link.json', folder_path = None):
    if folder_path is None:
        folder_path = os.curdir
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(pdf_dict_file, 'r', encoding = 'utf8') as f:
        pdf_dict = json.load(f)

    dir_list = os.listdir(folder_path)
    for k, v in pdf_dict.items():
        if k in dir_list:
            continue
        if v is None:
            continue
        if type(v) == str:
            path = os.path.join(folder_path, k+'.pdf')
            pdf = requests.get(v, verify = False).content
            with open(path, 'wb') as file:
                file.write(pdf)
                print('save at '+path)
        elif type(v) == bytes:
            path = os.path.join(folder_path, k+'.png')
            with open(path, 'wb') as file:
                file.write(v)
                #file.write(base64.decodebytes(v))
                print('save at '+path)


# pmos_url = "https://pmos.sd.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew"
# element_class = 'el-table__row'
# button_xpath = '/html/body/div[3]/div/div[2]/div/div/div[2]/div[3]/span[2]/button[2]' (optional)
# search_word = '工作日报' (optional)
# pdfs = get_pdf_links_more_pages(pmos_url, element_class, page_num=5, search_word=None)
# save_pdf(pdfs)
