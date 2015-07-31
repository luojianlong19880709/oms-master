# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from asset.form import *
from asset.models import *
from asset.asset_info import *
from oms.mysql import db_operate
from oms import settings_local
from oms.models import *
from asset.zabbixapi import *
from oms import settings_local
import re,time,os

def host_list_manage(request,id=None):
    """
    Manage Host List
    """
    user = request.user
    zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])

    if id:
	host_list = get_object_or_404(HostList_yz1, pk=id)
	action = 'edit'
    	page_name = '编辑主机'
#    	db = db_operate() 
#    	sql = 'select ip from asset_hostlist where id = %s' % (id)
#    	ret = db.mysql_command(settings_local.OMS_MYSQL,sql)
    else:
        host_list = HostList_yz1()
        action = 'add'   
        page_name = '新增主机'

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
	db = db_operate()
	sql = 'select ip from asset_hostlist_yz1 where id = %s' % (id)
	ret = db.mysql_command(settings_local.OMS_MYSQL,sql)[0]
        if delete:
           Message.objects.create(type='host', action='manage', action_ip=ret, content='主机下架')
           host_list = get_object_or_404(HostList_yz1, pk=id)
           host_list.delete()
	   zbxapi.host_delete(ret)
           return HttpResponseRedirect(reverse('host_list'))

    if request.method == 'POST': 
        form = HostsListForm(request.POST,instance=host_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('host_list'))
	    db = db_operate()
	    sql = 'select ip from asset_hostlist_yz1 where id = %s' % (id)
            ret = db.mysql_command(settings_local.OMS_MYSQL,sql)[0]
            if operate:
                if operate == 'update':
                    form.save()
                    Message.objects.create(type='host', action='manage', action_ip=ret, content='主机信息更新')
                    return HttpResponseRedirect(reverse('host_list'))
                else:
                    pass
    else:
        form = HostsListForm(instance=host_list)

    return render_to_response('host_manage.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
           },context_instance=RequestContext(request))


def host_list_manage_yz2(request,id=None):
    """
    Manage Host List
    """
    user = request.user
    zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
    if id:
        host_list = get_object_or_404(HostList_yz2, pk=id)
        action = 'edit'
        page_name = '编辑主机'
#       db = db_operate() 
#       sql = 'select ip from asset_hostlist where id = %s' % (id)
#       ret = db.mysql_command(settings_local.OMS_MYSQL,sql)
    else:
        host_list = HostList_yz2()
        action = 'add'
        page_name = '新增主机'

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
        db = db_operate()
        sql = 'select ip from asset_hostlist_yz2 where id = %s' % (id)
        ret = db.mysql_command(settings_local.OMS_MYSQL,sql)[0]
        if delete:
           Message.objects.create(type='host', action='manage', action_ip=ret, content='主机下架')
           host_list = get_object_or_404(HostList_yz2, pk=id)
           host_list.delete()
	   zbxapi.host_delete(ret)
           return HttpResponseRedirect(reverse('host_list_yz2'))

    if request.method == 'POST':
        form = HostsListForm_yz2(request.POST,instance=host_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('host_list_yz2'))
	    db = db_operate()
	    sql = 'select ip from asset_hostlist_yz2 where id = %s' % (id)
	    ret = db.mysql_command(settings_local.OMS_MYSQL,sql)[0]
            if operate:
                if operate == 'update':
                    form.save()
                    Message.objects.create(type='host', action='manage', action_ip=ret, content='主机信息更新')
                    return HttpResponseRedirect(reverse('host_list_yz2'))
                else:
                    pass
    else:
        form = HostsListForm_yz2(instance=host_list)

    return render_to_response('host_manage_yz2.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
           },context_instance=RequestContext(request))


def host_list_manage_cer(request,id=None):
    """
    Manage Host List
    """
    user = request.user
    zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
    if id:
        host_list = get_object_or_404(HostList_cer, pk=id)
        action = 'edit'
        page_name = '编辑主机'
#       db = db_operate() 
#       sql = 'select ip from asset_hostlist where id = %s' % (id)
#       ret = db.mysql_command(settings_local.OMS_MYSQL,sql)
    else:
        host_list = HostList_cer()
        action = 'add'
        page_name = '新增主机'

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
        db = db_operate()
        sql = 'select ip from asset_hostlist_cer where id = %s' % (id)
        ret = db.mysql_command(settings_local.OMS_MYSQL,sql)[0]
        if delete:
           Message.objects.create(type='host', action='manage', action_ip=ret, content='主机下架')
           host_list = get_object_or_404(HostList_cer, pk=id)
           host_list.delete()
	   zbxapi.host_delete(ret)
           return HttpResponseRedirect(reverse('host_list_cer'))

    if request.method == 'POST':
        form = HostsListForm_cer(request.POST,instance=host_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('host_list_cer'))
            db = db_operate()
            sql = 'select ip from asset_hostlist_cer where id = %s' % (id)
            ret = db.mysql_command(settings_local.OMS_MYSQL,sql)[0]
            if operate:
                if operate == 'update':
                    form.save()
                    Message.objects.create(type='host', action='manage', action_ip=ret, content='主机信息更新')
                    return HttpResponseRedirect(reverse('host_list_cer'))
                else:
                    pass
    else:
    	form = HostsListForm_cer(instance=host_list)

    return render_to_response('host_manage_cer.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
           },context_instance=RequestContext(request))


def host_monitor_add(request,id):
	host_list = HostList_yz1()

	zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
	hostip = HostList_yz1.objects.filter(id=id).values('ip')[0].values()[0]
	hostgroupName = HostList_yz1.objects.filter(id=id).values('application')[0].values()[0]
	re = str(hostgroupName).split(' ')[-1]

	try:
		if re == 'datanode': 
			zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Datanode port,Templates Tasktracker port')
		elif re == 'namenode':
			zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Namenode port')

		elif re == 'JobTracker':
			zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Jobtracker port')
                else:
			zbxapi.host_create(hostip,hostgroupName,'Template OS Linux')
		
	except Exception as e:
		print "Error is %s",e

	else:
		HostList_yz1.objects.filter(id=id).update(monitor='是')
		Message.objects.create(type='host', action='add_monitor', action_ip=hostip, content='添加监控')
	
	return HttpResponseRedirect(reverse('host_list'))


def host_monitor_add_yz2(request,id):

        zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
        hostip = HostList_yz2.objects.filter(id=id).values('ip')[0].values()[0]
        hostgroupName = HostList_yz2.objects.filter(id=id).values('application')[0].values()[0]
        re = str(hostgroupName).split(' ')[-1]

        try:
                if re == 'nodemanager':
                        zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Datanode port,Templates Nodemanager port')
                elif re == 'namenode':
                        zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Namenode port')

                elif re == 'resourceManager':
                        zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Resourcemanager port')

		elif re == 'client':
			zbxapi.host_create(hostip,hostgroupName,'Template OS Linux')

        except Exception as e:
                print "Error is %s",e

        else:
                HostList_yz2.objects.filter(id=id).update(monitor='是')
                Message.objects.create(type='host', action='add_monitor', action_ip=hostip, content='添加监控')

        return HttpResponseRedirect(reverse('host_list_yz2'))

def host_monitor_add_cer(request,id):

        zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
        hostip = HostList_cer.objects.filter(id=id).values('ip')[0].values()[0]
        hostgroupName = HostList_cer.objects.filter(id=id).values('application')[0].values()[0]
        re = str(hostgroupName).split(' ')[-1]

        try:
                if re == 'datanode':
                        zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Datanode port,Templates Tasktracker port')
                elif re == 'namenode':
                        zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Namenode port')

                elif re == 'JobTracker':
                        zbxapi.host_create(hostip,hostgroupName,'Template OS Linux,Templates Jobtracker port')

		else:
			zbxapi.host_create(hostip,hostgroupName,'Template OS Linux')

        except Exception as e:
                print "Error is %s",e

        else:
                HostList_cer.objects.filter(id=id).update(monitor='是')
                Message.objects.create(type='host', action='add_monitor', action_ip=hostip, content='添加监控')

        return HttpResponseRedirect(reverse('host_list_cer'))



def host_monitor_delete(request,id):
	
	zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
	hostip = HostList_yz1.objects.filter(id=id).values('ip')[0].values()[0]
	if hostip:
		zbxapi.host_delete(hostip)
  	        HostList_yz1.objects.filter(id=id).update(monitor='否')
		Message.objects.create(type='host', action='delete_monitor', action_ip=hostip, content='删除监控')
	
	
	return HttpResponseRedirect(reverse('host_list'))


def host_monitor_delete_yz2(request,id):

        zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
        hostip = HostList_yz2.objects.filter(id=id).values('ip')[0].values()[0]
        if hostip:
                zbxapi.host_delete(hostip)
		HostList_yz2.objects.filter(id=id).update(monitor='否')
                Message.objects.create(type='host', action='delete_monitor', action_ip=hostip, content='删除监控')


        return HttpResponseRedirect(reverse('host_list_yz2'))


def host_monitor_delete_cer(request,id):

        zbxapi = zabbix_api(url=settings_local.ZABBIX_API['url'],header=settings_local.ZABBIX_API['header'],user=settings_local.ZABBIX_API['user'],password=settings_local.ZABBIX_API['password'])
        hostip = HostList_cer.objects.filter(id=id).values('ip')[0].values()[0]
        if hostip:
                zbxapi.host_delete(hostip)
		HostList_cer.objects.filter(id=id).update(monitor='否')
                Message.objects.create(type='host', action='delete_monitor', action_ip=hostip, content='删除监控')


        return HttpResponseRedirect(reverse('host_list_cer'))




def host_list(request):
    """
    List all Hosts
    """
    user = request.user
    form = search(request.POST)
    all_host = HostList_yz1.objects.all()  
    host_count = HostList_yz1.objects.all().count()  
    paginator = Paginator(all_host,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_host = paginator.page(page)
    except:
        all_host = paginator.page(paginator.num_pages)
 

    if request.method == 'POST':
	if form.is_valid():
		ip = form.cleaned_data['search']
		if request.POST.has_key('abc'):
			all_host = HostList_yz1.objects.filter(ip=ip)

    			return render_to_response('host_list.html', {'all_host_list': all_host,'form':form},context_instance=RequestContext(request))
	
	

    return render_to_response('host_list.html', {'all_host_list': all_host, 'page': page, 'paginator':paginator,'form':form,'host_count':host_count},context_instance=RequestContext(request))


def host_list_yz2(request):
    """
    List all Hosts
    """
    user = request.user
    form = search(request.POST)
    all_host = HostList_yz2.objects.all()
    host_count = HostList_yz2.objects.all().count()
    paginator = Paginator(all_host,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_host = paginator.page(page)
    except :
        all_host = paginator.page(paginator.num_pages)

    if request.method == 'POST':
	if form.is_valid():
		ip = form.cleaned_data['search']
		if request.POST.has_key('abc'):
			all_host = HostList_yz2.objects.filter(ip=ip)
		
			return render_to_response('host_list_yz2.html',{'all_host_list': all_host, 'page': page, 'paginator':paginator,'form':form},context_instance=RequestContext(request))

    return render_to_response('host_list_yz2.html', {'all_host_list': all_host, 'page': page, 'paginator':paginator,'form':form,'host_count':host_count},context_instance=RequestContext(request))




def host_list_cer(request):
    """
    List all Hosts
    """
    user = request.user
    form = search(request.POST)
    all_host = HostList_cer.objects.all()
    host_count = HostList_cer.objects.all().count()
    paginator = Paginator(all_host,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_host = paginator.page(page)
    except :
        all_host = paginator.page(paginator.num_pages)

    if request.method == 'POST':
    	if form.is_valid():
		ip = form.cleaned_data['search']
		if request.POST.has_key('abc'):
			all_host = HostList_cer.objects.filter(ip=ip)
			
			return render_to_response('host_list_cer.html',{'all_host_list': all_host, 'page': page, 'paginator':paginator,'form':form},context_instance=RequestContext(request))




    return render_to_response('host_list_cer.html',{'all_host_list': all_host, 'page': page, 'paginator':paginator,'form':form,'host_count':host_count},context_instance=RequestContext(request))




def get_server_asset(request):
    """
    Get information service assets
    """
    
    if request.method == 'GET':
        action = request.get_full_path().split('=')[1]
        if action == 'flush':
            hostlist_sql = 'select hostname from asset_hostlist'
            server_sql = 'select hostname from asset_serverasset'
            db = db_operate() 
            host_ret = db.mysql_command(settings.OMS_MYSQL,hostlist_sql)
            server_ret = db.mysql_command(settings.OMS_MYSQL,server_sql)
            obj = [i for i in host_ret if i not in server_ret]       #主机列表数据与服务器资产数据IP做差集，数据更新时只更新差集，避免一次性更新全部
            ret = multitle_collect(obj)
            for i in ret:
                ServerAsset.objects.create(manufacturer=i[0], productname=i[1], service_tag=i[2], cpu_model=i[3], cpu_nums=i[4], cpu_groups=i[5],mem=i[6], disk=i[7], raid=i[8], hostname=i[9], ip=i[10], macaddress=i[11], os=i[12], virtual=i[13], idc_name=i[14])
        Message.objects.create(type='server', action='manage', action_ip='扫描', content='录入%s服务器软件、硬件信息' % (obj))
          
        return HttpResponseRedirect(reverse('server_asset_list'))

def server_asset_list(request):
    """
    List all Server Asset Info
    """

    user = request.user
    all_server = ServerAsset.objects.all()
    paginator = Paginator(all_server,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_server = paginator.page(page)
    except :
        all_server = paginator.page(paginator.num_pages)

    return render_to_response('server_asset_list.html', {'all_server_list': all_server, 'page': page, 'paginator':paginator})

def network_device_discovery(request,id=None):
    """
    Manage Network Device
    """
    
    if id:
        device_list = get_object_or_404(NetworkAsset, pk=id)
        action = 'edit'
        page_name = '编辑设备'
    else:
        device_list = NetworkAsset()
        action = 'add'   
        page_name = '新增设备'

    if request.method == 'POST': 
        form = NetworkAssetForm(request.POST,instance=device_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('network_device_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    return HttpResponseRedirect(reverse('network_device_list'))
                else:
                    pass
    else:
        form = NetworkAssetForm(instance=device_list)

    return render_to_response('device_manage.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
           },context_instance=RequestContext(request)) 

def network_device_list(request):
    """
    List all Network Device
    """
  
    user = request.user
    all_device = NetworkAsset.objects.all()
    paginator = Paginator(all_device,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_device = paginator.page(page)
    except :
        all_device = paginator.page(paginator.num_pages)

    return render_to_response('device_list.html', {'all_device_list': all_device, 'page': page, 'paginator':paginator})    

def idc_asset_manage(request,id=None):
    """
    Manage IDC
    """

    if id:
        idc_list = get_object_or_404(IdcAsset, pk=id)
        action = 'edit'
        page_name = '编辑IDC机房'
    else:
        idc_list = IdcAsset()
        action = 'add'
        page_name = '新增IDC机房'

    if request.method == 'POST':
        form = IdcAssetForm(request.POST,instance=idc_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('idc_asset_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    return HttpResponseRedirect(reverse('idc_asset_list'))
                else:
                    pass
    else:
        form = IdcAssetForm(instance=idc_list)

    return render_to_response('idc_manage.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
           },context_instance=RequestContext(request))

def idc_asset_list(request):
    """
    List all IDC
    """

    user = request.user
    all_idc = IdcAsset.objects.all()
    paginator = Paginator(all_idc,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_idc = paginator.page(page)
    except :
        all_idc = paginator.page(paginator.num_pages)

    return render_to_response('idc_list.html', {'all_idc_list': all_idc, 'page': page, 'paginator':paginator})



