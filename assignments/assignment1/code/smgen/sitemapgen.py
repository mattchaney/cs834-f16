import sys
import os
import argparse
import datetime
import time
import urllib

from os.path import getmtime, isdir, isfile

import xml.dom.minidom as md


def append(doc, urlset, loc, lastmod, changefreq, priority='0.5'):
	url = doc.createElement('url')
	urlset.appendChild(url)

	loc_element = doc.createElement('loc')
	loc_element.appendChild(doc.createTextNode(loc))
	url.appendChild(loc_element)

	lastmod_element = doc.createElement('lastmod')
	lastmod_element.appendChild(doc.createTextNode(lastmod))
	url.appendChild(lastmod_element)
	
	changefreq_element = doc.createElement('changefreq')
	changefreq_element.appendChild(doc.createTextNode(changefreq))
	url.appendChild(changefreq_element)

	priority_element = doc.createElement('priority')
	priority_element.appendChild(doc.createTextNode(priority))
	url.appendChild(priority_element)


YEAR = 3.154e+7
MONTH = 2.592e+6
WEEK = 604800.0
DAY = 86400
HOUR = 3600
MINUTE = 60

def estimate_changefreq(posixtime):
	timenow = time.time()
	delta = timenow - posixtime
	if delta > YEAR:
		return 'never'
	elif delta > MONTH:
		return 'yearly'
	elif delta > WEEK:
		return 'monthly'
	elif delta > DAY:
		return 'weekly'
	elif delta > HOUR:
		return 'daily'
	elif delta > MINUTE:
		return 'hourly'
	else:
		return 'always' 


def convertdate(posixtime):
	return datetime.datetime.utcfromtimestamp(posixtime).strftime('%Y-%m-%d')


def delve(root, folder, doc, urlset):
	items = os.listdir(root + folder)
	for item in items:
		filepath = root + folder + item
		if isfile(filepath):
			loc = args.host + urllib.quote(folder + item)
			lastmodsecs = getmtime(filepath)
			lastmod = convertdate(lastmodsecs)
			changefreq = estimate_changefreq(lastmodsecs)
			append(doc, urlset, loc, lastmod, changefreq)
		elif isdir(filepath):
			delve(root, folder + item + os.sep, doc, urlset)


def test(doc, urlset):
	append(doc, urlset, 'www.google.com', '2016-09-17', 'always', '0.8')
	append(doc, urlset, 'www.duckduckgo.com', '2016-09-17', 'daily')
	print doc.toprettyxml()


if __name__ == '__main__':
	# parse arguments
	parser = argparse.ArgumentParser('site map generator')
	parser.add_argument(
		'-test',
		'-t',
		action='store_true')
	parser.add_argument(
		'--path',
		'-p',
		default='.')
	parser.add_argument(
		'--host',
		default='http://www.example.com/')
	args = parser.parse_args()

	# create a document
	doc = md.Document()
	urlset = doc.createElement('urlset')
	urlset.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
	doc.appendChild(urlset)

	# if desired, perform simple test and return
	if args.test:
		test(doc, urlset)
		sys.exit(0)

	# parse path from args
	path = args.path
	if path[len(path)-1] != os.sep:
		path = path + os.sep

	# iterate over all items in doc
	delve(path, '', doc, urlset)

	print doc.toprettyxml()
