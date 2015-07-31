SALT_API = {"url": "https://10.4.19.71:8000",
            "user": "jianlong",
            "password": "123.com"
            }

ZABBIX_API = {"url": "http://10.4.16.228/zabbix/api_jsonrpc.php",
	      "header": {"Content-Type":"application/json"},
	      "user": "Admin",
	      "password": "123.com@LJL"
	     }


Cobbler_API = {"url": "",
            "user": "",
            "password": ""
            }

# salt result
RETURNS_MYSQL = {"host": "localhost",
               "port": 63306,
               "database": "salt",
               "user": "salt",
               "password": "salt"
                }

SERVICE = {"nginx": "nginx",
           "php": "php",
           "mysql": "mysql",
           "sysinit": "sysinit",
           "logstash": "logstash",
           "zabbix": "zabbix",
           "redis": "redis",
           "memcached": "memcached"
          }

OMS_MYSQL = {"host": "10.4.16.227",
               "port": 3306,
               "database": "oms",
               "user": "zabbix",
               "password": "zabbixadmin"
                }
