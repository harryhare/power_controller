from socket import *
from select import *
import time
addr = ('192.168.1.101',5025) # PA310
s = socket(AF_INET, SOCK_STREAM)
s.connect(addr) # connect
powers=[]
for i in range(50):
	s.send(b':NUMERIC:VALUE? 3\n') # command
	r = s.recv(100) # response
	r=float(r)
	powers.append(r)
	print(r)
	time.sleep(0.250)
s.close() # disconnect
print("average:%f"%(sum(powers)/len(powers)))
