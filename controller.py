import urllib.request
import json
import re
import platform

machines=["http://192.168.1.99:8081","http://192.168.1.98:8081","http://192.168.1.74:8081"]
pdu="http://user:user@192.168.1.100/port_status.shtml"

if(platform.platform()=='Windows-7-6.1.7601-SP1'):
	machines=["http://127.0.0.1:8081"]
	pdu="http://127.0.0.1/port_status.shtml"

def get_freq(machine):
	res=urllib.request.urlopen(machine+"/get")
	#print(res.read().decode('utf-8'))
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def get_all_freq():
	a=[]
	for m in machines:
		a.append(get_freq(m))
	return a

def get_total_power():
	res=urllib.request.urlopen(pdu)
	data=res.read().decode('utf-8')
	m=re.search('CA:\s+(\d+.\d*)A',data)
	#print(m.groups())
	#print(m.group())
	return float(m.group(1))*220

if __name__=="__main__":
	print(get_all_freq())
	print(get_total_power())