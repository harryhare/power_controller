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
	return cur_freq

class SETHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		print("GET")
		cur_freq=get_cur_freq()
		res=json.dumps(cur_freq)
		self.wfile.write(res)
		self.send_response(200)
		self.end_headers()

	def do_POST(self):
		print( "POST")
		self.send_response(200)
		self.end_headers()


Handler = SETHandler
PORT = 80
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
