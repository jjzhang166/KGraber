#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup as BS
from urllib import request
import re
import json
import os

file_content=open('./personal.htm').read()

soup=BS(file_content, 'html.parser')

playlist=soup.find_all('div',class_='mod_playlist__box')

songs=dict()

playlistFile = open("playlist.txt","w")

process = 0.0
total = len(playlist)

for item in playlist:
	title=item.div.p.span.string
	title=title.strip()
	url=item.a.attrs['href']
	songPageHTML=request.urlopen(url).read()	
	content=songPageHTML.decode()
	patstr=r'<script.+(window.__DATA__.+{.+}).+</script>'
	pattern=re.compile(patstr)
	match=re.search(pattern,content)
	if(match):
		process = process + 1
		ratio = process / total * 100
		print("process: [%5.2f%%]" %(ratio)) 
		info=match.group(1)
		jsonStr=info[info.index('=')+1:len(info)]
		songInfo=json.loads(jsonStr)
		playUrl=songInfo['detail']['playurl']
		songs[title]=playUrl
		line = playUrl + '\t' + title + '.m4a\n'
		playlistFile.write(line)
	else:
		print("The regular expression has failed! Please contact author!<824219521@qq.com>")
		exit(1)

playlistFile.close()

