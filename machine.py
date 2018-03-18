import socketserver
import http.server
import urllib.parse
import json
import os
from cpu_freq import *


class SETHandler(http.server.BaseHTTPRequestHandler):
	params={}
	res=''
	def get_corenum(self):
		num = get_corenum()
		self.res = json.dumps(num)
		self.send_response(200)
	def get_minfreq_all(self):
		freq= get_freq_all('min')
		self.res = json.dumps(freq)
		self.send_response(200)
	def get_maxfreq_all(self):
		freq= get_freq_all('max')
		self.res = json.dumps(freq)
		self.send_response(200)
	def get_minfreq(self):
		core = -1
		if 'core' in self.params.keys():
			core = int(self.params['core'][0])
		if (core != -1):
			freq = get_freq(core,'min')
			self.res = json.dumps(freq)
			self.send_response(200)
		else:
			self.res = "wrong argument"
			self.send_response(400)
	def get_maxfreq(self):
		core = -1
		if 'core' in self.params.keys():
			core = int(self.params['core'][0])
		if (core != -1):
			freq = get_freq(core, 'max')
			self.res = json.dumps(freq)
			self.send_response(200)
		else:
			self.res = "wrong argument"
			self.send_response(400)
	def get_freq_all(self):
		cur_freq = get_freq_all()
		self.res = json.dumps(cur_freq)
		self.send_response(200)
	def get_freq(self):
		core = -1
		if 'core' in self.params.keys():
			core = int(self.params['core'][0])
		if (core != -1):
			freq = get_freq(core)
			self.res = json.dumps(freq)
			self.send_response(200)
		else:
			self.res = "wrong argument"
			self.send_response(400)
	def set_freq_list(self):
		freq = []
		if 'freq' in self.params.keys():
			freq = json.loads(self.params['freq'][0])
			set_freq_list(freq)
			cur_freq = get_freq_all()
			self.res = json.dumps(cur_freq)
			self.send_response(200)
		else:
			self.res = "wrong argument"
			self.send_response(400)
	def set_freq_all(self):
		freq = -1
		if 'freq' in self.params.keys():
			f = int(self.params['freq'][0])
			freq = get_avail_freq(f)
		if (freq != -1):
			set_freq_all(freq)
			cur_freq = get_freq_all()
			self.res = json.dumps(cur_freq)
			self.send_response(200)
		else:
			self.res = "wrong argument"
			self.send_response(400)
	def set_freq(self):
		core = -1
		freq = -1
		if 'core' in self.params.keys():
			core = int(self.params['core'][0])
		if 'freq' in self.params.keys():
			f = int(self.params['freq'][0])
			freq = get_avail_freq(f)
		if (core != -1 and freq != -1):
			set_freq(core, freq)
			cur_freq = get_freq_all()
			self.res = json.dumps(cur_freq)
			self.send_response(200)
		else:
			self.res = "wrong argument"
			self.send_response(400)
	def get_util(self):
		util = get_util()
		self.res = json.dumps(util)
		self.send_response(200)

	def start_idle(self):
		self.res = str(os.system("./start_idle"))
		self.send_response(200)

	def stop_idle(self):
		self.res = str(os.system("./stop_idle"))
		self.send_response(200)

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
			self.params = urllib.parse.parse_qs(queryString)

		try:
			getattr(self, path[1:])()
		except Exception:
			self.res="bad gateway"
			self.send_response(500)

		self.end_headers()
		self.wfile.write(bytes(self.res, 'UTF-8'))

	def do_POST(self):
		print( "POST")
		self.send_response(200)
		self.end_headers()


def init():
	set_governor()


if __name__ == '__main__':
	init()
	Handler = SETHandler
	PORT = 8081
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("serving at port", PORT)
	httpd.serve_forever()
