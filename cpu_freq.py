from multiprocessing import cpu_count

available_freq=[1600000,1500000,1400000,1300000,1200000]
cpu_num = cpu_count()

cpu_freq=[1600000,1500000,1400000,1300000]

def get_cur_freq():
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
	cpu_freq[core]=freq
	return
	set_freq_file = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_setspeed"
	file=open(set_freq_file%(core),"w")
	file.write(str(freq))
	file.close()
	return