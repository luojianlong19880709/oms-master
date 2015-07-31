#!/usr/bin/env python
#coding=utf-8
import rrdtool
import threading
import os
import datetime,time
import createsub
from time import ctime
from test import settings_local
from zabbixapi import *

def rrd_create(grinfo):

	
	bashdir = "/data1/rrd/"
	path = bashdir + grinfo[0]['hostid'] + "/"
	if not os.path.exists(path):
		os.makedirs(path)
	for graphid in grinfo:

		rrdname = str(path + graphid['graphid'] + '.rrd')
		timeDaysAgo = (datetime.datetime.now() - datetime.timedelta(days = 730))
		startStamp = str(int(time.mktime(timeDaysAgo.timetuple())))
		DS = []
		for sub in grinfo:
			DStmp = str('DS:' + sub['itemid'] + ':GAUGE:120:0:U')
			DS.append(DStmp)

		if len(DS) == 1: createsub.Item01(rrdname, startStamp, DS)
		elif len(DS) == 2: createsub.Item02(rrdname, startStamp, DS)
		elif len(DS) == 3: createsub.Item03(rrdname, startStamp, DS)
		elif len(DS) == 4: createsub.Item04(rrdname, startStamp, DS)
		elif len(DS) == 5: createsub.Item05(rrdname, startStamp, DS)
		elif len(DS) == 6: createsub.Item06(rrdname, startStamp, DS)
		elif len(DS) == 7: createsub.Item07(rrdname, startStamp, DS)
		elif len(DS) == 8: createsub.Item08(rrdname, startStamp, DS)
		elif len(DS) == 9: createsub.Item09(rrdname, startStamp, DS)
		elif len(DS) == 10: createsub.Item10(rrdname, startStamp, DS)
		elif len(DS) == 11: createsub.Item11(rrdname, startStamp, DS)
		elif len(DS) == 12: createsub.Item12(rrdname, startStamp, DS)
		elif len(DS) == 13: createsub.Item13(rrdname, startStamp, DS)
		elif len(DS) == 14: createsub.Item14(rrdname, startStamp, DS)
		elif len(DS) == 15: createsub.Item15(rrdname, startStamp, DS)
		elif len(DS) == 16: createsub.Item16(rrdname, startStamp, DS)
		elif len(DS) == 17: createsub.Item17(rrdname, startStamp, DS)
		elif len(DS) == 18: createsub.Item18(rrdname, startStamp, DS)
		elif len(DS) == 19: createsub.Item19(rrdname, startStamp, DS)
		elif len(DS) == 20: createsub.Item20(rrdname, startStamp, DS)
		elif len(DS) == 21: createsub.Item21(rrdname, startStamp, DS)
		elif len(DS) == 22: createsub.Item22(rrdname, startStamp, DS)
		





def rrd_update(rrdfile, data):
	subtmp = data.pop()
	ds = ''
	vl = 'N:'
	for sub in data:
		ds = ds + sub['itemid'] + ":"
		vl = vl + sub['lastvalue'] + ":"
	ds = ds + subtmp['itemid']
	vl = vl + subtmp['lastvalue']
	rrdfile = str(rrdfile)
	ds = str(ds)
	vl = str(vl)
	rrdtool.update(rrdfile, '--template', ds, vl)


def items_get(host):

	zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
	bashdir = "/data1/rrd/"
	graphids = zbxapi.hostgraph_get(host)
	hostid = zbxapi.host_get(host)
	for graphid in graphids:
		graphitem = zbxapi.items_get(graphid)
		rrdfile = bashdir + hostid + "/" + str(graphid) + '.rrd'
		if os.path.isfile(rrdfile):
			data = []
			for item in graphitem:
				tmp = {'itemid':item['itemid'],'lastvalue':item['lastvalue']}
				data.append(tmp)
			rrd_update(rrdfile, data)
		else:
			grinfo = []
			for item in graphitem:
				tmp = {'hostid': hostid, 'graphid': graphid, 'itemid': item['itemid']}

				grinfo.append(tmp)
			rrd_create(grinfo)





def main():
	threads = []
	zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
#	hosts =  all_hostid_get()
	hosts = ['10.4.18.25','10.4.18.22','10.4.19.98','10.4.19.92','10.4.19.91','10.5.18.230','10.5.18.229','10.4.18.32']
	host_list = []
	for i in hosts:
	#	host_list.append(i['host'])
		host_list.append(i)
	keys = host_list
	numkey = len(keys)
	loop = 0
	for i in range(0, numkey, 30):
		nkeys = range(loop*30, (loop+1)*30, 1)
		for i in nkeys:
			if i >= numkey:
				break
			else:
				t = threading.Thread(target=items_get, args=(keys[i],))
				threads.append(t)
		for i in nkeys:
			if i >= numkey:
				break
			else:
				threads[i].start()
	
		for i in nkeys:
			if i >= numkey:
				break
			threads[i].join()
		loop = loop + 1


print main()

