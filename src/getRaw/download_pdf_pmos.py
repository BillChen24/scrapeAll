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

def get_pdf_links_one_page(url, element_class = pmos_element_class, driver = None, button_xpath = None, pdf_dict = {}, search_word = None):
    #print('get_pdf_links_one_page is called.')
    if driver is None:
        driver = webdriver.Chrome()

    if not driver.current_url == url:
        print(url)
        driver.get(url)

    # wait till elements show up
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, element_class)))
    #time.sleep(10)

    # Find all elements with a specific class name
    elements = driver.find_elements(By.CLASS_NAME, element_class)
    #print(elements)

    # Loop through each element
    for element in elements:
        # Click on the element
        pdf_name = element.find_element(By.TAG_NAME, 'span').text
        if not search_word is None and search_word not in pdf_name: #skip elements that don't contain keyword
            continue
        if len(pdf_name) < 3: #skip 热点信息
            continue
        #print(pdf_name)
        try:
            element.find_element(By.TAG_NAME, 'span').click() #click on element
        except WebDriverException:
            print(pdf_name + " is not clickable")
            continue
        time.sleep(5)  # wait for page to load
        #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, button_xpath)))
        if button_xpath is None:
            #if button_xpath not provided, click the last button
            pdf_button = driver.find_elements(By.TAG_NAME, 'button')[-1]
        else:
            pdf_button = driver.find_element(By.XPATH, button_xpath)
        try:
            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable(pdf_button))
            pdf_button.click()
        except WebDriverException:
            # no pdf link, save screenshot instead
            try:
                img = driver.find_elements(By.TAG_NAME, 'div')[-3].screenshot_as_base64
                pdf_link = base64.decodebytes(img.encode('utf-8'))
                print(pdf_name+' has screenshot saved')
            except WebDriverException:
                # if cannot screenshot, skip
                pdf_link = None
                print(pdf_nam + 'has no Link and cannot screenshot')
            pdf_dict[pdf_name] = pdf_link
            #close popup
            try:
                driver.find_elements(By.CSS_SELECTOR, "[aria-label=Close]")[1].find_element(By.TAG_NAME, 'i').click()
                time.sleep(3)
            except:
                ...
                #print(pdf_name)
            continue
        time.sleep(5)
        #print(driver.current_url)

        #if pdf link exsits, save link and close tab
        driver.switch_to.window(driver.window_handles[-1])
        pdf_link = driver.current_url
        driver.close()
        try:
            driver.switch_to.window(driver.window_handles[0])
        except:
            ...

        #close popup
        time.sleep(5)
        driver.find_elements(By.CSS_SELECTOR, "[aria-label=Close]")[1].find_element(By.TAG_NAME, 'i').click()
        time.sleep(3)
        pdf_dict[pdf_name] = pdf_link
    return pdf_dict, driver

def get_pdf_links_more_pages(url, element_class = pmos_element_class, driver = None, page_num = 1, pdf_dict = {}, search_word = None):
    '''
    get pdf links from url
    returns a dictionary contains all pdf links
    '''
    #print('get_pdf_links_more_pages is called.')
    # if page_num == 1:
    #     pdf_dict, driver = get_pdf_links_one_page(url, element_class, driver = driver, pdf_dict = pdf_dict, search_word=search_word)
    #     return pdf_dict
    for _ in range(page_num):
        pdf_dict, driver = get_pdf_links_one_page(url, element_class, driver = driver, pdf_dict = pdf_dict, search_word=search_word)
        if driver.find_element(By.CLASS_NAME, 'btn-next').is_enabled():
            driver.find_element(By.CLASS_NAME, 'btn-next').click()
            time.sleep(5)
    return pdf_dict

def save_pdf(pdf_dict, folder_path = None):
    """
    save all pdfs to path
    """
    if folder_path is None:
        folder_path = os.curdir
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for k, v in pdf_dict.items():
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
