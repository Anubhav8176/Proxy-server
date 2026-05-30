import argparse
from proxy import start_server


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--port")
	parser.add_argument("--origin")
	args = parser.parse_args()

	port = int(args.port)
	origin = args.origin
	
	print(origin)
	
	start_server(port, origin)