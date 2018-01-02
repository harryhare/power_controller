import urllib.request
import json
import re
import platform

machines=["http://192.168.1.99:8081","http://192.168.1.98:8081","http://192.168.1.74:8081"]
pdu="http://user:user@192.168.1.100/port_status.shtml"
core_num=6
if(platform.platform()=='Windows-7-6.1.7601-SP1'):
	machines=["http://127.0.0.1:8081"]
	pdu="http://127.0.0.1/port_status.shtml"
	core_num=4

def get_freq(machine):
	res=urllib.request.urlopen(machine+"/get_freq")
	#print(res.read().decode('utf-8'))
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def set_freq_core(machine,core, freq):
	res=urllib.request.urlopen(machine+"/set_freq?core=%d&freq=%d"%(core,freq))
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def set_freq(machine,freq):
	a=[]
	for i in range(core_num):
		a=(set_freq_core(machines[machine],i,freq))
	return a


def get_freq_all():
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

def get_util(machine):
	res=urllib.request.urlopen(machine+"/get_util")
	data=res.read().decode('utf-8')
	return float(data)

def get_util_all():
	a=[]
	for m in machines:
		a.append(get_util(m))
	return a

if __name__=="__main__":
	print(get_freq_all())
	print(get_total_power())
	print(set_freq(0,1300000))
	print(get_util_all())