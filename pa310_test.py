from socket import *
from select import *
import time
addr = ('192.168.1.101',5025) # PA310
s = socket(AF_INET, SOCK_STREAM)
s.connect(addr) # connect
s.send(b':NUMERIC:HOLD ON\n')
s.send(b':NUMERIC:ITEM1 U,1;ITEM2 I,1;ITEM3 P,1\n')
s.send(b':NUMERIC:VALUE?\n') # command
s.send(b':NUMERIC:HOLD OFF\n')
r = s.recv(30) # response
#s.send(b':NUMERIC:HOLD OFF\n')
#print(r)
s.close() # disconnect
b=r.decode('utf-8')
i=b.find(',')
j=b.rfind(',')
#print(float(b[0:i]))
#print(float(b[i+1:j]))
#print(float(b[j+1:]))
print(r)
print(float(b[j+1:]))

