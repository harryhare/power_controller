import socketserver
import http.server
import urllib.parse
import json
import os
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
		if(path=='/get_freq_all'):
			cur_freq=get_freq_all()
			res=json.dumps(cur_freq)
			self.send_response(200)
		elif(path=='/get_freq'):
			core =-1
			if 'core' in params.keys():
				core= int(params['core'][0])
			if(core!=-1):
				freq=get_freq(core)
				res=json.dumps(freq)
				self.send_response(200)
			else:
				res="wrong argument"
				self.send_response(400)
		elif(path=='/set_freq_all'):
			freq=-1
			if 'freq' in params.keys():
				f=int(params['freq'][0])
				freq=get_avail_freq(f)
			if(freq!=-1):
				set_freq_all(freq)
				cur_freq = get_freq_all()
				res = json.dumps(cur_freq)
				self.send_response(200)
			else:
				res="wrong argument"
				self.send_response(400)
		elif(path=='/set_freq'):
			core=-1
			freq=-1
			if 'core' in params.keys():
				core= int(params['core'][0])
			if 'freq' in params.keys():
				f=int(params['freq'][0])
				freq=get_avail_freq(f)
			if(core!=-1 and freq !=-1):
				set_freq(core,freq)
				cur_freq = get_freq_all()
				res = json.dumps(cur_freq)
				self.send_response(200)
			else:
				res="wrong argument"
				self.send_response(400)
		elif(path=='/get_util'):
			util=get_util()
			res=json.dumps(util)
			self.send_response(200)
		elif(path=='/start_idle'):
			res=str(os.system("./start_idle"))
			self.send_response(200)
		elif(path=='/stop_idle'):
			res=str(os.system("./stop_idle"))
			self.send_response(200)
		else:
			res="bad gateway"
			self.send_response(500)
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
