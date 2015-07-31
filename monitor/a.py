#coding=utf-8
from test import settings_local
from zabbixapi import *

def zabbixindex():
	zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
	groupinfo = zbxapi.all_hostgroupid_get()
	hostsinfo = zbxapi.all_hostid_get()
	
	for group in groupinfo:
		groupid = group['groupid']
		groupname = group['name']
	
	for host in hostsinfo:
		hostid = host['hostid']
		hostname = host['host']
		hostgraphs = zbxapi.hostgraphall_get(hostname)
	
		for graph in hostgraphs:
			graphid = graph['graphid']
			graphname = graph['name']
			flag = DrawTree.objects.filter(graphid=graphid)


print zabbixindex()
