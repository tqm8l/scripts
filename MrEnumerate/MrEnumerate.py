import collections
import string
import sys
import os
from urllib.parse import urldefrag, urljoin, urlparse
import bs4
import requests
import argparse
import shodan
import time


def crawler(startpage, maxpages=100, singledomain=True):
    pagequeue = collections.deque()
    pagequeue.append(startpage)
    crawled = []
    domain = urlparse(startpage).netloc if singledomain else None
    pages = 0
    failed = 0
    sess = requests.session()
    while pages < maxpages and pagequeue:
        url = pagequeue.popleft()
        try:
            response = sess.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
            print("*FAILED*:", url)
            failed += 1
            continue
        if not response.headers["content-type"].startswith("text/html"):
            continue
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        crawled.append(url)
        pages += 1
        if pagehandler(url, response, soup):
            links = getlinks(url, domain, soup)
            for link in links:
                if not url_in_list(link, crawled) and not url_in_list(link, pagequeue):
                    pagequeue.append(link)

    print("{0} pages crawled, {1} links failed.".format(pages, failed))

def getlinks(pageurl, domain, soup):
    links = [a.attrs.get("href") for a in soup.select("a[href]")]
    links = [urldefrag(link)[0] for link in links]
    links = [link for link in links if link]
    links = [
        link if bool(urlparse(link).netloc) else urljoin(pageurl, link)
        for link in links
    ]
    if domain:
        links = [link for link in links if samedomain(urlparse(link).netloc, domain)]
    return links

def pagehandler(pageurl, pageresponse, soup):
    print("Crawling:" + pageurl + " ({0} bytes)".format(len(pageresponse.text)))
    return True

def samedomain(netloc1, netloc2):
    domain1 = netloc1.lower()
    if "." in domain1:
        domain1 = domain1.split(".")[-2] + "." + domain1.split(".")[-1]
    domain2 = netloc2.lower()
    if "." in domain2:
        domain2 = domain2.split(".")[-2] + "." + domain2.split(".")[-1]

    return domain1 == domain2

def url_in_list(url, listobj):
    http_version = url.replace("https://", "http://")
    https_version = url.replace("http://", "https://")
    return (http_version in listobj) or (https_version in listobj)

def searchShodan(asset, key):
	req = requests.get("https://api.shodan.io/shodan/host/"+asset+"?key="+key+"")
	response = req.json()
	ports = response['ports']
	print(asset , ports)

def commander(command, file):
	with open(file, 'r') as file:
	 	for line in file:
	 		os.system(command + ' ' + line)

def CommonUDPports():
    os.system("nmap -sU -p 123,161,500 -script '*snmp* or ntp-monlist' -iL " + args.iL)

def bbw():
    with open(args.iL, 'r') as file:
        for url in file:
            with open(args.bbw, 'r') as file2:
                for payload in file2:
                    time.sleep(5)
                    new = url + payload
                    command = 'curl -I '+ new.replace('\n', '')
                    print('command === ',command)
                    result = os.system(str(command))

parser = argparse.ArgumentParser(description='MrEnumerate Help')
parser.add_argument('-c', help='Web Crawler',metavar='URL')
parser.add_argument('-s', help='Port Scan with Shodan API',metavar='apikey')
parser.add_argument('-iL', help='Provide File of Targets',metavar='file.txt')
parser.add_argument('-k', help='Iterate Through File. Eg -k enum4linux -a -iL scope.txt',metavar='command')
parser.add_argument('-eu', help='Nmap Scan Common External UDP Ports',action="store_const",const=True)
parser.add_argument('-bbw', help='Bug Bounty Directory Wordlist Brute Force ',metavar='wordlist.txt')
args = parser.parse_args()

if (args.c):
	startpage = args.c
	crawler(startpage, maxpages=100)
if (args.s and args.iL):
	key = args.s
	with open(args.iL, 'r') as file:
		for line in file:
			asset = line
			searchShodan(asset,key)
if (args.k and args.iL):
	command = args.k
	file = args.iL
	commander(command, file)
if (args.eu and args.iL):
    CommonUDPports()
if (args.bbw and args.iL):
    bbw()
