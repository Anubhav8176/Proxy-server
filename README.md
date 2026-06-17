# 🚀 Caching Proxy Server

A lightweight **HTTP caching proxy server** built in pure Python — no frameworks, no magic. It sits between your HTTP client and any origin server, forwarding requests and caching responses in memory so repeated calls never hit the origin twice.

```
Client  ──→  Proxy :PORT  ──→  Origin Server
                 ↑
         Cache (in-memory)
         returns on HIT,
         skips origin entirely
```

> 🗺️ **This project is part of the [roadmap.sh](https://roadmap.sh/projects/caching-server) Backend Developer series.**
> A huge shoutout to roadmap.sh for providing structured, real-world project ideas that bridge the gap between learning and building. If you're on a backend journey, their roadmaps are an incredible resource.

---

## ✨ Features

- **Transparent proxying** — forwards any HTTP GET request to the configured origin
- **In-memory caching** — responses are stored and served instantly on subsequent requests
- **TTL-based expiry** — cached entries automatically expire after a configurable duration
- **X-Cache headers** — every response carries `X-Cache: HIT` or `X-Cache: MISS` so you can verify caching behaviour
- **Concurrent request handling** — multiple requests handled simultaneously via `ThreadingMixIn`, each in its own thread
- **Thread-safe cache** — all cache reads and writes protected with `threading.Lock()` to prevent race conditions
- **CLI interface** — start and control the proxy entirely from the command line
- **Zero external dependencies** — uses only Python's standard library + `requests`

---

## 📁 Project Structure

```
Proxy-server/
├── main.py         # Entry point — CLI argument parsing
├── proxy.py        # HTTP server and request handler
└── CacheStore.py   # In-memory cache with TTL support
```

---

## ⚙️ How It Works

```
Incoming request
      │
      ▼
ThreadedHTTPServer (ThreadingMixIn + HTTPServer)
      │
      ▼  spawns a new thread per request
      │
      ▼
 Cache lookup (CacheStore) ← protected by threading.Lock()
      │
   ┌──┴──┐
  HIT   MISS
   │      │
   │      ▼
   │  Fetch from origin
   │      │
   │      ▼
   │  Store in cache
   │      │
   └──────┤
          ▼
   Send response to client
   (with X-Cache: HIT/MISS)
```

On a **cache miss** the proxy fetches from the origin, stores the response, and returns it with `X-Cache: MISS`.
On a **cache hit** the stored response is returned immediately with `X-Cache: HIT` — the origin is never contacted.

Each request runs in its own thread, so multiple clients are served concurrently without queuing. The shared cache is protected by a `threading.Lock()` to prevent race conditions when two threads attempt to write the same key simultaneously.

---

## 🛠️ Installation

**Prerequisites:** Python 3.10+

1. Clone the repository
```bash
git clone https://github.com/Anubhav8176/Proxy-server.git
cd Proxy-server
```

2. Install dependencies
```bash
pip install requests
```

That's it — no virtual environment or complex setup required.

---

## 🚦 Usage

### Start the proxy

```bash
python main.py --port <PORT> --origin <ORIGIN_URL>
```

**Example** — proxy to dummyjson.com on port 3000:
```bash
python main.py --port 3000 --origin https://dummyjson.com
```

### Make requests through the proxy

```bash
# First request — fetches from origin
curl -v http://localhost:3000/products

# Second request — served from cache
curl -v http://localhost:3000/products
```

### Verify caching with X-Cache header

```bash
curl -s -o /dev/null -w "%{http_code}" -v http://localhost:3000/products 2>&1 | grep "X-Cache"

# First call:   X-Cache: MISS
# Second call:  X-Cache: HIT
```

---

## 🔬 Example Output

```
Server starting on port 3000 → https://dummyjson.com

[MISS] /products
[HIT]  /products
[MISS] /users/1
[HIT]  /users/1
[MISS] /products?limit=5
```

---

## 🧠 Key Concepts Demonstrated

| Concept | Where |
|---|---|
| HTTP request/response cycle | `proxy.py` — `do_GET()` |
| In-memory key-value caching | `CacheStore.py` — `CacheStore` class |
| TTL-based cache expiry | `CacheStore.py` — `is_expired()` |
| CLI argument parsing | `main.py` — `argparse` |
| Custom HTTP response headers | `proxy.py` — `X-Cache` header |
| Header filtering (hop-by-hop) | `proxy.py` — `SKIP_HEADERS` |
| Python dataclasses | `CacheStore.py` — `CacheEntry` |
| Concurrent request handling | `proxy.py` — `ThreadedHTTPServer` |
| Thread-safe cache writes | `CacheStore.py` — `threading.Lock()` |
| Python MRO / Mixin pattern | `proxy.py` — `ThreadingMixIn` inheritance |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `http.server` | Built-in HTTP server (stdlib) |
| `argparse` | CLI argument parsing (stdlib) |
| `dataclasses` | Structured cache entries (stdlib) |
| `time` | TTL expiry timestamps (stdlib) |
| `socketserver` | `ThreadingMixIn` for concurrent connections (stdlib) |
| `threading` | `Lock()` for thread-safe cache access (stdlib) |
| `requests` | Forwarding HTTP requests to origin |

---

---

## 🗺️ Built with roadmap.sh

This project was built as part of the **[Caching Server](https://roadmap.sh/projects/caching-server)** challenge from [roadmap.sh](https://roadmap.sh) — a community-driven platform with free, structured roadmaps for developers. The backend roadmap in particular is one of the best free resources for systematically building real-world backend skills.

If you're learning backend development, go check them out at **[roadmap.sh](https://roadmap.sh)**.

---

## 👤 Author

**Anubhav**
[GitHub @Anubhav8176](https://github.com/Anubhav8176)
