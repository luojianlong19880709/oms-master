#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import urllib2
from urllib2 import URLError

class zabbix_api:
	def __init__(self,url,header,user,password):
		self.__url = url
		self.__header = header
		self.__user = user
		self.__password = password

	def user_login(self):
		
		data = json.dumps({
				"jsonrpc": "2.0",
				"method": "user.login",
				"params": { 
                                  "user": self.__user, 
                                  "password": self.__password 
                                  }, 
                       		"id": 0 
				})
		request = urllib2.Request(self.__url, data)
		
		for key in self.__header:
			request.add_header(key, self.__header[key])
			

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "认证错误", e.code 
		
		else:
			response = json.loads(result.read())
			result.close()
			self.authID = response['result']
			return self.authID

	def host_get(self,hostName):
		
		data = json.dumps({
				"jsonrpc": "2.0",
				"method": "host.get",
				"params": {
					"output": ["hostid","name","status","host"],
					"filter": {"host":hostName},
					
					},
				"auth": self.user_login(),
				"id": 1
				
				})
		request = urllib2.Request(self.__url, data)
		
		for key in self.__header:
			request.add_header(key, self.__header[key])
		
		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.' 
				print 'Reason: ', e.reason 
			
			elif hasattr(e, 'code'):
				print 'The server could not fulfill the request.'
				print 'Error code: ', e.code 


		else:
			response = json.loads(result.read()) 
		#	print response
			result.close() 
			
		#	print "主机数量为 %s" %(len(response['result'])) 

			for host in response['result']:
				hostid = host['hostid']
		
				return hostid

	def template_get(self,templateName=''):
		data =  json.dumps({
					"jsonrpc": "2.0",
					"method": "template.get",
					"params": {
							"output": ['templateid','name'],
							"filter": {
								"name": templateName
							}
					},
					"auth": self.user_login(),
					"id": 1,
					
				})
	
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)
		except URLError  as e:
			print "Error as", e

		else:
			response = json.loads(result.read())
			result.close()
		
		templateid = response['result']

		return templateid[0]['templateid']	

	def hostgroup_get(self,hostgroupName=''):
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "hostgroup.get",
					"params": {
							"output": ['groupid','name'],
							"filter": {
								"name": hostgroupName
							}
						},
					"auth": self.user_login(),
					"id": 1,
				})

		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as",e

		else:
			response = json.loads(result.read())
			result.close()

		hostgroupid = response['result']
	
		return hostgroupid[0]['groupid']


	def host_create(self,hostip,hostgroupName,templateName):
		if self.host_get(hostip):
			print "该主机已经添加"
			sys.exit(1)
		group_list = []
		template_list = []
		for i in hostgroupName.split(','):
			var = {}
			var['groupid'] = self.hostgroup_get(i)
			group_list.append(var)
		for i in templateName.split(','):
			var = {}
			var['templateid'] = self.template_get(i)
			template_list.append(var)
			
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "host.create",
					"params": {
						"host": hostip,
						"interfaces": [
							{
						 
							"type": 1,
						 	"main": 1,
						 	"useip": 1,
						 	"ip": hostip,
							"dns": "",
							"port": "10050"		
					 
							}
						],
						"groups": group_list,
							
						"templates": template_list,
										
						},
					"auth": self.user_login(),
					"id": 1
				})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])

		try:
			result = urllib2.urlopen(request)
		except Error as e:
			print "Error as", e
		
		else:
			response = json.loads(result.read())
			print response
			result.close()

	def host_delete(self,hostip):
		hostid_list = []
		for i in hostip.split(','):
			var = {}
			var['hostid'] = self.host_get(i)
			hostid_list.append(var)


		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "host.delete",
					"params": hostid_list,
					"auth": self.user_login(),
					"id": 1
				
				})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		
		try:
			result = urllib2.urlopen(request)
		except Error as e:
			print "Error as", e
		else:
			result.close()

	def hostgraph_get(self,hostip):
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "host.get",
					"params":{
						"selectGraphs": ['graphid','name'],
						"filter": {"host": hostip}
					},

					"auth": self.user_login(),
					"id": 1

				})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])

		try:
			result = urllib2.urlopen(request)
		
		except Error as e:
			print "Error as", e

		else:
			response = json.loads(result.read())
			list = response['result'][0]['graphs']
			
			graph = []
			for i in list:
				graph.append(i['graphid'])
			result.close()
			return graph
	
	def hostgraphall_get(self,hostip):
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "host.get",
					"params": {
						"selectGraphs": ['graphid','name'],
						"filter": {"host": hostip}
					},
					"auth": self.user_login(),
					"id": 1
				})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)
		except Error as e:
			print "Error as", e
		
		else:
			response = json.loads(result.read())
			result.close()
			return response['result'][0]['graphs']

	def items_get(self,graphids):
	#	hostid = self.host_get(hostip)
	#	graphids = self.hostgraph_get(hostip)[0]['graphid']
	#	hostid = self.graphitem_get(graphid)
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "item.get",
					"params":{
						"output": ["itemid","units","lastvalue","lastclock","value_type","delay","name","key_"],
						"graphids": graphids,
						"sortfield": "name"
					},
					"auth": self.user_login(),
					"id": 1
					})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)

		except Error as e:
			print "Error as", e
		
		else:
			response = json.loads(result.read())
			result.close()
			tmp = response['result']
			items = []
			for value in tmp:
				if "$" in value['name']:
					name0 = value['key_'].split('[')[1].split(']')[0].replace(',', '')
					name1 = value['name'].split()
					if "CPU" in name1:
						name1.pop(-2)
						name1.insert(1,name0)
					elif "free" in name0:
						name0 = name0.replace('free',' free')
						name1.pop()
						name1.append(name0)
					elif "total" in name0:
						name0 = name0.replace('total',' total')
						name1.pop()
						name1.append(name0)
					else:
						name1.pop()
						name1.append(name0)
					name = ' '.join(name1)
					tmpitems = {'itemid':value['itemid'],'delay':value['delay'],'units':value['units'],'name':name,'value_type':value['value_type'],'lastclock':value['lastclock'],'lastvalue':value['lastvalue']}
			
				else:
					tmpitems = {'itemid':value['itemid'],'delay':value['delay'],'units':value['units'],'name':value['name'],'value_type':value['value_type'],'lastclock':value['lastclock'],'lastvalue':value['lastvalue']}
				items.append(tmpitems)
			return items
			
	def history_get(self,hostip):
		itemsids = []
		items = self.items_get(hostip)

		for i in items:
			itemsids.append(i['itemid'])

		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "history.get",
					"params": {
						"output": "extend",
						"history": 0,
						"itemsids": itemsids,
						"sortfield": "clock",
						"sortorder": "DESC",
						"limit": 10

						},
					"auth": self.user_login(),
					"id": 1
				})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)
		except Error as e:
			print "Error as", e

		else:
			response = json.loads(result.read())
			result.close()
			return response
	def graphitem_get(self,graphid):
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "graphitem.get",
					"params": {
						"output": "extend",
						"expandData": 1,
						"graphids": graphid
					},
					"auth": self.user_login(),
					"id": 1
				})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)
		except Error as e:
			print "Error as", e

		else:
			response = json.loads(result.read())
			result.close()
			return response['result'][0]['hostid']
	
	def all_hostid_get(self):
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "host.get",
					"params": {
						"output": ["hostid","status","host"]
					},
					"auth": self.user_login(),
					"id": 1
				})
		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)
		except Error as e:
			print "Error as", e

		else:
			response = json.loads(result.read())
			result.close()
			return response['result']

	def all_hostgroupid_get(self,hostid):
		data = json.dumps({
					"jsonrpc": "2.0",
					"method": "hostgroup.get",
					"params": {
						"output": "extend",
						"hostids": hostid
					},
					"auth": self.user_login(),
					"id": 1
				})

		request = urllib2.Request(self.__url, data)
		for key in self.__header:
			request.add_header(key, self.__header[key])
		try:
			result = urllib2.urlopen(request)
		except Error as e:
			print "Error as", e
		
		else:
			response = json.loads(result.read())
			result.close()
			return response['result'][0]['name']
			


if __name__ == "__main__":

	zabbix = zabbix_api('http://10.4.16.228/zabbix/api_jsonrpc.php',{"Content-Type":"application/json"},'Admin','123.com@LJL')
#	print zabbix.host_get('10.4.19.86')
#	print zabbix.template_get('Template OS Linux')			
#	print zabbix.hostgroup_get('Zabbix servers')
#	print zabbix.host_create('10.4.19.71','Zabbix servers','Template OS Linux,Templates Datanode port')
	print zabbix.all_hostid_get()