import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()


def start_server(port, origin):

	#Server address and port
	server_address = ('', port)

	#Create instance of Http server
	http_server = HTTPServer(server_address, MyRequestHandler)
	
	print("Server starting....")
	http_server.serve_forever()	
	
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--port")
	parser.add_argument("--origin")
	args = parser.parse_args()

	port = int(args.port)
	origin = args.origin
	
	print(origin)
		
	start_server(port, origin)