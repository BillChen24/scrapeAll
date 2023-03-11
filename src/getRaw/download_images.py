# download_images.py
# -*- coding: utf-8 -*-
#	simple download routine for images

## Installation
# 	Install python package `selenium` (https://selenium-python.readthedocs.io/installation.html)
# 	Download and install Chromedriver to `/usr/bin` or `/usr/local/bin` (https://selenium-python.readthedocs.io/installation.html#downloading-python-bindings-for-selenium)

from selenium import webdriver
from urllib.request import urlopen, urlretrieve, Request
import os, sys
import pickle
import re
import time
from fpdf import FPDF   # create pdf from images
from PIL import Image   # for reading image sizes
import itertools
import requests		# for header request
from collections import OrderedDict

# for waiting commands:
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import imp

# UnicodeDecodeError: these little magic lines...
if sys.version_info <= (3,0):
	imp.reload(sys)
	sys.setdefaultencoding('utf8')

# Chrome Options
#	no image & js loading: https://stackoverflow.com/questions/38301993/how-to-disable-java-script-in-chrome-driver-selenium-python
chromeOptions = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2, 'profile.managed_default_content_settings.javascript': 2}
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)

# urllib headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

minsize = 20000
single_url = ''
wait_id = ''
img_regex = '.'
timeout = 10


if (len(sys.argv)>1):
# passed an argument:
	arg1 = sys.argv[1]
	if re.search('^http',arg1):
		# it's a single url
		single_url = arg1
		if (len(sys.argv)>2):
			# passed an outf
			outf = sys.argv[2]
		else:
			outf = 'TITLE'		# use the title tag
	else:
		# it's a pickle file
		outf = arg1
else:
# Set manually:
	## File name = pickle file
	# IMW exchanges on news site: http://www.nmgdlxw.cn/dbjy.asp
# 	outf = 'IM-jiaoyi'

	## Individual URL (comment out if using pickle)
	single_url = 'http://www.ne21.com/news/show-79555.html'
# 	img_regex = 'upload/'
# 	outf = ''



def imgpath_by_url(single_url):
	# Returns scraping params based on the url
	# eg if the url matches 'bjx\.com\.cn':
	# 	minsize = 15000  (only download files >= 15 kB)
	# 	timeout = 10     (wait 10 seconds before starting to download)
	# 	text_xpath = "//div[@id='content']"   (optional place to look for in page)
	# 	img_regex = 'UploadFile/'   (only download images that have this in their url -- avoids downloading news images, etc.)

	# Default params, find everything:
	wait_class = ''
	wait_id = ''
	timeout = 0
	img_regex = '.'
	text_xpath = '//body'

	if re.search('\.book118\.com',single_url):
		img_regex = "." # "\/img\/"
		wait_id = 'p16'
		timeout = 15			# time to scroll down
	if re.search('\.ne21\.com',single_url):
		img_regex = "upload/" # "\/img\/"
		wait_id = 'p16'
		timeout = 15			# time to scroll down
	elif re.search('books\.google\.com',single_url):
		img_regex = 'https\:\/\/books\.google\.com\/books\/content\?'
		timeout = 5
		wait_class = '' # 'pageImageDisplay'
	elif re.search('bjx\.com\.cn',single_url):
		# Beijixing websites
		minsize = 15000
		timeout = 10  # timeout waiting period
		text_xpath = "//div[@id='content']"
		img_regex = 'UploadFile/'
	elif re.search('escn\.com\.cn',single_url):
		text_xpath = "//div[@class='entry']"
	elif re.search('sgcio\.com',single_url):
		text_xpath = "//div[@class='post']"
		img_regex = 'uploadfile'
	elif re.search('www\.kmpex\.com',single_url):
		timeout = 3
	elif re.search('www\.cctd\.com\.cn',single_url):
		text_xpath = '//*[@id="Zoom"]'
		
	# Instructions: Customize for new website
	# elif re.search(<<regular expression matching url>>,single_url):
	# 	minsize = ...
	# 	timeout = ...
	# 	text_xpath = <<xpath expression matching main text field>> (OPTIONAL)
	# 	img_regex = <<regex matching the images want to download>> (OPTIONAL)
	# 	wait_id = <<HTML element ID to wait until loaded before proceeding with download>>  (OPTIONAL)
	# 	wait_class = <<HTML element class to wait until loaded before proceeding with download>>  (OPTIONAL)


	return img_regex, wait_id, wait_class, timeout, text_xpath


def download_multipage(url, outf='', text_xpath = '//body', img_regex = '.', wait_id = '', wait_class = '', timeout=0 , nextpage_xpath = './/a[contains(., \'下一页\')]/ancestor::div[position()=1]'):

	# capture list of all image srcs
	srcs, outf = download_from_url(url=url, outf = outf, text_xpath = text_xpath, img_regex = img_regex, wait_id = wait_id, wait_class = wait_class, timeout=timeout, nextpage_xpath=nextpage_xpath)

# 	print(srcs)
# 	return

	# begin checking all srcs:
	i = 1
	imagelist = []

	if not os.path.exists(outf):
		os.makedirs(outf)
	if not outf.endswith('/'):		outf = outf + '/'

	for src in srcs:
		if src:
			print(src)
			if re.search(img_regex,src):
				try:
					file = urlopen(Request(url=src, headers=headers))
					size = file.headers.get("content-length")
					if size:
						size = int(size)
					file.close()
					if not size or size > minsize:
						print("...downloading")
						i_str = str(i)
						extension = os.path.splitext(src)[1]
						urlretrieve(src,outf+i_str+extension)
						if extension != '.gif':
							imagelist.append(outf+i_str+extension)
						i = i + 1
				except Exception as e:
					print(e)
					pass

	# save to all.pdf
	if len(imagelist):
		pdf = FPDF(orientation = 'P', unit = 'in', format='letter')
		pdf.set_auto_page_break(0)		# do not create extra page between images
		for image in imagelist:
			try:
				im = Image.open(image)
				w, h = im.size
				pdf.add_page()
				if float(w)/float(h) < 0.7727:	# height limiting
					pdf.image(image,h=10)
				else:			# width limiting
					pdf.image(image,w=7.5)
			except:
				pass
		pdf.output(outf + 'all.pdf', "F")



def download_from_url(url, outf='', text_xpath = '//body', img_regex = '.', wait_id = '', wait_class = '', timeout=0 , nextpage_xpath = './/a[contains(., \'下一页\')]/ancestor::div[position()=1]'):
# url:			url to scrape
# outf:			new folder
# img_regex: 	only download images that match this regular expression

	print(url)

	driver=webdriver.Chrome(chrome_options=chromeOptions)
	driver.get(url)
	try:
		if wait_id != '':
			element_present = EC.presence_of_element_located((By.ID, wait_id))
		elif wait_class != '':
			element_present = EC.presence_of_element_located((By.CLASS_NAME, wait_class))
		else:
			element_present = 0

		WebDriverWait(driver, timeout/2)
		# logger.info('scrollheight = ' + driver.execute_script("return document.documentElement.scrollHeight"))
		for h in [x / 100 for x in range(1, 99)]:
			driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight*%s);" % h)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight*%s);" % h)
		if element_present:
			WebDriverWait(driver, timeout/2).until(element_present)
		else:
			WebDriverWait(driver, timeout/2)

	except TimeoutException as e:
		logger.warning('TimeoutException. URL: ' + driver.current_url + '\n' + 'Waiting for: ' + wait_id + ' ' + wait_class + '\n' + e.__str__())
		driver.close()
		return None, None
	except:
		logger.warning("Unexpected error:", sys.exc_info()[0])
		driver.close()
		return None, None


	if outf == 'TITLE':
		# set output equal to HTML title
		outf = (driver.title)
		if outf == '':
			# returned nothing, set to url fname (without .html)
			outf = os.path.splitext(os.path.split(url)[1])[0]

	# subset based on text_xpath
	found_text = driver.find_elements_by_xpath(text_xpath)
	if len(found_text) == 0:
		print(("No text found matching text_xpath: " + text_xpath))
		found_text = driver.find_elements_by_xpath('//body')

	images = found_text[0].find_elements_by_tag_name('img')
	srcs = [image.get_attribute("src") for image in images]

	# check for additional pages:
	if outf != '':   # only on initial page
		nextpage_found = driver.find_elements_by_xpath(nextpage_xpath)
		if len(nextpage_found) > 0:
			print("...found some additional pages")
			links = nextpage_found[0].find_elements_by_xpath('.//a')
			all_src = [link.get_attribute("href") for link in links]
			all_src = list(OrderedDict.fromkeys(all_src))	# remove duplicates, retain order
			try:
				all_src = [x for x in all_src if x != url]		# remove head url
			except ValueError:
				pass
			for src in all_src:
				# call child pages...
				s, t = download_from_url(url=src, outf = '', text_xpath = text_xpath, img_regex = img_regex, wait_id = wait_id, wait_class = wait_class, timeout=timeout)
				srcs += s


	driver.close()

	return srcs, outf


def download_from_list(images = []):
	for i in range(len(images)):
		src = images[i]
		extension = os.path.splitext(src)[1]
		urlretrieve(src,str(i)+extension)


if single_url != '':
	img_regex, wait_id, wait_class, timeout, text_xpath = imgpath_by_url(single_url)
# 	download_from_url(single_url, outf = outf, text_xpath = text_xpath, img_regex = img_regex, wait_id = wait_id, wait_class = wait_class, timeout=timeout)
	download_multipage(url=single_url, outf = outf, text_xpath = text_xpath, img_regex = img_regex, wait_id = wait_id, wait_class = wait_class, timeout=timeout)



else:
#	we have a pickle
	complete_pickle_ext = '--images-completed.pickle'

	with open(outf + '.pickle', 'rb') as f:
		url_files = pickle.load(f)

	if os.path.exists(outf + complete_pickle_ext):
		with open(outf + complete_pickle_ext, 'rb') as f:
			comp_files = pickle.load(f)
	else:
		comp_files = []

	# print(url_files)

	for i in url_files:
		print((i[1]))
		print((i[0]))
		if i in comp_files:
			# already downloaded previously
			print('...skipping\n')
			continue
		img_regex, wait_id, wait_class, timeout, text_xpath = imgpath_by_url(i[0])
# 		download_from_url(i[0], outf = i[1] + u'/', img_regex = img_regex, wait_id = wait_id, wait_class = wait_class, timeout=timeout)
		download_multipage(url = i[0], outf = i[1] + '/',text_xpath = text_xpath, img_regex = img_regex, wait_id = wait_id, wait_class = wait_class, timeout=timeout)
		print(('File ' + i[1] + ' completed\n'))
		comp_files.append(i)

		# save completed files to file for later use
		with open(outf + complete_pickle_ext,'wb') as f:
			pickle.dump(comp_files, f, pickle.HIGHEST_PROTOCOL)
