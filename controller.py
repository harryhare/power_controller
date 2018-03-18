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
N2=1 # change freq close to max freq
A=100.
B=1.
#D=(274.79E+00-266.34E+00)/200
freq_factor=(292.1E+00-275.05E+00)/200
sigma=4. # large sigma -> target power change slow

#target_power = 290  #292-310,machine 1
target_power = 15
max_power = 310
maxfreq = 22 #2200000
minfreq = 12 #1200000

max_freq = []
min_freq = []
current_freq = []
current_util = []
core_num = 0
core_list = []
current_power = 0

def update():
	global core_num
	global maxfreq
	global minfreq
	global current_power
	global current_freq
	global current_util
	global max_freq
	global min_freq
	global core_list
	global period
	period += 1
	current_power = get_power()
	current_freq = np.array(get_freq_all()).flatten()/100000
	current_util = np.array(get_util_all()).flatten()
	core_num = len(current_freq)
	core_list = get_corenum_all()
	max_freq = np.array(get_freq_all('max')).flatten()/100000
	min_freq = np.array(get_freq_all('min')).flatten()/100000
	print('peroid:%d'%(period))
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
	    y+=dx*freq_factor
	return y*c


def cal_target_power(target_power, current_power, i):
	return target_power+(current_power-target_power)*exp(-i/sigma)# 0.95 -> 6 time


def cal_perform_loss( d_freq, c):
	core_num=len(d_freq)
	y=0
	for i in range(core_num):
		x=current_freq[i]+d_freq[i]*c
		# if(x>max_freq[i]):
		# 	x=max_freq[i]
		# elif(x<min_freq[i]):
		# 	x=min_freq[i]
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
	#print('A*y1:%.8f,B*y2:%.8f,%.8f'%(A*y1,B*y2,A*y1+B*y2),d_freq)
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
	return sum(x) /5.

def test_continues_freq():
	global core_num
	global current_freq
	global current_util
	global current_power
	print(core_num)
	current_freq=np.array([22,22,22,22])
	fake_update()
	for i in range (20):
		print('period  %d:'%(i))
		res = minimize(fun, np.array([-0] * core_num))
		d_freq=res['x']
		print(d_freq)
		current_freq = current_freq+d_freq
		for i in range(core_num):
			if(current_freq[i]>max_freq[i]):
				current_freq[i]=max_freq[i]
			if(current_freq[i]<min_freq[i]):
				current_freq[i]=min_freq[i]
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

def adjust_freq_to_int(current_freq, d_freq):
	target_freq = current_freq + d_freq
	core_num=len(current_freq)
	for i in range(core_num):
		current_freq[i] = round(target_freq[i])
		if (current_freq[i] > max_freq[i]):
			current_freq[i] = max_freq[i]
		if (current_freq[i] < min_freq[i]):
			current_freq[i] = min_freq[i]
	left =  sum(target_freq) - sum(current_freq)
	diff = target_freq - current_freq
	while (left >= 1):
		index = get_max_index(diff)
		if (diff[index] < 0):
			break
		if (current_freq[index] + 1 > max_freq[index]):
			diff[index] = -1
			continue
		current_freq[index] += 1
		diff[index] -= 1
		left -= 1
	while (left <= -1):
		index = get_min_index(diff)
		if (diff[index] > 0):
			break
		if (current_freq[index] - 1 < min_freq[index]):
			diff[index] = 1
			continue
		current_freq[index] -= 1
		diff[index] += 1
		left += 1
	return current_freq

def test_discret_freq():
	global core_num
	global current_freq
	global current_util
	global current_power
	print(core_num)
	current_freq=np.array([22,22,22,22])
	fake_update()
	for i in range (10):
		print('period  %d:'%(i))
		res = minimize(fun, np.array([-0] * core_num))
		d_freq=res['x']
		print(d_freq)
		current_freq=adjust_freq_to_int(current_freq,d_freq)
		fake_update()

period = 0
def adjust_freq():
	global current_freq
	update()
	res = minimize(fun, np.array([-0] * core_num))
	d_freq = res['x']
	print('d_freq',d_freq)
	current_freq=adjust_freq_to_int(current_freq,d_freq)
	set_freq_list(current_freq*100000)
	return

def adjust_freq_test():
	global max_freq
	global min_freq
	max_freq=[22]*20
	min_freq=[12]*20
	adjust_freq_to_int(np.array([22, 22, 22, 22, 22,
	                    22, 22, 22., 22, 22.,
	                    22., 22., 22., 22. ,22.,
	                    22., 22. ,22.,22. ,22.]),
	                   np.array([-0.3367607 , -0.3367607 , -0.33676064,-0.33676064, -0.33676064, -0.3367607,
						 -0.33676065, -0.33676064, -0.33676064, -0.33676064 ,-0.33676064,-0.33676064,
						 -0.33676064 ,-0.33676064, -0.33676064,-0.33676064, -0.33676064,-0.33676064,
						 -0.33676064, -0.33676064]))


if __name__=="__main__":
	#test_continues_freq()
	test_discret_freq()
	#adjust_freq_test()
	# while(True):
	# 	adjust_freq()
	# 	time.sleep(1)




