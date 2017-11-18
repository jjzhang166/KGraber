#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup as BS
import time
import random
import requests
import urllib
import qrcode
import re
import json
import math
import os
import shutil

class KGraber:

    login_code_endPoint = r'http://cgi.kg.qq.com/fcgi-bin/fcg_login_code'
    login_scan_endPoint = r'http://node.kg.qq.com/cgi/fcgi-bin/fcg_scan_login'
    login_info_endPoint = r'http://node.kg.qq.com/cgi/fcgi-bin/fcg_login_info'
    user_homepage_endPoint = r'http://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage'
    
    def getTimestamp(self):
        return int(time.time()*1000)

    def getACSRFToken(self,e):
        t=5381
        for ch in e:
          t += (t << 5) + ord(ch)
        return 2147483647 & t

    def getpvid(self):
        return int(round(2147483647 * random.random()) * self.getTimestamp() % 1e10)

    def show_qrcode(self):
        query = {\
                'jsonpCallback':'response',
                'charset':'utf-8',
                'inCharset':'GB2312',
                'outCharset':'utf-8',
                'format':'',
                'g_tk':5381,
                 'g_tk_openkey':5381,
                'nocache':random.random()
                }
        self.query = query
        qrInfoUrl = self.login_code_endPoint + '?' + urllib.parse.urlencode(query)
        self.session = requests.Session()
        pvid = str(self.getpvid())
        self.session.cookies.set('pgv_pvid', pvid)
        self.session.cookies.set('pgv_info','ssid=s' + pvid)
        response = self.session.get(qrInfoUrl).content.decode('utf-8')
        self.qrsig = self.session.cookies.get('qrsig')
        startIndex = len(query['jsonpCallback']) + 1
        endIndex = len(response)-1
        response = response[startIndex : endIndex]
        response = eval(response)
        code = response['code']
        if code == 0:
            data = response['data']
            self.code = data['code']
            self.sig = data['sig']
    
            qrInfo =  r'http://kg.qq.com/m.html?' + urllib.parse.urlencode(data)
            qrImg = qrcode.make(qrInfo)
            qrImg.show('Please use the QuMinKeGe App Scan and logged in')
            input('If you have scaned the qrcode with App and logged in, enter any key to continue')
        else:
            print("Can not get the qrInfo")

    def scan_login(self):
            payload = {
                'uin':0,
                'loginUin':0,
                'hostUin':0,
                'format':'fs',
                'inCharset':'GB2312',
                'outCharset':'utf-8',
                'notice':0,
                'platform':'activity',
                'needNewCode':0,
                'g_tk':5381,
                'g_tk_openkey':5381,
                'code':self.code,
                'sig':self.sig,
                'g_tk_qrsig':self.getACSRFToken(self.qrsig),
                'qzreferrer':'http://kg.qq.com/'
            }
            pvid = str(self.getpvid())
            headers = {
                'Host': 'node.kg.qq.com',
                'Connection': 'keep-alive',
                'Content-Length': '315',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://imgcache.qq.com',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://imgcache.qq.com/music/miniportal_v4/tool/html/fp_utf8.html',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cookie': 'pgv_pvid=%s; pgv_info=ssid=s%s; qrsig=%s' % (pvid,pvid,self.qrsig)
            }
            scan_login_url = self.login_scan_endPoint + '?' + urllib.parse.urlencode({'g_tk':5381})
            self.session.post(scan_login_url,data = payload,headers=headers).content.decode('utf-8')

    def login_info(self):
        self.g_tk_openkey = self.getACSRFToken(self.session.cookies.get('openkey'))
        self.query['g_tk_openkey'] = self.g_tk_openkey
        login_info_url = self.login_info_endPoint + '?' + urllib.parse.urlencode(self.query)
        response = self.session.get(login_info_url).content.decode('utf-8')
        self.uid = self.session.cookies.get('muid')

 
    def getAllSongs(self):
        self.ugclist = {}
        flag = True
        while flag :
            pageLen = math.ceil(len(self.ugclist) / 8) + 1 
            query = {
                    'jsonpCallback':'response',
                    'g_tk':5381,
                    'outCharset':'utf-8',
                    'format':'jsonp',
                    'type':'get_ugc',
                    'start':pageLen,
                    'num':8,
                    'touin':'',
                    'share_uid':self.uid,
                    'g_tk_openkey':self.g_tk_openkey,
                    '_':self.getTimestamp()
                    }
            user_songs_url = self.user_homepage_endPoint + '?' + urllib.parse.urlencode(query)
            response = requests.get(user_songs_url).content.decode('utf-8')
            startIndex = len(query['jsonpCallback']) + 1
            endIndex = len(response)-1
            response = response[startIndex : endIndex]
            response = json.loads(response)
            if response['code'] == 0:
                for item in response['data']['ugclist']:
                    self.ugclist[item['shareid']]=item['title']
                flag = response['data']['has_more'] == 1
        self.downloadSongs()

    def downloadSongs(self):

        save_dir = 'songs'
        if os.path.isdir(save_dir):
            shutil.rmtree(save_dir)
        os.mkdir(save_dir)

        def getSong(sid,title):
            url= 'http://node.kg.qq.com/play?s=%s&g_f=personal' % sid
            content=requests.get(url).content.decode('utf-8')
            patstr=r'<script.+(window.__DATA__.+{.+}).+</script>'
            pattern=re.compile(patstr)
            match=re.search(pattern,content)
            playUrl = ''
            if(match):
                info=match.group(1)
                jsonStr=info[info.index('=')+1:len(info)]
                songInfo=json.loads(jsonStr)
                playUrl=songInfo['detail']['playurl']
                path = urllib.parse.urlparse(playUrl).path
                query = urllib.parse.urlparse(playUrl).query
                query = urllib.parse.parse_qs(query)
                if 'fname' in query:
                    fname = query['fname'][0]
                    ext = fname[fname.rfind('.'):]
                else:
                    ext = path[path.rfind('.'):]
                filename = title + ext

                print('Download: %s' % filename)
                r = requests.get(playUrl) 
                save_file = save_dir +'/' + filename
                with open(save_file, "wb") as song:
                    song.write(r.content)
                    song.close()
                
        for sid,title in self.ugclist.items():
            getSong(sid,title)

        print('Download Completed! The songs directory store all your songs, enjoy it! ;-D')

    def grabeSongs(self):
        self.show_qrcode()
        self.scan_login()
        self.login_info()
        self.getAllSongs()
   

if __name__ == '__main__':
    KGraber().grabeSongs()
    







