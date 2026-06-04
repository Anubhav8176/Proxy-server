import argparse
from proxy import start_server, cache


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--port", type=int, default=3000)
	parser.add_argument("--origin", type = str)
	parser.add_argument("--clear-cache", action='store_true')
	args = parser.parse_args()
	if args.clear_cache:
		cache.clear()
		return
	
	if not args.origin:
		parser.error('--origin is required when starting the server')
	port = int(args.port)
	origin = args.origin
	
	print(origin)
	
	start_server(port, origin)

if __name__ == "__main__":
	main()