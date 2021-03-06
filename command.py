import urllib.request
import urllib.parse
import json
import re
import platform
import time
import getpass
import telnetlib
import socket
import numpy as np

from cpu_freq import available_freq

machines=["http://192.168.1.99:8081","http://192.168.1.74:8081"]
pdu="http://192.168.1.100/port_status.shtml"
pdu_domain='Admin'
pdu_uri='http://192.168.1.100'

core_num=20
current_sample_num=50
current_aquire_mode='telnet'#'web','telnet'
telnet_username='user'
telnet_passwd='user'

if(platform.platform()=='Windows-7-6.1.7601-SP1'):
	machines=["http://127.0.0.1:8081"]
	pdu="http://127.0.0.1/port_status.shtml"
	core_num=4
	current_sample_num = 5

def start_idle(machine):
	res=urllib.request.urlopen(machines[machine]+"/start_idle")
	data=res.read().decode('utf-8')
	return data

def start_idle_all():
	a=[]
	for m in range(len(machines)):
		x=start_idle(m)
		a.append(x)
	return a

def stop_idle(machine):
	res=urllib.request.urlopen(machines[machine]+"/stop_idle")
	data=res.read().decode('utf-8')
	return data

def stop_idle_all():
	a=[]
	for m in range(len(machines)):
		x=stop_idle(m)
		a.append(x)
	return a

def set_freq_core(machine, core, freq):
	res=urllib.request.urlopen(machines[machine]+"/set_freq?core=%d&freq=%d"%(core,freq))
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def set_freq_machine(machine,freq):
	res = urllib.request.urlopen(machines[machine] + "/set_freq_all?&freq=%d" % (freq))
	data = res.read().decode('utf-8')
	return json.loads(data)

def set_freq_list(freq):
	a=[]
	end=0
	core_list=get_corenum_all()
	for m in range(len(machines)):
		begin=end
		end=begin+core_list[m]
		data={'freq':list(freq[begin:end])}
		data=urllib.parse.urlencode(data)
		#res= urllib.request.urlopen(machines[m] + "/set_freq_list?freq=%s" % (urllib.parse.urlencode(json.dumps(list(freq[begin:end])))))
		res= urllib.request.urlopen(machines[m] + "/set_freq_list?"+data)
		# x=list(freq[begin:end])
		# print(type(x),x)
		# x=json.dumps(x)
		# print(type(x),x)
		# x=urllib.parse.urlencode(x)
		# print(type(x),x)
		# res=urllib.request.urlopen(machines[m] + "/set_freq_list?freq="+urllib.parse.urlencode(json.dumps(list(freq[begin:end]))))
		data = res.read().decode('utf-8')
		a.append(data)
	return json.loads(data)

def set_freq_all(freq):
	res =[]
	for m in range(len(machines)):
		res.append(set_freq_machine(m,freq))
	return res

def get_freq_core(machine,core):
	res=urllib.request.urlopen(machines[machine]+"/get_freq?core=%d"%(core))
	data=res.read().decode('utf-8')
	return json.loads(data)


def get_freq_machine(machine,type=''):
	res=urllib.request.urlopen(machines[machine]+"/get_"+type+"freq_all")
	data=res.read().decode('utf-8')
	return json.loads(data)

def get_freq_all(type=''):
	a=[]
	for m in range(len(machines)):
		a.append(get_freq_machine(m,type))
	return a

def get_freq_average():
	a=[]
	for m in range(len(machines)):
		b=get_freq_machine(m)
		avg=sum(b)/len(b)
		a.append(avg)
	return a

def get_corenum_machine(machine):
	res=urllib.request.urlopen(machines[machine]+"/get_corenum")
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def get_corenum_all():
	a=[]
	for m in range(len(machines)):
		a.append(get_corenum_machine(m))
	return a


def get_util_machine(machine):
	res=urllib.request.urlopen(machines[machine]+"/get_util")
	data=res.read().decode('utf-8')
	data=json.loads(data)
	return data

def get_util_all():
	a=[]
	for m in range(len(machines)):
		a.append(get_util_machine(m))
	return a

def get_current():
	if(current_aquire_mode=='telnet'):
		return get_current_telnet()
	else:
		return get_current_web()

def get_power():
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		x = np.array(get_freq_all()).flatten()
		return sum(x)/500000.
	addr = ('192.168.1.101', 5025)  # PA310
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(addr)  # connect
	s.send(b':NUMERIC:VALUE? 3\n')  # command
	r = s.recv(100)  # response
	r = float(r)
	s.close()  # disconnect
	return r

def telnet_init(tn):
	HOST = "192.168.1.100"
	user = 'user'
	password = 'user'

	tn = telnetlib.Telnet(HOST)

	# tn.read_until(b"login: ")
	# tn.write(user.encode('ascii') + b"\n")
	# if password:
	# 	tn.read_until(b"Password: ")
	# 	tn.write(password.encode('ascii') + b"\n")
	x=tn.read_until(b"> ")
	print(x.decode())


def get_current_telnet():
	HOST = "192.168.1.100"
	tn = telnetlib.Telnet(HOST)
	x=tn.read_until(b"> ")

	sum=0.0
	for i in range(current_sample_num):
		tn.write(b"crt\n")
		x = tn.read_until(b'> ')
		data=x.decode('ascii')
		m = re.search('Input Current A:\s+(\d+.\d*)\s+A', data)
		x=float(m.group(1))
		sum+=x
	return sum/current_sample_num

def get_current_web():
	auth_handler = urllib.request.HTTPBasicAuthHandler()
	auth_handler.add_password(realm="Admin", uri='http://192.168.1.100', user='user', passwd='user')
	opener = urllib.request.build_opener(auth_handler)
	# ...and install it globally so it can be used with urlopen.
	urllib.request.install_opener(opener)
	sum=0.0
	n=current_sample_num
	for i in range(n):
		res=urllib.request.urlopen(pdu)
		data=res.read().decode('utf-8')
		m=re.search('CA:\s+(\d+.\d*)A',data)
		#print(m.groups())
		#print(m.group())
		sum+=float(m.group(1))
	return sum/n



def get_power_freq_data(ordered=False):
	a={}
	l=available_freq
	if(ordered):
		l.sort()
	for freq in l:
		set_freq_all(freq)
		print("freq%d:"%(freq))
		time.sleep(5)
		p=get_power()
		a[freq]=p
		print("%f\n"%(p))
	file = open("power_freq.data",'w')
	for freq in available_freq:
		file.write(str(freq)+","+str(a[freq])+'\n')
	file.close()
	return a

def test_basic():
	print('core_num',get_corenum_all())
	print('freq:',str(get_freq_all()))
	print('freq_average:',get_freq_average())
	print('power:',get_power())
	print('set_freq:',set_freq_machine(0,1300000))
	print('util:',get_util_all())
	print(get_power_freq_data(True))

def test_model():
	for i in range(1200000,2300000,100000):
		print('core_num',get_corenum_all())
		print("freq:",set_freq_all(i))
		print("util:",get_util_all())
		print("power:",get_power())
		time.sleep(5)

if __name__=="__main__":
	test_model()