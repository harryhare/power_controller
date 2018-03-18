from multiprocessing import cpu_count
import psutil
import platform

available_freq=[2200000,2100000,2000000,1900000,1800000,1700000,1600000,1500000,1400000,1300000,1200000]
cpu_num = cpu_count()

if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
	cpu_num=4
fake_freq=[1200000]*4
fake_util=[0.25, 0.50, 0.75, 1.00]
fake_max_freq=max(available_freq)
fake_min_freq=min(available_freq)

#pre_filename="/sys/devices/system/cpu/cpu%d/cpufreq/"
pre_filename="/sys/devices/system/cpu/cpufreq/policy%d/"

def set_governor():
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		return
	filename=pre_filename+"scaling_governor"
	for core in range(cpu_num):
		file = open(filename%(core),"w")
		file.write("userspace")
		file.close()

def get_corenum():
	return psutil.cpu_count()

def get_avail_freq(f):
	freq=min(available_freq)
	for t in available_freq:
		if t <= f:
			freq = t
			break
	return freq

def get_freq_all(type='cur'):
	cur_freq=[0]*cpu_num
	for core in range(cpu_num):
		cur_freq[core] = get_freq(core,type)
	return cur_freq

def get_freq(core, type='cur'):
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		if (type=='cur'):
			return fake_freq[core]
		elif(type=='min'):
			return 1200000
		elif(type=='max'):
			return 2200000
		else:
			return -1
	cur_freq_file = pre_filename+"scaling_"+type+"_freq"
	file = open(cur_freq_file%(core),"r")
	cur=file.read()[:-1]
	cur_freq = int(cur)
	file.close()
	return cur_freq

def set_freq(core, freq):
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		fake_freq[core]=freq
		return
	set_freq_file = pre_filename+"scaling_setspeed"
	file=open(set_freq_file%(core),"w")
	file.write(str(freq))
	file.close()
	return

def set_freq_all(freq):
	for core in range(cpu_num):
		set_freq(core,freq)

def set_freq_list(freq):
	for core in range(cpu_num):
		set_freq(core,freq[core])

def get_util_total():
	return psutil.cpu_percent(0)

def get_util():
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		#util model
		util=[0]*cpu_num
		for i in range(cpu_num):
			util[i]=fake_util[i]*fake_max_freq/fake_freq[i]
			if(util[i]>1):
				util[i]=1.0
		return util
	return psutil.cpu_percent(0,True)

def get_util_top():
	return psutil.cpu_percent(0)

if __name__=='__main__':
	print(get_util())
	print(get_util_total())
	print(get_util_top())
	print(set_freq(1,1200000))
	print(get_freq(1))
	print(set_freq_all(1200000))
	print(get_freq_all())
	print(psutil.cpu_count())#logic
	print(psutil.cpu_count(False))#real
	print(psutil.cpu_stats())
	print(psutil.cpu_freq())#averge
	print(psutil.cpu_freq(True))#each
	print(psutil.cpu_percent(None))
	print(psutil.cpu_percent(None,True))
	print(psutil.cpu_percent(1,True))
	print(psutil.cpu_percent(0))
	print(psutil.cpu_percent(1))
	print(psutil.cpu_percent(2))
	print(psutil.cpu_percent(3))
