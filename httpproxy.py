#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import httplib
import threading
import codecs
import uuid
import json
from datetime import datetime, date, time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import db_ProxyIPs
import model_ProxyIPs


def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
	countNum = 0
	requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
	print 'get ip proxies from website of :'+targeturl+',starting:'+str(datetime.now())
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
	print 'get ip proxies from website of :'+targeturl+',starting:'+str(datetime.now())
	return countNum

def verifyProxyList():
	models=db_ProxyIPs.get_not_verified_proxis()
	all_thread=[]
	for model in models:
		protocol= model.Protocol
		ip      = model.IP
		port    = model.Port
		ID= model.ID
		#验证代理的有效性
		#verifyProxyIP(ip,port,ID)
		thread=threading.Thread(target=verifyProxyIP,args=(ip,port,ID))
		all_thread.append(thread)
		thread.start()
	for thread in all_thread:
		thread.join()

def verifyProxyIP(ip,port,ID=''):
	try:
		requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
		myurl = 'http://www.baidu.com/'
		conn = httplib.HTTPConnection(ip, port, timeout=5.0)
		conn.request(method = 'GET', url = myurl, headers = requestHeader )
		res = conn.getresponse()
		if ID=='' or ID==None:
			db_ProxyIPs.update_last_verified_time(ID,str(datetime.now()))
		else:
			db_ProxyIPs.update_last_verified_time_by_ip(str(datetime.now()),ip,port)
		print "+++Success:" + ip + ":" + str(port)

	except BaseException as e:
		print "---Failure:" + ip + ":" + str(port)
		if ID=='' or ID==None:
			db_ProxyIPs.move(ID)
		else:
			db_ProxyIPs.remove_by_ip(ip,port)

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
	
def get_verified_proxy():
	newest_verified_proxy_ips=db_ProxyIPs.get_newest_verified_proxy_ips(1)
	if len(newest_verified_proxy_ips)>0:
		return newest_verified_proxy_ips[0];

def get_proxies_from_web():
	print "get proxy ip starting:"+str(datetime.now())
	proxynum = getProxyList("http://www.xicidaili.com/nn/")
	print "CN-Anonymity：" + str(proxynum)
	# proxynum = getProxyList("http://www.xicidaili.com/nt/")
	# print u"国内透明：" + str(proxynum)
	# proxynum = getProxyList("http://www.xicidaili.com/wn/")
	# print u"国外高匿：" + str(proxynum)
	# proxynum = getProxyList("http://www.xicidaili.com/wt/")
	# print u"国外透明：" + str(proxynum)

	print "get proxy ip finish,"+str(datetime.now())
	print "\n verify ip proxy start:"+str(datetime.now())
	verifyProxyList()

	print "\n verify ip proxy finish:"+str(datetime.now())
	print str(datetime.now())

if __name__ == '__main__':
	get_proxies_from_web()

