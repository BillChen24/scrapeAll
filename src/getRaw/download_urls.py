# download_urls.py
# -*- coding: utf-8 -*-
#	simple download routine for collecting urls (e.g., in pickle file)
# 	designed to be used with download_images.py, download_docs.py or download_text.py

from selenium import webdriver
import urllib.request, urllib.parse, urllib.error
import os.path, sys, imp
import pickle
import re
from collections import OrderedDict
import itertools

# UnicodeDecodeError: these little magic lines...
if sys.version_info <= (3,0):
	imp.reload(sys)
	sys.setdefaultencoding('utf8')



#Chrome Options
#	no image loading: https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)

def trim(string):
	return string.strip()

def download_from_url(url, src_regex = '.', link_regex = '.', outf='', nextpage_xpath = './/a[contains(., \'下一页\')]/ancestor::div[position()=1]'):
# src_regex:		only record links matching
# outf:				output pickle file
	print(url)
	driver=webdriver.Chrome(chrome_options=chromeOptions)
	driver.get(url)

	url_files = []
	links = driver.find_elements_by_tag_name('a')

	for link in links:
		src = link.get_attribute("href")

		if link.text != '':
			link_text = link.text
		else:
			link_text = 'TITLE'

		if src != None and re.search(src_regex,src) and re.search(link_regex,link_text):
			print(link.text)
			print(src)

			if src.endswith("#"):
				# javascript call
				src = link.get_attribute("onclick")
				if src == None:
					continue
			url_files.append([src, link_text])

	if outf == 'TITLE':
		# code to set output equal to HTML title
		outf = (driver.title)
		if outf == '':
			# returned nothing, set to url fname (without .html)
			outf = os.path.splitext(os.path.split(url)[1])[0]
# 				print outf

	if outf != '':
	#	first-level call => check for addtn'l pages
		print(outf)
		if nextpage_xpath != '':
			nextpage_found = driver.find_elements_by_xpath(nextpage_xpath)
		else:
			nextpage_found = []
		if len(nextpage_found) > 0:
			print("...found some additional pages")
			links = nextpage_found[0].find_elements_by_xpath('.//a')
			all_src = [link.get_attribute("href") for link in links]
			all_src = list(OrderedDict.fromkeys(all_src))			# remove duplicates, retain order
			try:
				all_src = [x for x in all_src if ((x != url) & (x != None))]		# remove head url and blanks
			except ValueError:
				pass
# 				print [src + u'\n' for src in all_src]
			for src in all_src:
				print(src)

				# call child pages...
				url_next = download_from_url(src, outf = '', src_regex = src_regex, nextpage_xpath=nextpage_xpath)

				url_files.extend(url_next)


		# let's write:
		with open(outf + '.pickle','wb') as f:
			pickle.dump(url_files, f, pickle.HIGHEST_PROTOCOL)
# 		print [u[0]+u'\n' for u in url_files]
		print('Output to ' + outf)

	else:
	#	we are in sub-call
	#	return as text
		driver.close()
		return url_files

	driver.close()

def download_from_urls(urls, src_regex = '.', outf='', nextpage_xpath = './/a[contains(., \'下一页\')]/ancestor::div[position()=1]'):
	url_files = []
	for url in urls:
		download_from_url(url, src_regex = src_regex, outf=outf, nextpage_xpath = nextpage_xpath)
		# for each, load up urls and add to list
		with open(outf + '.pickle', 'rb') as f:
			us = pickle.load(f)
			for u in us:
				url_files.append(u)

	# write combined list
	with open(outf + '.pickle','wb') as f:
		pickle.dump(url_files, f, pickle.HIGHEST_PROTOCOL)
	print(url_files)

def decode_links(outf, urlbase, src_rep):
#	add urlbase to relative paths

	with open(outf + '.pickle', 'rb') as f:
		links = pickle.load(f)

	urls = [re.search(src_rep,l[0]) for l in links if l != None]
	urls = [urlbase + m.group(1) for m in urls]
	titles = [l[1] for l in links if l != None]
# 	print urls
# 	print titles
	urls = [[urls[i],titles[i]] for i in range(1,len(urls))]
# 	print urls

	with open(outf + '.pickle','wb') as f:
		pickle.dump(urls, f, pickle.HIGHEST_PROTOCOL)





#####
## IMW exchange news site: http://www.nmgdlxw.cn/dbjy.asp

#   WILL BE UPDATED:
# start_url = 'http://www.nmgdlxw.cn/moredb.asp?id=%BD%BB%D2%D7%B3%C9%BD%BB'
# download_from_url(start_url, src_regex = '/read.asp', outf='IM-jiaoyi')

# start_url = 'http://www.nmgdlxw.cn/moredb.asp?id=%BD%BB%D2%D7%BD%E1%CB%E3'
# download_from_url(start_url, src_regex = '/read.asp', outf='IM-jiaoyi-jiesuan')


#	HISTORICAL:
# start_url = 'http://www.nmgdlxw.cn/more.asp?dqys=2&id=%BD%BB%D2%D7%B3%C9%BD%BB'
# download_from_url(start_url, src_regex = '/read.asp', outf='IM-jiaoyi-2')


## IM Grid monthly dispatch reports
# start_url = 'http://www.impc.com.cn/lmsy/ydfw/sgtd/index.htm'
# download_from_url(start_url, src_regex = 'sgtd\/\d', outf='IM-sangong')

# start_url = 'http://www.impc.com.cn/lmsy/ydfw/sgtd/index1.htm'
# download_from_url(start_url, src_regex = 'sgtd\/\d', outf='IM-sangong-2')

# ## CEC
# start_url = 'http://www.cec.org.cn/guihuayutongji/tongjxinxi/niandushuju/'
# download_from_url(start_url, src_regex = 'niandushuju\/\d', outf='CEC-niandushuju')


# ## Kunming exchange xinxipilu
# loop
# base_url = 'http://www.kmpex.com/web/kmdljyzx/56?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_coA4&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo='
# urls = []
# outf = 'Kunming-xinxipilu'
# for i in range(1,4,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# 	urls.append(base_url + str(i))
# print urls
# download_from_urls(urls, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-xinxipilu', nextpage_xpath = '')


# indiv pages
# start_url = 'http://www.kmpex.com/web/kmdljyzx/56?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_coA4&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo=1'
# download_from_url(start_url, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-xinxipilu')

# # can't auto find next page links...argh:
# start_url = 'http://www.kmpex.com/web/kmdljyzx/56?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_coA4&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo=2'
# download_from_url(start_url, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-xinxipilu-2')
# start_url = 'http://www.kmpex.com/web/kmdljyzx/56?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_coA4&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo=3'
# download_from_url(start_url, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-xinxipilu-3')
# start_url = 'http://www.kmpex.com/web/kmdljyzx/56?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_coA4&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo=4'
# download_from_url(start_url, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-xinxipilu-4')


# ## Kunming exchange jianbao
# loop
# base_url = 'http://www.kmpex.com/web/kmdljyzx/57?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_B5eP&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo='
# urls = []
# outf = 'Kunming-jianbao'
# for i in range(1,4,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# 	urls.append(base_url + str(i))
# print urls
# download_from_urls(urls, src_regex = 'kmdljyzx\/viewarticle\?', outf=outf, nextpage_xpath = '')

#   indiv pages:
# start_url = 'http://www.kmpex.com/web/kmdljyzx/57'
# download_from_url(start_url, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-jianbao')
# start_url = 'http://www.kmpex.com/web/kmdljyzx/57?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_B5eP&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo=2'
# download_from_url(start_url, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-jianbao-2')
# start_url = 'http://www.kmpex.com/web/kmdljyzx/57?p_p_id=customcolumnportlet_WAR_Cms_Eipportlet_INSTANCE_B5eP&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&pageNo=3'
# download_from_url(start_url, src_regex = 'kmdljyzx\/viewarticle\?', outf='Kunming-jianbao-3')


# ## Guangzhou exchange tongzhigonggao
# base_url = 'https://www.gzpec.cn/main/indexnew.do?method=toList&INFOTYPE=2&page='
# urls = []
# outf = 'guangzhou-tongzhigonggao'
# # for i in range(1,14,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# for i in range(1,4,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# 	urls.append(base_url + str(i))
# print urls
# download_from_urls(urls, src_regex = 'indexnew\.do?', outf=outf, nextpage_xpath = '')


# ## Guangzhou exchange zhengcefagui
# base_url = 'https://www.gzpec.cn/main/indexnew.do?method=toList&INFOTYPE=1&page='
# urls = []
# outf = 'guangzhou-zhengcefagui'
# for i in range(1,3,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# 	urls.append(base_url + str(i))
# print urls
# download_from_urls(urls, src_regex = 'indexnew\.do\?.*INFOID', outf=outf, nextpage_xpath = '')


# ## Gansu exchange
# base_url = 'https://61.178.40.43/pmos/index/infoList.jsp?itemid=213000&title=%E4%BA%A4%E6%98%93%E5%85%AC%E5%91%8A&curpage='
# urlbase = "http://61.178.40.43/pmos/index/infoContent3.jsp?guid="
# src_rep = "logNews\(\"(.+?)\""
# urls = []
# outf = 'gansu-jiaoyigonggao'
# for i in range(1,13,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# 	urls.append(base_url + str(i))
# print urls
# download_from_urls(urls, src_regex = '#', outf=outf, nextpage_xpath = '')
#
# decode_links(outf = outf, urlbase = urlbase, src_rep = src_rep)


# ## Gansu xinwen dongtai (handful of recent dispatch reports)
# base_url = 'https://61.178.40.43/pmos/index/infoList.jsp?itemid=212000&curpage='
# urlbase = "http://61.178.40.43/pmos/index/infoContent3.jsp?guid="
# src_rep = "logNews\(\"(.+?)\""
# urls = []
# outf = 'gansu-xinwendongtai'
# for i in range(1,2,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# 	urls.append(base_url + str(i))
# print urls
# download_from_urls(urls, src_regex = '#', outf=outf, nextpage_xpath = '') # extract links (with item id in url field)
# decode_links(outf = outf, urlbase = urlbase, src_rep = src_rep)  # convert item id to page urls (add relative paths) resave pickle

# ## Gansu xinwen dongtai (handful of recent dispatch reports)
# base_url = 'https://61.178.40.43/pmos/index/infoList.jsp?itemid=212000&curpage='
# urlbase = "http://61.178.40.43/pmos/index/infoContent3.jsp?guid="
# src_rep = "logNews\(\"(.+?)\""
# urls = []
# outf = 'gansu-xinwendongtai'
# for i in range(1,2,1):  # range(x,y,d): all indices ≥ x and < y, increment by d
# 	urls.append(base_url + str(i))
# print urls
# download_from_urls(urls, src_regex = '#', outf=outf, nextpage_xpath = '') # extract links (with item id in url field)
# decode_links(outf = outf, urlbase = urlbase, src_rep = src_rep)  # convert item id to page urls (add relative paths) resave pickle

## CCTD monthly coal reports
outf = 'cctd-monthly-r3'
url = 'https://www.cctd.com.cn/list-46-1.html'
urlbase = "https://www.cctd.com.cn/"
download_from_url(url, src_regex = 'show-', outf=outf, link_regex = '电煤价格指数') # extract links (with item id in url field)
