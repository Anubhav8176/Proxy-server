from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

class MyRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		origin = self.server.origin
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

		print(f"Unwanted Headers: t-e: {header.get('transfer-encoding')}, connection: {header.get('connection')} and c-e: {header.get('content-encoding')}")

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