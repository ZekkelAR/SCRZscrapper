import requests
import re
import os
import sys
from bs4 import BeautifulSoup
import json
from rich.panel import Panel
from rich.progress import track
from time import sleep
from rich import print
from time import sleep
import time
import os,sys

def banner():
	print(Panel.fit("""
		[cyan]
███████╗ ██████╗██████╗ ███████╗
██╔════╝██╔════╝██╔══██╗╚══███╔╝
███████╗██║     ██████╔╝  ███╔╝ 
╚════██║██║     ██╔══██╗ ███╔╝  
███████║╚██████╗██║  ██║███████╗
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝
	 """, title="MOIRAI CORPORATION"))
	print(Panel.fit("""
[+] [bold red]Detik [white]Scrapper to JSON     .
[!] Author : Zekkel AR
		"""))



def url_request2(url,info):
	image_saved={}
	content_saved={}
	title_saved={}
	out_list = []
	art = ""
	#print("")
	req = requests.get(url).text
	grab_title = re.findall('<title>(.*?)</title>', req)
	for title in grab_title:
		title_saved=title
	soup = BeautifulSoup(req, 'html.parser')

	try:
		imeg_grab = BeautifulSoup(req, "html.parser")
		warning = imeg_grab.find('div', class_="detail__media")
		images = warning.find_all('img')
		example = images[0].attrs['src']
		#print('[x] Images : '+example)
		image_saved = example
	except:
		try:
			imeg_grab = BeautifulSoup(req, "html.parser")
			warning = imeg_grab.find('figure')
			images = warning.find('picture', class_="img_con lqd")

			mages2 = warning.find('img')
			example = mages2.attrs['src']
			#print('[!] Images : '+example)
		except:
			pass



	soup.div['class'] = 'detail__body-text itp_bodycontent'

	fac = []
	for sub_heading in soup.find_all('p'):
		art = sub_heading.text.strip()
		#print(sub_heading.text)
		fac.append(sub_heading.text.strip())										# Add content to array

	
	wopps = {"title":title_saved, "images":image_saved, "articles":fac}				# Format save to Json
	
	if info == 'last':
		jsonString = json.dumps(wopps)
		jsonFile = open("detik.json", "a")
		jsonFile.write(jsonString+'\n')
		jsonFile.close()
	else:
		jsonString = json.dumps(wopps)
		jsonFile = open("detik.json", "a")
		jsonFile.write(jsonString+','+'\n')
		jsonFile.close()
	





def search_complete():
	all_url = [] 																	 # save all url in array for calculate len
	pages = 1 																		 # pages on detik.com
	sloops = input('[x] Input ur Query : ')

	while(True):
		time.sleep(1)
		url = "https://www.detik.com/search/searchall?query={}&siteid=2&sortby=time&page={}" .format(sloops, pages)
		search = requests.get(url).text
		if '0 hasil ditemukan' in search: 											 # if page null, its mean no article in that page, and then break process
			break
		else:
			get_url_soup = BeautifulSoup(search, "html.parser") 					 # like requests.text, this for get content in url
			warning = get_url_soup.find('div', class_="list media_rows list-berita") # find div
			images = warning.find_all('article')	 								 # get article on div class list media_rows list-berita
			for images2 in images: 													 			
				ranz = images2.find_all('a') 										 # url of article is in a href, so this to find <a>
				for zzz in ranz:
					all_url.append(zzz['href'])										 # get href ( links )

			lenz = len(all_url)														 # check length url on array 
			siz = 1
			progress_bar = 1
			print(Panel.fit("Scraping Page {}" .format(pages)))
			print(Panel.fit("Grabbed {} URL" .format(len(all_url))))

			for example in track(all_url, total=lenz):
				if siz == lenz:
					url_request2(example, 'last')
				else:
					url_request2(example, 'nope')
				
				siz+=1
				time.sleep(1)
		all_url.clear()
		pages +=1
	

def search2():
	all_url=[]
	url = "https://www.detik.com/search/searchall?query=jokowi&siteid=2"
	search = requests.get(url).text
	get_url_soup = BeautifulSoup(search, "html.parser")
	warning = get_url_soup.find('div', class_="list media_rows list-berita")
	images = warning.find_all('article')
	for images2 in images:
		ranz = images2.find_all('a') 
		for zzz in ranz:
			all_url.append(zzz['href'])
	print(Panel.fit("""
[+] [green]Grabbing                   .
[white][!] Total Sites : {}
		""" .format(len(all_url))))
	
	lenz = len(all_url)
	siz = 1
	progress_bar = 1

	for example in track(all_url, total=lenz):
		if siz == lenz:
			url_request2(example, 'last')
		else:
			url_request2(example, 'nope')
		
		siz+=1
		time.sleep(1)


def main1():
	open('detik.json', 'a').write('['+'\n')
	search2();open('detik.json', 'a').write(']'+'\n')

def main2():
	open('detik.json', 'a').write('['+'\n')
	search_complete();open('detik.json', 'a').write(']'+'\n')


if __name__ == "__main__":
	os.system('cls')
	banner()
	main2()
