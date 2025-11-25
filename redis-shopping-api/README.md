# 🛒 Redis Shopping API (Practice Project)

This project is a **complete dummy shopping application backend** built using:

- **FastAPI**
- **Redis (4 Logical Databases)**
- **Docker Compose**

It is designed for **learning Redis in real-world scenarios**, including caching, sessions, rate limiting, and cart management.

---

# 📌 Why This Project Exists

Real e-commerce backends (Amazon, Flipkart, Shopify) use Redis to:

- Speed up product browsing  
- Reduce database load  
- Store user sessions  
- Rate-limit aggressive requests  
- Maintain carts with fast operations  

This project gives you **all of those patterns in a simple way** so you can learn, practice, and extend it.

---

# 🔥 Why 4 Redis Logical Databases?

Redis DBs (0–15) are **logical partitions**, NOT separate servers.  
We use **4 databases** to keep data clean and separated:

| Redis DB | Purpose | Why? |
|----------|---------|------|
| **DB 0** | Product & Homepage Cache | Fast browsing, reduce DB load |
| **DB 1** | Sessions / Authentication | Should never mix with cache |
| **DB 2** | Rate Limiting | Stops spam & API abuse |
| **DB 3** | Cart & Temporary Data | Fast-changing user data |

This separation improves:

- Safety  
- Debugging  
- Easy clearing of specific DBs  
- Keeps each data type isolated  

---

# 🗂 Project Structure

```
redis-shopping-api/
│
├── backend/
│   ├── main.py               # FastAPI app
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Backend container
│
├── redis.conf                # Redis config (DB0–DB3)
├── docker-compose.yml        # All containers
└── README.md

```

---

# ⚙️ Redis Configuration (redis.conf)

```

databases 4
maxmemory 256mb
maxmemory-policy allkeys-lru
appendonly yes
appendfsync everysec
loglevel notice
timeout 0

```

### What Each Config Means

| Setting | Explanation |
|--------|-------------|
| `databases 4` | Creates DB0–DB3 |
| `maxmemory 256mb` | Memory cap |
| `maxmemory-policy allkeys-lru` | Evict least-used keys |
| `appendonly yes` | Durable persistence |
| `everysec` | Sync AOF every second |
| `timeout 0` | Never disconnect idle clients |

---

# 🚀 How to Run

### 1. Create project (if using generator script)
```
python3 generate_project.py
```

### 2. Start containers
```
docker compose up --build
```

### 3. Open API Docs
```
http://localhost:8000/docs
```

---

# 🧪 Dummy APIs & What They Use

### ✔ Product Cache — DB 0
```
GET /product/{id}
```
- First call = slow (simulated DB)
- Next calls = instant (Redis cache)

```
GET /homepage
```
Cached for 30 seconds.

---

### ✔ Authentication — DB 1
```
POST /login
GET /me
```

Stores session tokens in Redis DB1:
```
session:<token> → { "user_id": 101 }
```

---

### ✔ Rate Limiting — DB 2
Applied on:

- `/login`
- `/homepage`
- `/product/{id}`

Prevents spamming & API abuse.

---

### ✔ Cart System — DB 3
```
POST /cart/add
GET /cart
```

Stores user carts in DB3:
```
cart:<user_id>
```

Fast & isolated.

---

# 🎯 Summary

This project teaches:

- Redis caching
- Session handling
- Rate limiting
- Cart storage
- API optimization
- Dockerized microservices

Perfect for learning backend & DevOps skills.

Enjoy practicing Redis! 🚀
