import json
import uuid
import time
import asyncio

import redis
from fastapi import FastAPI, HTTPException, Request, Depends
from prometheus_fastapi_instrumentator import Instrumentator, metrics

app = FastAPI(title="Redis Shopping API")

# Redis connections
cache_db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
session_db = redis.Redis(host="redis", port=6379, db=1, decode_responses=True)
ratelimit_db = redis.Redis(host="redis", port=6379, db=2, decode_responses=True)
cart_db = redis.Redis(host="redis", port=6379, db=3, decode_responses=True)

# Configure Prometheus with custom histogram buckets
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=False,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    inprogress_name="http_requests_inprogress",
    inprogress_labels=True
)

# Add custom latency metric with fine-grained buckets for API response tracking
instrumentator.add(
    metrics.latency(
        buckets=(
            0.001,  # 1ms   - Ultra-fast cache hits
            0.005,  # 5ms   - Very fast responses
            0.01,   # 10ms  - Fast responses
            0.025,  # 25ms  - Quick responses
            0.05,   # 50ms  - Normal responses
            0.1,    # 100ms - Acceptable responses
            0.25,   # 250ms - Slower responses
            0.5,    # 500ms - Slow responses
            1.0,    # 1s    - Very slow responses
            2.5,    # 2.5s  - Extremely slow
            5.0,    # 5s    - Timeout territory
            10.0,   # 10s   - Severe issues
        ),
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_name="http_request_duration_seconds",
        metric_doc="Duration of HTTP requests in seconds"
    )
)

# Add request/response size tracking
instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace="",
        metric_subsystem="",
    )
).add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace="",
        metric_subsystem="",
    )
)

# Instrument the FastAPI app and expose /metrics endpoint
instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=True)

# Fake data
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
    time.sleep(0.1)  # Simulate database query
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


@app.get("/")
def root():
    return {"message": "Redis Shopping Dummy API running"}


@app.get("/product/{pid}")
async def get_product(pid: int, req: Request):
    await rate_limit(req)
    key = f"product:{pid}"

    # Check cache first
    cached = cache_db.get(key)
    if cached:
        # Return immediately from cache (fast!)
        return {"source": "redis_db0", "data": json.loads(cached)}

    # Cache miss - sleep 2 seconds before fetching from DB
    await asyncio.sleep(2)
    
    product = db_get_product(pid)
    if not product:
        raise HTTPException(404)

    cache_db.set(key, json.dumps(product), ex=120)
    return {"source": "database", "data": product}


@app.get("/homepage")
async def homepage(req: Request):
    await rate_limit(req)
    
    # Check cache first
    cached = cache_db.get("homepage")
    if cached:
        # Return immediately from cache (fast!)
        return {"source": "redis_db0", "data": json.loads(cached)}

    # Cache miss - sleep 2 seconds before generating
    await asyncio.sleep(2)
    time.sleep(0.2)  # Simulate generation
    
    cache_db.set("homepage", json.dumps(HOMEPAGE_DATA), ex=30)
    return {"source": "generated", "data": HOMEPAGE_DATA}


@app.post("/login")
async def login(email: str, password: str):
    # Check session cache first
    session_key = f"login_attempt:{email}"
    cached_token = session_db.get(session_key)
    
    if cached_token:
        # Return cached session immediately
        return {"token": cached_token, "source": "cached"}
    
    # Not cached - sleep 2 seconds
    await asyncio.sleep(2)
    
    user = FAKE_USERS.get(email)
    if not user or user["password"] != password:
        raise HTTPException(401)

    token = create_session(user_id=user["id"])
    # Cache the token for quick subsequent logins
    session_db.set(session_key, token, ex=300)
    return {"token": token, "source": "new"}


@app.get("/me")
async def me(session=Depends(auth_required)):
    # User data is already from cache (session_db), return immediately
    return {"user_id": session["user_id"]}


@app.post("/cart/add")
async def add_to_cart(pid: int, qty: int = 1, session=Depends(auth_required)):
    user_id = session["user_id"]
    key = f"cart:{user_id}"

    # Check if cart exists in cache
    cart_data = cart_db.get(key)
    
    if cart_data:
        # Cart exists in cache - fast operation
        cart = json.loads(cart_data)
    else:
        # New cart - sleep 2 seconds
        await asyncio.sleep(2)
        cart = []
    
    cart.append({"pid": pid, "qty": qty})
    cart_db.set(key, json.dumps(cart), ex=3600)
    
    return {"message": "Added to cart", "cart": cart}


@app.get("/cart")
async def get_cart(session=Depends(auth_required)):
    user_id = session["user_id"]
    key = f"cart:{user_id}"

    # Check cache first
    cart = cart_db.get(key)
    
    if cart:
        # Return immediately from cache (fast!)
        return {"cart": json.loads(cart), "source": "cached"}
    
    # No cart in cache - sleep 2 seconds
    await asyncio.sleep(2)
    return {"cart": [], "source": "new"}
