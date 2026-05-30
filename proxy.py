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

		print(f"The response is: \n header:{header},\n status: {status}\n and body:{body}")
		
		

# The function starts the server and handles all the configuration for the server.
def start_server(port, origin):

	#Server address and port
	server_address = ('', port)

	#Create instance of Http server
	http_server = HTTPServer(server_address, MyRequestHandler)
	http_server.origin = origin
	
	print("Server starting....")
	http_server.serve_forever()