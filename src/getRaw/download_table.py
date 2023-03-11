# download_table.py
# -*- coding: utf-8 -*-
#	download html tables using Selenium and pandas
#	table scraping from: https://beenje.github.io/blog/posts/parsing-html-tables-in-python-with-pandas/

from selenium import webdriver
import urllib.request, urllib.parse, urllib.error
import os, sys, imp
import pickle
import re
import io
import itertools
import requests		# for header request
from collections import OrderedDict
import pandas as pd
from util import *   # load shared utility functions

# UnicodeDecodeError: these little magic lines...
if sys.version_info <= (3,0):
	imp.reload(sys)
	sys.setdefaultencoding('utf8')


#Chrome Options
#	no image & js loading: https://stackoverflow.com/questions/38301993/how-to-disable-java-script-in-chrome-driver-selenium-python
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2,  'profile.managed_default_content_settings.javascript': 2}
chromeOptions.add_experimental_option("prefs",prefs)


def trim(string):
	return string.strip()

# for future use, can download images:
minsize = 10000
single_url = ''



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
# MANUAL ENTRY:
## File name = pickle file
# 	outf = 'cctd-monthly-revised'
	outf = 'cctd-monthly-revised-round2'
## Individual URL (comment out if using pickle)
# 	single_url = 'https://www.cctd.com.cn/show-46-167312-1.html'
# 	outf = u'TITLE'

# Local file  (comment out if using pickle)
# 	single_url = 'file:///Users/michd/Research/python/download_images/cctd-monthly-2014-2015.html'
# 	outf = 'cctd-monthly-2014-2015'

def textpath_by_url(single_url):

	if re.search('cctd\.com\.cn',single_url):
# 		text_xpath = "//table[@class='listTable2']"
		text_xpath = ".//td[contains(., \'全国\')]/ancestor::table[position()<4]"
	else:
		text_xpath = '/html'

	return text_xpath


def download_from_url(url, outf='TITLE', text_xpath = '/html'):
# url:			url to scrape
# outf:			new file
# text_xpath: 	text xpath

	print(url)

# 	if not re.search('^http',url):
# 		return ''

	driver=webdriver.Chrome(chrome_options=chromeOptions)
	driver.get(url)
	found_text = driver.find_elements_by_xpath(text_xpath)

	# only first match:
# 	text = found_text[0].text		# -> text without html
	if len(found_text)>0:
		# found some text

		text = found_text[0].get_attribute('outerHTML')		# -> with html
		if outf.endswith('TITLE'):
			# code to set output equal to HTML title
			o = (driver.title)
# 			print outf
			if o == '':
				# returned nothing, set to url fname (without .html)
				o = os.path.splitext(os.path.split(url)[1])[0]
# 				print outf
			outf = outf[:-5] + o

		print(outf)

		df = pd.read_html(text,header=0)[0]
		try:
			print(outf)
			df.to_csv(outf + '.csv')
		except ValueError:
			print('Unable to extract table!')
			driver.close()
			return 0


		# 	let's write
# 			with io.open(outf + u'.html', 'w', encoding='utf-8') as f:
# 				f.writelines(text)


	else:
	#	no text found
		print('...nothing found for xpath="' + text_xpath + '"')
		driver.close()
		return 0

	driver.close()
	return 1


if single_url != '':
	download_from_url(single_url, outf = outf, text_xpath = textpath_by_url(single_url))

else:
#	we have a pickle

	with open(outf + '.pickle', 'rb') as f:
		url_files = pickle.load(f)

	if os.path.exists(outf + '--table-completed.pickle'):
		with open(outf + '--table-completed.pickle', 'rb') as f:
			comp_files = pickle.load(f)
	else:
		comp_files = []


	comp_fnames = [c[1] for c in comp_files]   	# just the names of completed files
# 	print url_files

	# create directory
	outdir = outf
	if not outdir.endswith('/'):		outdir = outdir + '/'
	if outdir != '' and not os.path.exists(outdir):
		os.makedirs(outdir)


	for i in url_files:
		print(i[1])
		print(i[0])
# 		if i in comp_files or i[1] == u'TITLE':		# revert back later without 'TITLE' check
		if i in comp_files:
			# already downloaded previously
			print('...skipping\n')
			continue
		if i[1] in comp_fnames:
			#  already downloaded a file with the same name, but different url
			ind = 2
			u = i[1] + '-' + str(ind)
			while u in comp_fnames:
				# keep adding indices until not found
				ind = ind + 1
				u = i[1] + '-' + str(ind)
			i[1] = u

		i[1] = clean_filename(i[1])
		print(i[1])

		if download_from_url(i[0], outf = outdir + i[1], text_xpath = textpath_by_url(i[0])):
			print('File ' + i[1] + ' completed\n')
			comp_files.append(i)

		# save completed files to file for later use
		with open(outf + '--text-completed.pickle','wb') as f:
			pickle.dump(comp_files, f, pickle.HIGHEST_PROTOCOL)
