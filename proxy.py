from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from socketserver import ThreadingMixIn, TCPServer

from CacheStore import CacheStore

cache = CacheStore()

SKIP_HEADERS = {'transfer-encoding', 'connection', 'content-encoding', 'keep-alive'}


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass


class MyRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		origin = self.server.origin

		# Need to intercept the request here
		key = self.path
		entry = cache.get(key=key)

		if entry:
			self._send(status=entry.status, headers=entry.headers, body=entry.body, cache_status="HIT")
			return

		url = origin.rstrip('/') + self.path
		try:
			response = requests.get(url)
			headers = response.headers
			body = response.content
			status = response.status_code
		except requests.RequestException as e:
			headers = e.response.headers
			body = e.response.content
			status = e.response.status_code

		cache.set(key=key, status=status, body=body, headers=headers)
		self._send(status=status, headers=headers, body=body, cache_status="MISS")

	def _send(self, status, headers, body, cache_status):
		self.send_response(code=status)
		for k, v in headers.items():
			if k.lower() not in SKIP_HEADERS:
				self.send_header(k, v)
		self.send_header('X-Cache', cache_status)
		self.send_header('Content-Length', str(len(body)))
		self.end_headers()
		self.wfile.write(body)
		
		

# The function starts the server and handles all the configuration for the server.
def start_server(port, origin):

	#Server address and port
	server_address = ('', port)

	#Create instance of Threaded Http server
	http_server = ThreadedHTTPServer(server_address, MyRequestHandler)
	http_server.origin = origin
	
	print("Server starting....")
	http_server.serve_forever()