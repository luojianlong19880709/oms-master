# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# import views
from asset.views import *
from monitor.views import *
from oms.views import index
from installed.views import system_install_managed,system_install_list,system_install,system_install_record
from deploy.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^oms/admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^asset/host_list/$', host_list, name='host_list'),
    url(r'^asset/host_list_yz2/$', host_list_yz2, name='host_list_yz2'),
    url(r'^asset/host_list_cer/$', host_list_cer, name='host_list_cer'),
    url(r'^asset/add_host/$', host_list_manage, name='add_host'),
    url(r'^asset/add_host_yz2/$', host_list_manage_yz2, name='add_host_yz2'),
    url(r'^asset/add_host_cer/$', host_list_manage_cer, name='add_host_cer'),
    url(r'^asset/host_delete/$', host_list_manage, name='host_delete'),
    url(r'^asset/host_delete_yz2/$', host_list_manage_yz2, name='host_delete_yz2'),
    url(r'^asset/host_delete_cer/$', host_list_manage_cer, name='host_delete_cer'),
    url(r'^asset/host_manage/(?P<id>\d+)/$', host_list_manage, name='host_manage'),
    url(r'^asset/host_manage_yz2/(?P<id>\d+)/$', host_list_manage_yz2, name='host_manage_yz2'),
    url(r'^asset/host_manage_cer/(?P<id>\d+)/$', host_list_manage_cer, name='host_manage_cer'),
    url(r'^asset/host_monitor_add/(?P<id>\d+)/$', host_monitor_add, name='host_monitor_add'),
    url(r'^asset/host_monitor_add_yz2/(?P<id>\d+)/$', host_monitor_add_yz2, name='host_monitor_add_yz2'),
    url(r'^asset/host_monitor_add_cer/(?P<id>\d+)/$', host_monitor_add_cer, name='host_monitor_add_cer'),
    url(r'^asset/host_monitor_delete/(?P<id>\d+)/$', host_monitor_delete, name='host_monitor_delete'),
    url(r'^asset/host_monitor_delete_yz2/(?P<id>\d+)/$', host_monitor_delete_yz2, name='host_monitor_delete_yz2'),
    url(r'^asset/host_monitor_delete_cer/(?P<id>\d+)/$', host_monitor_delete_cer, name='host_monitor_delete_cer'),
    url(r'^monitor/zabbixindex/$', zabbixindex, name='zabbixindex'),
    url(r'^monitor/zabbixdraw/$', zabbixdraw, name='zabbixdraw'),
    url(r'^monitor/drawall/$', drawall, name='drawall'),
    url(r'^asset/server_asset/$', server_asset_list, name='server_asset_list'),
    url(r'^asset/server_get/$', get_server_asset, name='get_server_asset'),
    url(r'^asset/device_list/$', network_device_list, name='network_device_list'),
    url(r'^asset/device_add/$', network_device_discovery, name='add_device'),
    url(r'^asset/idc_list/$', idc_asset_list, name='idc_asset_list'),
    url(r'^asset/add_idc/$', idc_asset_manage, name='add_idc'),
    url(r'^install/install_list/$', system_install_list, name='install_list'),
    url(r'^install/install_manage/(?P<id>\d+)/$', system_install_managed, name='install_manage'),
    url(r'^install/system_install/$',system_install, name='system_install'),
    url(r'^install/install_record/$',system_install_record, name='install_record'),
    url(r'^deploy/key_list/$', salt_key_list, name='key_list'),
    url(r'^deploy/key_delete/$', salt_delete_key, name='delete_key'),
    url(r'^deploy/key_accept/$', salt_accept_key, name='accept_key'),
    url(r'^deploy/module_deploy/$', module_deploy, name='module_deploy'),
    url(r'^deploy/remote_execution/$', remote_execution, name='remote_execution'),
    url(r'^deploy/remote_execution_yz2/$', remote_execution_yz2, name='remote_execution_yz2'),
    url(r'^deploy/remote_execution_cer/$', remote_execution_cer, name='remote_execution_cer'),
    url(r'^deploy/code_deploy/$', code_deploy, name='code_deploy'),
)
