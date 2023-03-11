# download_text.py
# -*- coding: utf-8 -*-
#	simple download routine for articles spread across multiple pages
from selenium import webdriver
import urllib.request, urllib.parse, urllib.error
import os, sys, imp
import pickle
import re
import io
import itertools
import requests		# for header request
from collections import OrderedDict

# UnicodeDecodeError: these little magic lines...
if sys.version_info <= (3,0):
	imp.reload(sys)
	sys.setdefaultencoding('utf8')


#Chrome Options
#	no image & js loading: https://stackoverflow.com/questions/38301993/how-to-disable-java-script-in-chrome-driver-selenium-python
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2,  'profile.managed_default_content_settings.javascript': 2}
# chromeOptions.add_experimental_option("prefs",prefs)


def trim(string):
	return string.strip()

# for future use, can download images:
minsize = 10000
single_url = ''
nextpage_xpath = ''


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
#		for future use:
	# outf = ''

## Individual URL (comment out if using pickle)
	# single_url = 'http://www.sgcio.com/Banksinfo/yhzx/2017/0401/15055.html'
	# text_xpath = "//div[@id='main']"
	# outf = u'《2017年云南电力市场化交易实施方案》印发'
	# nextpage_xpath = ".//div[@class='pageList']"
	# single_url = 'file:///Users/michd/Research/python/download_images/test.html'
	single_url = 'http://shoudian.bjx.com.cn/html/20150508/616370.shtml'
	outf = '宁夏首次电力集中撮合交易完成105亿千瓦时'


def textpath_by_url(single_url):
	if re.search('\.bjx\.com\.cn',single_url):
		text_xpath = "//div[@class='list_main']"
	elif re.search('360doc\.com',single_url):
		text_xpath = "//div[@class='a_left']"
	elif re.search('nmgnews\.com\.cn',single_url):
		text_xpath = "//table[@style='clear:both']"
	elif re.search('impc\.com\.cn.*sgtd\/',single_url):
		text_xpath = "/html/body/table[4]/tbody/tr/td[3]/table[2]/tbody/tr/td/table/tbody/tr[2]/td[2]/table"
	elif re.search('cec\.org\.cn',single_url):
		text_xpath = "//div[@class='main']"
	elif re.search('kmpex\.com',single_url):
		text_xpath = "//div[@class='portlet-body']"
	elif re.search('gzpec\.cn',single_url):
		text_xpath = "//div[@class='contents clear']"
	elif re.search('escn\.com\.cn',single_url):
		text_xpath = "//div[@class='entry']"
	elif re.search('sgcio\.com',single_url):
		text_xpath = "//div[@class='post']"
	else:
		text_xpath = '//body'

	return text_xpath


def download_from_url(url, outf='', text_xpath = '//body', nextpage_xpath = './/a[contains(., \'下一页\')]/ancestor::div[position()=1]'):
# url:			url to scrape
# outf:			new file
# text_xpath: 	text xpath

	print(url)

	if not re.search('^http',url):
		return ''

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

		if outf != '' :
		#	first-level call
			print(outf)
			# check for additional pages:
# 			print nextpage_xpath.encode('utf8')
			nextpage_found = found_text[0].find_elements_by_xpath(nextpage_xpath)
			if len(nextpage_found) > 0:		# -> with html
				print("...found some additional pages")
				links = nextpage_found[0].find_elements_by_xpath('.//a')
				all_src = [link.get_attribute("href") for link in links]
				all_src = list(OrderedDict.fromkeys(all_src))			# remove duplicates, retain order
				try:
					all_src = [x for x in all_src if x != url]		# remove head url
				except ValueError:
					pass
# 				print [src + u'\n' for src in all_src]
				for src in all_src:
# 					print src

					# call child pages...
					t_next = download_from_url(src, outf = '', text_xpath = text_xpath)

# 					t_next = u''
					text = text + t_next

			# 	let's write
			with io.open(outf + '.html', 'w', encoding='utf-8') as f:
				f.writelines(text)
		else:
		#	we are in sub-call
		#	return as text
			driver.close()
			return text

	else:
	#	no text found
		print('...nothing found for xpath="' + text_xpath + '"')
		driver.close()
		return ''

	driver.close()


if single_url != '':
	if nextpage_xpath:
		download_from_url(single_url, outf = outf, text_xpath = textpath_by_url(single_url), nextpage_xpath = nextpage_xpath)
	else:
		download_from_url(single_url, outf = outf, text_xpath = textpath_by_url(single_url))

else:
#	we have a pickle

	with open(outf + '.pickle', 'rb') as f:
		url_files = pickle.load(f)

	if os.path.exists(outf + '--text-completed.pickle'):
		with open(outf + '--text-completed.pickle', 'rb') as f:
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

		if nextpage_xpath:
			download_from_url(i[0], outf = outdir + i[1], text_xpath = textpath_by_url(i[0]), nextpage_xpath = nextpage_xpath)
		else:
			download_from_url(i[0], outf = outdir + i[1], text_xpath = textpath_by_url(i[0]))

		print('File ' + i[1] + ' completed\n')
		comp_files.append(i)

		# save completed files to file for later use
		with open(outf + '--text-completed.pickle','wb') as f:
			pickle.dump(comp_files, f, pickle.HIGHEST_PROTOCOL)
