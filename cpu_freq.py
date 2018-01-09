from multiprocessing import cpu_count
import psutil
import platform

available_freq=[2200000,2100000,2000000,1900000,1800000,1700000,1600000,1500000,1400000,1300000,1200000]
cpu_num = cpu_count()

cpu_freq=[1600000,1500000,1400000,1300000]

def get_cur_freq():
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		return cpu_freq
	cur_freq_file = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq"
	cur_freq=[0]*cpu_num
	for i in range(cpu_num):
		file = open(cur_freq_file%(i),"r")
		cur=file.read()[:-1]
		cur_freq[i] = int(cur)
		file.close()
	return cur_freq

def set_freq(core, freq):
	if (platform.platform() == 'Windows-7-6.1.7601-SP1'):
		cpu_freq[core]=freq
		return
	set_freq_file = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_setspeed"
	file=open(set_freq_file%(core),"w")
	file.write(str(freq))
	file.close()
	return


def get_util_total():
	return psutil.cpu_percent(0)

def get_util():
	return psutil.cpu_percent(0,True)

def get_util_top():
	return psutil.cpu_percent(0)

if __name__=='__main__':
	print(psutil.cpu_stats())
	print(psutil.cpu_percent(None))
	print(psutil.cpu_percent(None,True))
	print(psutil.cpu_percent(1,True))
	print(psutil.cpu_percent(0))
	print(psutil.cpu_percent(1))
	print(psutil.cpu_percent(2))
	print(psutil.cpu_percent(3))