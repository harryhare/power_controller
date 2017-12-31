import socketserver
import http.server
import urllib.parse
import json

from multiprocessing import cpu_count


def get_cur_freq():
	cpu_num=cpu_count()
	cur_freq_file = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq"
	cur_freq=[0]*cpu_num
	for i in range(cpu_num):
		file = open(cur_freq_file%(i),"r")
		cur=file.read()[:-1]
		cur_freq[i] = int(cur)
		file.close()
	return cur_freq

def set_cur_freq(core, freq):
	set_freq_file = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_setspeed"
	file=open(set_freq_file%(core),"w")
	file.write(str(freq))
	file.close()
	return

class SETHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		print("GET")
		cur_freq=get_cur_freq()
		res=json.dumps(cur_freq)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(bytes(res, 'UTF-8'))

	def do_POST(self):
		print( "POST")
		self.send_response(200)
		self.end_headers()

if  __name__ == '__main__':
	Handler = SETHandler
	PORT = 8080
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("serving at port", PORT)
	httpd.serve_forever()
