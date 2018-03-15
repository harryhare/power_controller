from multiprocessing import cpu_count
import psutil
import platform

available_freq=[2200000,2100000,2000000,1900000,1800000,1700000,1600000,1500000,1400000,1300000,1200000]
cpu_num = cpu_count()

cpu_freq=[1600000,1500000,1400000,1300000]

pre_filename="/sys/devices/system/cpu/cpu%d/cpufreq/"
pre_filename="/sys/devices/system/cpu/cpufreq/policy%d/"

def change_governor():
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		return
	filename=pre_filename+"scaling_governor"
	for core in range(cpu_num):
		file = open(filename%(core),"r")
		file.write("userspace")
		file.close()

def get_avail_freq(f):
	freq=min(available_freq)
	for t in available_freq:
		if t <= f:
			freq = t
			break
	return freq

def get_freq_all():
	cur_freq=[0]*cpu_num
	for core in range(cpu_num):
		cur_freq[core] = get_freq(core)
	return cur_freq

def get_freq(core):
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		return cpu_freq[core]
	cur_freq_file = pre_filename+"scaling_cur_freq"
	file = open(cur_freq_file%(core),"r")
	cur=file.read()[:-1]
	cur_freq = int(cur)
	file.close()
	return cur_freq

def set_freq(core, freq):
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		cpu_freq[core]=freq
		return
	set_freq_file = pre_filename+"scaling_setspeed"
	file=open(set_freq_file%(core),"w")
	file.write(str(freq))
	file.close()
	return

def set_freq_all(freq):
	for core in range(cpu_num):
		set_freq(core,freq)

def get_util_total():
	return psutil.cpu_percent(0)

def get_util():
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
	print(psutil.cpu_stats())
	print(psutil.cpu_percent(None))
	print(psutil.cpu_percent(None,True))
	print(psutil.cpu_percent(1,True))
	print(psutil.cpu_percent(0))
	print(psutil.cpu_percent(1))
	print(psutil.cpu_percent(2))
	print(psutil.cpu_percent(3))