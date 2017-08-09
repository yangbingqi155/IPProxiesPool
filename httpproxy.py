#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import httplib
import threading
import codecs
import uuid
import json
from datetime import datetime, date
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import db_ProxyIPs
import model_ProxyIPs

def proxyList2Models(proxyList):
	models=[]
	for proxy in proxyList:
		model=model_ProxyIPs.ProxyIPsModel()
		model.ID=str(uuid.uuid1())
		model.IP=proxy[0]
		model.Country=proxy[1].upper()
		model.Port=int(proxy[2])
		model.ServerAddresss=proxy[3]
		model.Anonymity=proxy[4]
		model.Protocol=proxy[5]
		model.Speed=proxy[6]
		model.ConnectSpeed=proxy[7]
		model.LastVerifiedTime=proxy[8]
		model.IsVerified=proxy[9]
		models.append(model)
	return models;
def getProxyListFromHidemy(targeturl="https://hidemy.name/en/proxy-list/?country=US&type=hs&anon=4#list"):
	countNum = 0
	requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
	url = targeturl
	print 'get ip proxies from website of :'+url+',starting:'+str(datetime.now())
	#print url
	request = urllib2.Request(url, headers=requestHeader)
	html_doc = urllib2.urlopen(request).read()

	soup = BeautifulSoup(html_doc, "html.parser")
	#print soup
	trs = soup.find('table',attrs={'class','proxy__t'}).find("tbody").find_all('tr')
	ipproxies=[]
	
	for tr in trs:
		tds = tr.find_all('td')
		ip      =   tds[0].text.strip()
		port    =   tds[1].text.strip()
		nation  =   tds[2].find("div").text.replace('&nbsp;','').strip()
		anony   =   tds[5].text.strip()
		protocol=   tds[4].text.strip()
		speed=   float(tds[3].find("div").find("p").text.replace("ms","").strip())

		anony='anonymous' if anony=='High' else anony
		nation='US' if nation.find('United States')>=0 else nation
		protocol=protocol.split(',')[0].strip() if protocol.find(",")>=0 else protocol
		locate=''
		ConnectSpeed=0
		LastVerifiedTime=str(datetime.now())
		IsVerified=0
		# print 'ip:'+ip+',anonymous:'+anony+",nation:"+nation+",protocol:"+protocol
		if anony!='anonymous' or nation!='US' or (protocol!='HTTPS' and protocol!='HTTP' ):
			continue
		ipproxy=[ip,nation,port,locate,anony,protocol,speed,ConnectSpeed,LastVerifiedTime,IsVerified]
		ipproxies.append(ipproxy)
		countNum += 1
	models=proxyList2Models(ipproxies)
	for model in models:
		db_ProxyIPs.add(model)
	return countNum
	
def getProxyListFromHidemyByPage(targeturl="https://hidemy.name/en/proxy-list/?start="):
	countNum = 0
	requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
	for page in range(0,15):
		url = targeturl+str(page*64)
		print 'get ip proxies from website of :'+url+',starting:'+str(datetime.now())
		#print url
		request = urllib2.Request(url, headers=requestHeader)
		html_doc = urllib2.urlopen(request).read()

		soup = BeautifulSoup(html_doc, "html.parser")
		#print soup
		trs = soup.find('table',attrs={'class','proxy__t'}).find("tbody").find_all('tr')
		ipproxies=[]
		
		for tr in trs:
			tds = tr.find_all('td')
			ip      =   tds[0].text.strip()
			port    =   tds[1].text.strip()
			nation  =   tds[2].find("div").text.strip()
			anony   =   tds[5].text.strip()
			protocol=   tds[4].text.strip()
			speed=   float(tds[3].find("div").find("p").text.replace("ms","").strip())

			anony='anonymous' if anony=='High' else anony
			nation='US' if nation=='United States' else nation
			protocol=protocol.split(',')[0].strip() if protocol.find(",")>=0 else protocol
			locate=''
			ConnectSpeed=0
			LastVerifiedTime=str(datetime.now())
			IsVerified=0
			#print 'anony:'+anony+",nation:"+nation+",protocol:"+protocol
			if anony!='anonymous' or nation!='US' or (protocol!='HTTPS' and protocol!='HTTP' ):
				continue
			ipproxy=[ip,nation,port,locate,anony,protocol,speed,ConnectSpeed,LastVerifiedTime,IsVerified]
			ipproxies.append(ipproxy)
			countNum += 1
		models=proxyList2Models(ipproxies)
		for model in models:
			db_ProxyIPs.add(model)
	
	return countNum
def getProxyListFromUSProxy(targeturl="https://www.us-proxy.org/"):
	countNum = 0
	requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
	print 'get ip proxies from website of :'+targeturl+',starting:'+str(datetime.now())
	url = targeturl
	#print url
	request = urllib2.Request(url, headers=requestHeader)
	html_doc = urllib2.urlopen(request).read()

	soup = BeautifulSoup(html_doc, "html.parser")
	#print soup
	trs = soup.find('table', id='proxylisttable').find("tbody").find_all('tr')
	ipproxies=[]
	for tr in trs:
		tds = tr.find_all('td')
		ip      =   tds[0].text.strip()
		port    =   tds[1].text.strip()
		nation  =   tds[2].text.strip()
		anony   =   tds[4].text.strip()
		protocol=   tds[6].text.strip()
		
		speed=0
		protocol='https' if protocol=='yes' else 'http'
		locate=''
		ConnectSpeed=0
		LastVerifiedTime=str(datetime.now())
		IsVerified=0
		if anony!='anonymous' or nation!='US':
			continue
		ipproxy=[ip,nation,port,locate,anony,protocol,speed,ConnectSpeed,LastVerifiedTime,IsVerified]
		ipproxies.append(ipproxy)
		countNum += 1
	models=proxyList2Models(ipproxies)
	for model in models:
		db_ProxyIPs.add(model)
	print 'get ip proxies from website of :'+targeturl+',starting:'+str(datetime.now())
	return countNum

def getProxyListFromXiCi(targeturl="http://www.xicidaili.com/nn/"):
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
		ipproxies=[]
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
			
			speed=float(speed.replace(u"秒",""))
			locate=''
			anony='anonymous' if anony==u'高匿' else ''
			ConnectSpeed=0
			LastVerifiedTime=str(datetime.now())
			IsVerified=0
			ipproxy=[ip,nation,port,locate,anony,protocol,speed,ConnectSpeed,LastVerifiedTime,IsVerified]
			ipproxies.append(ipproxy)
			countNum += 1
		models=proxyList2Models(ipproxies)
		for model in models:
			db_ProxyIPs.add(model)
	print 'get ip proxies from website of :'+targeturl+',starting:'+str(datetime.now())
	return countNum

def verifyProxyList():
	models=db_ProxyIPs.get_need_verified_proxis()
	all_thread=[]
	for model in models:
		protocol= model.Protocol
		ip      = model.IP
		port    = model.Port
		country = model.Country
		ID= model.ID
		#验证代理的有效性
		#verifyProxyIP(ip,port,ID)
		thread=threading.Thread(target=verifyProxyIP,args=(ip,port,country,ID))
		all_thread.append(thread)
		thread.start()
	for thread in all_thread:
		thread.join()

def verifyProxyIP(ip,port,country,ID=''):
	try:
		requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
		myurl = 'http://www.baidu.com/'
		if country.upper()=="US":
			myurl = 'http://www.amazon.in/'
		elif country.upper()=="CN":
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

def get_proxies_from_web():
	print "get proxy ip starting:"+str(datetime.now())
	# proxynum = getProxyListFromXiCi("http://www.xicidaili.com/nn/")
	# print "cn-anonymity：" + str(proxynum)
	
	proxynum = getProxyListFromUSProxy("https://www.us-proxy.org/")
	print "US-Anonymity:" + str(proxynum)
	
	proxynum = getProxyListFromUSProxy("https://free-proxy-list.net/")
	print "US-Anonymity:" + str(proxynum)
	
	proxynum = getProxyListFromHidemy("https://hidemy.name/en/proxy-list/?country=US&type=hs&anon=4#list")
	print "US-Anonymity:" + str(proxynum)
	
	print "get proxy ip finish,"+str(datetime.now())
	print "\n verify ip proxy start:"+str(datetime.now())
	verifyProxyList()

	print "\n verify ip proxy finish:"+str(datetime.now())
	
def sleeptime(hour,min,sec):
	return hour*3600 + min*60 + sec

if __name__ == '__main__':
	#get_proxies_from_web()
	second = sleeptime(0,0,10)
	while 1==1:
		get_proxies_from_web()
		time.sleep(second)
		print 'do action'

