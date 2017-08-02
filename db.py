#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

import config

def excute_no_query(sql,paras=()):
	#创建连接
	conn = pymysql.connect(host=config.ip_proxies_database_con_host, port=config.ip_proxies_database_con_port, user=config.ip_proxies_database_con_user, passwd=config.ip_proxies_database_con_passwd, db=config.ip_proxies_database_con_db)
	#创建游标
	cursor = conn.cursor()
	
	#执行SQL，并返回收影响行数
	effect_row = 0
	if len(paras)>0:
		effect_row=cursor.execute(sql,paras)
	else:
		effect_row=cursor.execute(sql)

	#提交，不然无法保存新建或者修改的数据
	conn.commit()
	  
	# 关闭游标
	cursor.close()
	# 关闭连接
	conn.close()
	return effect_row
def select(sql,paras=()):
	#创建连接
	conn = pymysql.connect(host=config.ip_proxies_database_con_host, port=config.ip_proxies_database_con_port, user=config.ip_proxies_database_con_user, passwd=config.ip_proxies_database_con_passwd, db=config.ip_proxies_database_con_db)
	#创建游标
	cursor = conn.cursor()
	
	#执行SQL，并返回收影响行数
	effect_row = 0
	if len(paras)>0:
		effect_row=cursor.execute(sql,paras)
	else:
		effect_row=cursor.execute(sql)

	result=cursor.fetchmany(effect_row)
	#提交，不然无法保存新建或者修改的数据
	conn.commit()
	  
	# 关闭游标
	cursor.close()
	# 关闭连接
	conn.close()
	return result
	
if __name__ == '__main__':
	sql='delete from ProxyIPs'
	effect_row=excute_no_query(sql)
	print 'effect_row:'+str(effect_row)