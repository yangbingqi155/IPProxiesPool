#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import model_ProxyIPs

def data_2_model(data):
	model=model_ProxyIPs.ProxyIPsModel()
	model.ID=data[0]
	model.IP=data[1]
	model.Country=data[2]
	model.Port=data[3]
	model.ServerAddresss=data[4]
	model.Anonymity=data[5]
	model.Protocol=data[6]
	model.Speed=data[7]
	model.ConnectSpeed=data[8]
	model.LastVerifiedTime=data[9]
	model.IsVeried=data[10]

def add(model):
	if len(get(model.IP,model.Port,model.Protocol))<=0:
		sql="INSERT INTO `IPProxies`.`ProxyIPs`(`ID`,`IP`,`Country`,`Port`,`ServerAddresss`,`Anonymity`,`Protocol`,`Speed`,`ConnectSpeed`,`LastVerifiedTime`,`IsVeried`)VALUES(%s,%s,%s,%d,%s,%s,%s,%.2f,%.2f,%s,%s);"
		paras=(model.ID,model.IP,model.Country,model.Port,model.ServerAddresss,model.Anonymity,model.Protocol,model.Speed,model.ConnectSpeed,model.LastVerifiedTime,model.IsVeried)
		return True if db.excute_no_query(sql,paras)>0 else False
	else:
		return True
def move(ID):
	sql="delete `IPProxies`.`ProxyIPs` where ID=%s"
	paras=(ID)
	return True if db.excute_no_query(sql,paras)>0 else False
	
def update_last_verified_time(ID,last_verified_time):
	sql="update `IPProxies`.`ProxyIPs` set LastVerifiedTime=%s where ID=%s"
	paras=(last_verified_time,ID)
	return True if db.excute_no_query(sql,paras)>0 else False

def get_newest_proxy_ips(top_num):
	sql="select top %d *from `IPProxies`.`ProxyIPs` where IsVeried=1 order by LastVerifiedTime desc"
	paras=(top_num)
	data=db.select(sql,paras)
	models=[]
	for item in data:
		model=data_2_model(item)
		models.append(model)
	return models

def get(ip,port,protocol):
	sql="select *from `IPProxies`.`ProxyIPs` where ip=%s and port=%d and protocol=%s"
	paras=(ip,port,protocol)
	data=db.select(sql,paras)
	return data

def get_not_verified_proxis(top_num):
	sql="select top %d *from `IPProxies`.`ProxyIPs` where IsVeried=0 order by LastVerifiedTime desc"
	paras=(top_num)
	data=db.select(sql,paras)
	models=[]
	for item in data:
		model=data_2_model(item)
		models.append(model)
	return models