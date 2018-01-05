import urllib.request
import json
import re
import platform
import time
from cpu_freq import available_freq

machines=["http://192.168.1.99:8081","http://192.168.1.98:8081","http://192.168.1.74:8081"]
pdu="http://192.168.1.100/port_status.shtml"
pdu_domain='Admin'
pdu_uri='http://192.168.1.100'

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

def set_freq_core(machine, core, freq):
	res=urllib.request.urlopen(machine+"/set_freq?core=%d&freq=%d"%(core,freq))
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def set_freq(machine,freq):
	a=[]
	for i in range(core_num):
		a=(set_freq_core(machines[machine],i,freq))
	return a

def set_freq_all(freq):
	for m in range(len(machines)):
		set_freq(m,freq)

def get_freq_all():
	a=[]
	for m in machines:
		a.append(get_freq(m))
	return a
def get_freq_average():
	a=[]
	for m in machines:
		b=get_freq(m)
		avg=sum(b)/len(b)
		a.append(avg)
	return a

def get_total_power():
	auth_handler = urllib.request.HTTPBasicAuthHandler()
	auth_handler.add_password(realm="Admin", uri='http://192.168.1.100', user='user', passwd='user')
	opener = urllib.request.build_opener(auth_handler)
	# ...and install it globally so it can be used with urlopen.
	urllib.request.install_opener(opener)
	res=urllib.request.urlopen(pdu)
	data=res.read().decode('utf-8')
	m=re.search('CA:\s+(\d+.\d*)A',data)
	#print(m.groups())
	#print(m.group())
	return float(m.group(1))*220

def get_util(machine):
	res=urllib.request.urlopen(machine+"/get_util")
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def get_util_all():
	a=[]
	for m in machines:
		a.append(get_util(m))
	return a


def get_power_freq_data():
	a={}
	for freq in available_freq:
		set_freq_all(freq)
		print("freq%d:"%(freq))
		time.sleep(60)
		p=get_total_power()
		p=p/(len(machines)*core_num)
		a[freq]=p
		print("%f\n"%(p))
	file = open("power_freq.data",'w')
	for freq in available_freq:
		file.write(str(freq)+","+str(a[freq])+'\n')
	file.close()
	return a

if __name__=="__main__":
	print('freq:',str(get_freq_all()))
	print('freq_average:',get_freq_average())
	print('power:',get_total_power())
	print('set_freq:',set_freq(0,1300000))
	print('util:',get_util_all())
	#print(get_power_freq_data())