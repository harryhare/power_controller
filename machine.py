import socketserver
import http.server
import urllib.parse
import json
from cpu_freq import *

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
			core=-1
			freq=1200000
			if 'core' in params.keys():
				core= int(params['core'][0])
			if 'freq' in params.keys():
				f=int(params['freq'][0])
				for t in available_freq:
					if t<=f:
						freq=t
						break
			if(core!=-1):
				set_freq(core,freq)
			else:
				for i in range(cpu_num):
					set_freq(i,freq)
			cur_freq = get_cur_freq()
			res = json.dumps(cur_freq)
			self.send_response(200)
		else:
			self.send_response(500)
			res="bad gateway"
		self.end_headers()
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
