# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from monitor.models import *
from oms.mysql import db_operate
from oms import settings_local
from oms.models import *
from monitor.zabbixapi import *
from oms import settings_local
import re,time,os
import drawrrd


def zabbixindex(request):
	if request.method == 'GET':
		if request.GET == '':
			zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
			hostsinfo = zbxapi.all_hostid_get()
			"""
			for group in groupinfo:
				groupid = group['groupid']
				groupname = group['name']
			"""	
				
			for host in hostsinfo:
				hostid = host['hostid']
				hostname = host['host']
				groupname = zbxapi.all_hostgroupid_get(hostid)
				hostgraphs = zbxapi.hostgraphall_get(hostname)
				
				for graph in hostgraphs:
					graphid = graph['graphid']
					graphname = graph['name']
					flag = DrawTree.objects.filter(graphid=graphid)
					
					if not flag:
						draw = '1'
						if 'YZ hadoop namenode' in groupname:
							type = '1'
							classname = 'YZ hadoop namenode'
						elif 'YZ hadoop jobtracker' in groupname:
							type = '2'
							classname = 'YZ hadoop jobtracker'
						elif 'YZ hadoop datanode' in groupname:
							type = '3'
							classname = 'YZ hadoop datanode'
						elif 'YZ hadoop hbase master' in groupname:
							type = '4'
							classname = 'YZ hadoop hbase master'
						elif 'YZ hadoop 2.0 namenode' in groupname:
							type = '5'
							classname = 'YZ hadoop 2.0 namenode'
						elif 'YZ hadoop 2.0 nodemanager' in groupname:
							type = '6'
							classname = 'YZ hadoop 2.0 nodemanager'
						elif 'YZ hadoop 2.0 resourcemanager' in groupname:
							type = '7'
							classname = 'YZ hadoop 2.0 resourcemanager'
						elif 'CER hadoop namenode' in groupname:
							type = '8'
							classname = 'CER hadoop namenode'
						elif 'CER hadoop JobTracker' in groupname:
							type = '9'
							classname = 'CER hadoop JobTracker'
						elif 'BJCER hadoop datanode' in groupname:
							type = '10'
							classname = 'BJCER hadoop datanode'
						else:
							classname = groupname
							type = '0'
						DrawTree.objects.create(classname=classname,hostname=hostname,hostid=hostid,graphid=graphid,graphname=graphname,draw=draw,type=type)
						itemsinfo = zbxapi.items_get(graphid)
						units = itemsinfo[0]['units']
						for item in itemsinfo:
							itemid = item['itemid']
							itemname = item['name']
							DrawGraphs.objects.create(graphid=graphid, itemid=itemid, itemname=itemname, units=units)
						
			return render_to_response('zabbixindex.html',{})
					
	sql = "select distinct classname from asset_drawtree where type!='0' and type!='3' and type!='6' and type!='10'"
	
	type = DrawTree.objects.getclass(sql)
	
	typelist = []
	for i in type:
		sql = "select distinct hostname,hostid,type from asset_drawtree where classname="+"'"+i[0]+"'"
		chosts = DrawTree.objects.getclass(sql)
		tmplist = []
		for chost in chosts:
			tmp = {'hostname': chost[0], 'hostid': chost[1]}
			tmplist.append(tmp)
		typelist.append({'type':i[0], 'host':tmplist, 'tflag': chost[2]})

	return render_to_response('zabbixindex.html',{'typelist':typelist})
			


def zabbixdraw(request):
	dir = '/data1/rrd'
	pngdir = r"/var/www/html/oms-master/static/images/rrdpng/"
	hostid = request.GET['hostid']
	type = request.GET['type']
	sql = "select hostid, graphid, graphname, hostname from asset_drawtree where hostid="+hostid+" and type="+type+" and draw='1'"
	graphs = DrawTree.objects.getclass(sql)
	pngs = []
	gdatas = []
	strtime = str(int(time.time()- 86400))
	for graph in graphs:
		hostid = graph[0]
		graphid = graph[1]
		graphname = graph[2]
		hostname = graph[3]
		rpath = dir + r"/" + hostid + r"/" + graphid + r".rrd"
		if not os.path.exists(pngdir + hostid + r"/"):
			os.makedirs(pngdir + hostid + r"/")
		pngname = pngdir + hostid + r"/" + graphid + r".png"
		sql = "select itemid,itemname,units from asset_drawgraphs where graphid="+graphid
		pitem = DrawGraphs.objects.getdata(sql)
		sql = "select cols from asset_drawdef where graphid="+graphid
		cols = DrawDef.objects.getdata(sql)
		if cols:
			cols = (cols[0][0].split(":"),)
		sql = "select types from asset_drawdef where graphid="+graphid
		itypes = DrawDef.objects.getdata(sql)
		if itypes:
			itypes = (itypes[0][0].split(":"),)
		gdata = {'pname':pngname, 'gname':graphname, 'rrdpath':rpath, 'pitem':pitem, 'graphid':graphid,'cols':cols, 'itypes':itypes, 'host':hostname, 'stime':strtime, 'flag':'Daily'}
		
		gdatas.append(gdata)
		pngs.append({'pngpath':str(pngname).replace(r"/var/www/html/oms-master", ''), 'graphid':graphid})
	drawrrd.drawmain(gdatas)	
	return render_to_response('zabbixdraw.html',{'pngs':pngs})



def drawall(request):
	gdatas = []
	pngs = []
	dir = r"/data1/rrd/"
	graphid = request.GET['graphid']
	sql = "select hostid, graphname, hostname from asset_drawtree where graphid="+graphid
	graph = DrawTree.objects.getclass(sql)
	hostid = graph[0][0]
	graphname = graph[0][1]
	hostname = graph[0][2]
	rpath = dir + hostid + r"/" + graphid + r".rrd"
	pngdir = r"/var/www/html/oms-master/static/images/rrdpng/cache"
	if not os.path.exists(pngdir + graphid):
		os.makedirs(pngdir + graphid + r"/")
	
	png2d = pngdir + graphid + r"/" + r"2d.png"
	pngs.append(str(png2d).replace(r"/var/www/html/oms-master", ''))
	png1w = pngdir + graphid + r"/" + r"1w.png"
	pngs.append(str(png1w).replace(r"/var/www/html/oms-master", ''))
	png1m = pngdir + graphid + r"/" + r"1m.png"
	pngs.append(str(png1m).replace(r"/var/www/html/oms-master", ''))
	png1y = pngdir + graphid + r"/" + r"1y.png"
	pngs.append(str(png1y).replace(r"/var/www/html/oms-master", ''))
	sql = "select itemid,itemname,units from asset_drawgraphs where graphid="+graphid
	pitem = DrawGraphs.objects.getdata(sql)
	sql = "select cols from asset_drawdef where graphid="+graphid
	cols = DrawDef.objects.getdata(sql)
	if cols:
		cols = (cols[0][0].split(":"),)
	sql = "select types from asset_drawdef where graphid="+graphid
	itypes = DrawDef.objects.getdata(sql)
	if itypes:
		itypes = (itypes[0][0].split(":"),)
	sql = "select itemid,itemname,units from asset_drawgraphs where graphid="+graphid
	pitem = DrawGraphs.objects.getdata(sql)
	strtime = str(int(time.time()- 86400))
	gdata = {'pname':png2d, 'gname':graphname, 'rrdpath':rpath, 'pitem':pitem, 'graphid':graphid, 'cols':cols, 'itypes':itypes, 'host':hostname, 'stime':strtime, 'flag':'Daily'}
	gdatas.append(gdata)
	strtime = str(int(time.time()- 604800))
	gdata = {'pname':png1w, 'gname':graphname, 'rrdpath':rpath, 'pitem':pitem, 'graphid':graphid, 'cols':cols, 'itypes':itypes, 'host':hostname, 'stime':strtime, 'flag':'Weekly'}
	gdatas.append(gdata)
	strtime = str(int(time.time()- 2592000))
	gdata = {'pname':png1m, 'gname':graphname, 'rrdpath':rpath, 'pitem':pitem, 'graphid':graphid, 'cols':cols, 'itypes':itypes, 'host':hostname, 'stime':strtime, 'flag':'Monthly'}
	gdatas.append(gdata)
	strtime = str(int(time.time()- 31536000))
	gdata = {'pname':png1y, 'gname':graphname, 'rrdpath':rpath, 'pitem':pitem, 'graphid':graphid, 'cols':cols, 'itypes':itypes, 'host':hostname, 'stime':strtime, 'flag':'Yearly'}
	gdatas.append(gdata)
	drawrrd.drawmain(gdatas)
	return render_to_response('drawall.html', {'pngs':pngs})

