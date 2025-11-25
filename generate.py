import os

# -----------------------------
# Helper to write files safely
# -----------------------------
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

# -----------------------------
# Project Structure
# -----------------------------
BASE = "redis-shopping-api"

files = {
    f"{BASE}/backend/main.py": """import json
import uuid
import time

import redis
from fastapi import FastAPI, HTTPException, Request, Depends

app = FastAPI(title="Redis Shopping API")

cache_db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
session_db = redis.Redis(host="redis", port=6379, db=1, decode_responses=True)
ratelimit_db = redis.Redis(host="redis", port=6379, db=2, decode_responses=True)
cart_db = redis.Redis(host="redis", port=6379, db=3, decode_responses=True)

FAKE_PRODUCTS = {
    1: {"id": 1, "name": "iPhone 15", "price": 80000, "stock": 5},
    2: {"id": 2, "name": "MacBook Pro", "price": 180000, "stock": 3},
}

FAKE_USERS = {"user@example.com": {"id": 101, "password": "password123"}}

HOMEPAGE_DATA = {
    "banners": ["Offer 1", "Offer 2"],
    "featured": [1, 2],
}

def db_get_product(pid: int):
    time.sleep(0.1)
    return FAKE_PRODUCTS.get(pid)

async def rate_limit(request: Request, limit: int = 10, seconds: int = 60):
    ip = request.client.host
    route = request.url.path
    key = f"ratelimit:{ip}:{route}"

    hits = ratelimit_db.incr(key)
    if hits == 1:
        ratelimit_db.expire(key, seconds)

    if hits > limit:
        ttl = ratelimit_db.ttl(key)
        raise HTTPException(429, f"Rate limit exceeded. Retry in {ttl}s")

def create_session(user_id: int):
    token = str(uuid.uuid4())
    session_db.set(f"session:{token}", json.dumps({"user_id": user_id}), ex=3600)
    return token

def get_user(token: str):
    data = session_db.get(f"session:{token}")
    return json.loads(data) if data else None

async def auth_required(req: Request):
    header = req.headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        raise HTTPException(401, "Missing token")

    token = header.split()[1]
    user = get_user(token)
    if not user:
        raise HTTPException(401, "Invalid or expired session")
    return user

@app.get("/product/{pid}")
async def get_product(pid: int, req: Request):
    await rate_limit(req)
    key = f"product:{pid}"

    cached = cache_db.get(key)
    if cached:
        return {"source": "redis_db0", "data": json.loads(cached)}

    product = db_get_product(pid)
    if not product:
        raise HTTPException(404)

    cache_db.set(key, json.dumps(product), ex=120)
    return {"source": "database", "data": product}

@app.get("/homepage")
async def homepage(req: Request):
    await rate_limit(req)
    cached = cache_db.get("homepage")

    if cached:
        return {"source": "redis_db0", "data": json.loads(cached)}

    time.sleep(0.2)
    cache_db.set("homepage", json.dumps(HOMEPAGE_DATA), ex=30)
    return {"source": "generated", "data": HOMEPAGE_DATA}

@app.post("/login")
async def login(email: str, password: str):
    user = FAKE_USERS.get(email)
    if not user or user["password"] != password:
        raise HTTPException(401)

    token = create_session(user_id=user["id"])
    return {"token": token}

@app.get("/me")
async def me(session=Depends(auth_required)):
    return {"user_id": session["user_id"]}

@app.post("/cart/add")
async def add_to_cart(pid: int, qty: int = 1, session=Depends(auth_required)):
    user_id = session["user_id"]
    key = f"cart:{user_id}"

    cart_data = cart_db.get(key)
    cart = json.loads(cart_data) if cart_data else []
    cart.append({"pid": pid, "qty": qty})

    cart_db.set(key, json.dumps(cart), ex=3600)
    return {"message": "Added to cart", "cart": cart}

@app.get("/cart")
async def get_cart(session=Depends(auth_required)):
    user_id = session["user_id"]
    key = f"cart:{user_id}"

    cart = cart_db.get(key)
    return {"cart": json.loads(cart) if cart else []}

@app.get("/")
def root():
    return {"message": "Redis Shopping Dummy API running"}
""",

    f"{BASE}/backend/requirements.txt": """fastapi
uvicorn[standard]
redis
""",

    f"{BASE}/backend/Dockerfile": """FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
""",

    f"{BASE}/redis.conf": """databases 4
maxmemory 256mb
maxmemory-policy allkeys-lru
appendonly yes
appendfsync everysec
loglevel notice
timeout 0
""",

    f"{BASE}/docker-compose.yml": """version: "3.9"

services:
  redis:
    image: redis:7-alpine
    container_name: redis_server
    volumes:
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: ["redis-server","/usr/local/etc/redis/redis.conf"]
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    container_name: redis_api
    depends_on:
      - redis
    ports:
      - "8000:8000"
    environment:
      REDIS_HOST: redis
""",

    f"{BASE}/README.md": """# Redis Shopping Dummy API

This project is a complete working dummy shopping API using Redis DB 0–3.

### Redis DB Usage
| DB | Purpose |
|----|---------|
| DB 0 | Cache (Products, Homepage) |
| DB 1 | Sessions & Authentication |
| DB 2 | Rate Limiting |
| DB 3 | Cart Storage |

### Start Project

docker compose up --build

### API Endpoints
- `GET /product/{id}`
- `GET /homepage`
- `POST /login`
- `GET /me`
- `POST /cart/add`
- `GET /cart`

Enjoy practicing Redis!
"""
}

# -----------------------------
# Write all files
# -----------------------------
for path, content in files.items():
    write(path, content)

print("\nProject created successfully! 🎉")