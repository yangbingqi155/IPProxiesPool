#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import httplib
import threading
import sys
import codecs
import uuid
import json
from datetime import datetime, date, time

import db_ProxyIPs
import model_ProxyIPs
reload(sys)
sys.setdefaultencoding('utf-8')


lock = threading.Lock()

def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
    countNum = 0
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    print u'获取IP代理,来自'+targeturl+','+str(datetime.now())
    for page in range(1,2):
        url = targeturl + str(page)
        #print url
        request = urllib2.Request(url, headers=requestHeader)
        html_doc = urllib2.urlopen(request).read()
    
        soup = BeautifulSoup(html_doc, "html.parser")
        #print soup
        trs = soup.find('table', id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            #国家
            if tds[0].find('img') is None :
                nation = 'Unknow'
                locate = 'Unknow'
            else:
                nation =   tds[0].find('img')['alt'].strip()
                locate  =   tds[3].text.strip()
            ip      =   tds[1].text.strip()
            port    =   tds[2].text.strip()
            anony   =   tds[4].text.strip()
            protocol=   tds[5].text.strip()
            speed   =   tds[6].find('div')['title'].strip()
            time    =   tds[8].text.strip()
            
            model=model_ProxyIPs.ProxyIPsModel()
            model.ID=str(uuid.uuid1())
            model.IP=ip
            model.Country=nation.upper()
            model.Port=int(port)
            model.ServerAddresss=''
            model.Anonymity='anonymous' if anony==u'高匿' else ''
            model.Protocol=protocol
            model.Speed=float(speed.replace(u"秒",""))
            model.ConnectSpeed=0
            model.LastVerifiedTime=str(datetime.now())
            model.IsVerified=0
            db_ProxyIPs.add(model)
            #print '%s=%s:%s' % (protocol, ip, port)
            countNum += 1
    print u'获取IP代理成功,来自'+targeturl+','+str(datetime.now())
    return countNum

def verifyProxyList():
    #验证代理的有效性
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    myurl = 'http://www.baidu.com/'
    models=db_ProxyIPs.get_not_verified_proxis()
    for model in models:
        protocol= model.Protocol
        ip      = model.IP
        port    = model.Port
        ID= model.ID
        try:
            conn = httplib.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method = 'GET', url = myurl, headers = requestHeader )
            res = conn.getresponse()
            db_ProxyIPs.update_last_verified_time(ID,str(datetime.now()))
            print "+++Success:" + ip + ":" + str(port)
            
        except BaseException as e:
            #print e
            print "---Failure:" + ip + ":" + str(port)
            db_ProxyIPs.move(ID)
def get_verified_proxies_num():
	pass
	# outFile = open('verified.txt')
	# i=0
	# while True:
		# lock.acquire()
		# ll = outFile.readline().strip()
		# lock.release()
		# if len(ll) == 0: break
		# i=i+1
	# return i
def get_verified_proxy(index):
	pass
	# outFile = open('verified.txt')
	# i=0
	# while True:
		# lock.acquire()
		# ll = outFile.readline().strip()
		# lock.release()
		# if len(ll) == 0: break
		# if index==i:
			# line = ll.strip().split('|')
			# protocol= str(line[5])
			# address= protocol+"://"+line[1]+":"+str(line[2])
			# return {protocol:address}
		# i=i+1
def get_proxies_from_web():
    print u"开始获取代理,"
    print datetime.now()
    # proxynum = getProxyList("http://www.xicidaili.com/nn/")
    # print u"国内高匿：" + str(proxynum)
    # proxynum = getProxyList("http://www.xicidaili.com/nt/")
    # print u"国内透明：" + str(proxynum)
    # proxynum = getProxyList("http://www.xicidaili.com/wn/")
    # print u"国外高匿：" + str(proxynum)
    # proxynum = getProxyList("http://www.xicidaili.com/wt/")
    # print u"国外透明：" + str(proxynum)

    print u"结束获取代理,"
    print datetime.now()
    print u"\n验证代理的有效性："
    print datetime.now()
    verifyProxyList()
    # all_thread = []
    # for i in range(50):
        # t = threading.Thread(target=verifyProxyList)
        # all_thread.append(t)
        # t.start()
        
    # for t in all_thread:
        # t.join()
    
    print u"代理获取完毕."
    print datetime.now()

if __name__ == '__main__':
    get_proxies_from_web()

