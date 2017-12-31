import socketserver
import http.server
import urllib.parse
import json

from multiprocessing import cpu_count

available_freq=[1600000,1500000,1400000,1300000,1200000]
cpu_num = cpu_count()


def get_cur_freq():
	cur_freq_file = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq"
	cur_freq=[0]*cpu_num
	for i in range(cpu_num):
		file = open(cur_freq_file%(i),"r")
		cur=file.read()[:-1]
		cur_freq[i] = int(cur)
		file.close()
	return cur_freq

def set_freq(core, freq):
	set_freq_file = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_setspeed"
	file=open(set_freq_file%(core),"w")
	file.write(str(freq))
	file.close()
	return

class SETHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		print("GET")
		print(self.address_string())
		print(self.headers)
		print(self.path)
		print(self.request)
		path=self.path
		params={}
		if '?' in self.path:
			[path,queryString]=self.path.split('?', 1)
			queryString = urllib.parse.unquote(queryString)
			params = urllib.parse.parse_qs(queryString)
		if(path=='/get'):
			cur_freq=get_cur_freq()
			res=json.dumps(cur_freq)
			self.send_response(200)
		elif(path=='/set'):
			self.send_response(200)
			core=-1
			freq=1200000
			if 'core' in params.keys():
				core= params['core']
			if 'freq' in params.keys():
				f=params['freq']
				for t in available_freq:
					if t<=f:
						t=f
						break;
			if(core!=-1):
				set_freq(core,freq)
			else:
				for i in range(cpu_num):
					set_freq(i,freq)
			cur_freq = get_cur_freq()
			res = json.dumps(cur_freq)
		else:
			self.send_response(500)
			res="bad gateway"
		self.end_headers()
		res+='\n'
		self.wfile.write(bytes(res, 'UTF-8'))

	def do_POST(self):
		print( "POST")
		self.send_response(200)
		self.end_headers()

if  __name__ == '__main__':
	Handler = SETHandler
	PORT = 8081
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("serving at port", PORT)
	httpd.serve_forever()
