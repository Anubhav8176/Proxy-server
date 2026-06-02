from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

class MyRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		origin = self.server.origin

		# Need to intercept the request here
		key = self.path

		url = origin.rstrip('/') + self.path
		try:
			response = requests.get(url)
			header = response.headers
			body = response.content
			status = response.status_code
		except requests.RequestException as e:
			header = e.response.headers
			body = e.response.content
			status = e.response.status_code

		self.send_response(code=status)
		for k, v in header.items():
			if k.lower() not in ('transfer-encoding', 'connection', 'content-encoding'):
				self.send_header(k, v)
		self.end_headers()
		self.wfile.write(body)
		
		

# The function starts the server and handles all the configuration for the server.
def start_server(port, origin):

	#Server address and port
	server_address = ('', port)

	#Create instance of Http server
	http_server = HTTPServer(server_address, MyRequestHandler)
	http_server.origin = origin
	
	print("Server starting....")
	http_server.serve_forever()