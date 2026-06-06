import threading
import requests

def make_request():
    response = requests.get("http://localhost:3000/posts")
    print(response.headers.get("X-Cache"))

threads = [threading.Thread(target=make_request) for _ in range(100)]
for t in threads: t.start()
for t in threads: t.join()