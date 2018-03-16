from math import exp
from scipy.optimize import minimize
import numpy as np
from command import *


#sqr = lambda p: p[0]**2 +p[1]**2
def sqr(p):
	return p[0]**2+p[1]**2+p[2]**2
def test():
	print(minimize(sqr, np.array([1]*4)))

N1=1 # change freq clost to targ_power
N2=2 # change freq close to max freq
A=800.
B=1.

#target_power = 290  #292-310,machine 1
target_power = 17
max_power = 310
maxfreq = 22 #2200000
minfreq = 12 #1200000

max_freq = []
min_freq = []
current_freq = []
current_util = []
core_num = 0
current_power = 0

def init():
	global core_num
	global maxfreq
	global minfreq
	global current_power
	global current_freq
	global current_util
	global max_freq
	global min_freq
	current_power = get_power()
	current_freq = np.array(get_freq_all()).flatten()/100000
	current_util = np.array(get_util_all()).flatten()
	core_num = len(current_freq)
	max_freq = [maxfreq]*core_num
	min_freq = [minfreq]*core_num
	print('current_power:%.2f,target:%.2f'%(current_power,target_power))
	print('freq:',current_freq)
	print('util:',current_util)

def fake_update():
	global core_num
	global maxfreq
	global minfreq
	global current_power
	global current_freq
	global current_util
	global max_freq
	global min_freq
	current_power = get_fake_power()
	current_util = get_fake_util()
	core_num = len(current_freq)
	max_freq = [maxfreq]*core_num
	min_freq = [minfreq]*core_num
	print('current_power:%.2f,target:%.2f'%(current_power,target_power))
	print('freq:',current_freq)
	print('util:',current_util)

def cal_d_power( d_freq,c):
	y=0
	for dx in d_freq:
		#y+=0.000017*dx
	    y+=dx/5.
	return y*c


def cal_target_power(target_power, current_power, i):
	return target_power+(current_power-target_power)*exp(-i/2.)# 0.95 -> 6 time


def cal_perform_loss( d_freq, c):
	core_num=len(d_freq)
	y=0
	for i in range(core_num):
		x=current_freq[i]+d_freq[i]*c
		if(x>max_freq[i]):
			x=max_freq[i]
		elif(x<min_freq[i]):
			x=min_freq[i]
		y+=(max_freq[i]-x)**2*current_util[i]
	return y


def fun(d_freq):
	global target_power
	global current_power
	y1=0
	for i in range(1,N1+1):
		y1+=(current_power+cal_d_power(d_freq,i)-cal_target_power(target_power,current_power,i))**2
	y2=0
	for i in range(1,N2+1):
		y2+=(cal_perform_loss(d_freq,i))
	print('A*y1:%.8f,B*y2:%.8f,%.8f'%(A*y1,B*y2,A*y1+B*y2),d_freq)
	return A*y1+B*y2

def get_fake_util():
	global maxfreq
	mid_util=[0.25, 0.5, 0.75, 1.0]
	core_num = len(current_freq)
	util = [0] * core_num
	for i in range(core_num):
		util[i] = mid_util[i] * maxfreq / current_freq[i]
		if (util[i] > 1):
			util[i] = 1.0
	return util

def get_fake_power():
	x=current_freq
	return sum(x) / 5.

def test_continues_freq():
	global core_num
	global current_freq
	global current_util
	global current_power
	print(core_num)
	current_freq=np.array([17,17,17,17])
	fake_update()
	for i in range (10):
		print('period  %d:'%(i))
		res = minimize(fun, np.array([-0] * core_num))
		d_freq=res['x']
		print(d_freq)
		current_freq = current_freq+d_freq
		fake_update()


def get_min_index(l):
	index=0
	for i in range(len(l)):
		if(l[i]<l[index]):
			index=i
	return index


def get_max_index(l):
	index=0
	for i in range(len(l)):
		if(l[i]>l[index]):
			index=i
	return index


def test_discret_freq():
	global core_num
	global current_freq
	global current_util
	global current_power
	print(core_num)
	current_freq=np.array([20,21,21,21])
	fake_update()
	for i in range (1):
		print('period  %d:'%(i))
		res = minimize(fun, np.array([-0] * core_num))
		d_freq=res['x']
		print(d_freq)
		temp_freq = current_freq+d_freq
		for i in range(core_num):
			current_freq[i]=round(temp_freq[i])
			if(current_freq[i]>max_freq[i]):
				current_freq[i]=max_freq[i]
			if(current_freq[i]<min_freq[i]):
				current_freq[i]=min_freq[i]
		left=sum(temp_freq)-sum(current_freq)
		diff=temp_freq-current_freq
		while(left>=1):
			index=get_max_index(diff)
			if(diff[index]<0):
				break
			if(current_freq[index]+1>max_freq[index]):
				diff[index]=-1
				continue
			current_freq[index]+=1
			diff[index]-=1
			left-=1
		while(left<=-1):
			index=get_min_index(diff)
			if(diff[index]>0):
				break
			if(current_freq[index]-1<min_freq[index]):
				diff[index]=1
				continue
			current_freq[index]-=1
			diff[index]+=1
			left+=1
		fake_update()

def adjust_freq():

	return

if __name__=="__main__":
	test_discret_freq()



