# login_stress_test.py

import concurrent.futures
import requests
import time

URL = "http://127.0.0.1:8000/auth/login"

DATA = {
    "email": "harshilkalsariya6@gmail.com",
    "password": "WrongPassword123"
}

TOTAL_REQUESTS = 1000
CONCURRENT_WORKERS = 100

def attack(_):
    try:
        r = requests.post(URL, json=DATA, timeout=5)
        return r.status_code
    except Exception:
        return "ERROR"

start = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
    results = list(executor.map(attack, range(TOTAL_REQUESTS)))

end = time.time()

print(f"Time: {end-start:.2f}s")
print(f"200: {results.count(200)}")
print(f"401: {results.count(401)}")
print(f"500: {results.count(500)}")
print(f"Errors: {results.count('ERROR')}")