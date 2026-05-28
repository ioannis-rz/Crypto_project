import requests
import os
from concurrent.futures import ThreadPoolExecutor
import time

url = "https://127.0.0.1:5000/login"
payload = {
    "username": "aaa",
    "password": "2"
}
def send_request(i):
    start = time.time()
    try:
        response = requests.post(url, data=payload, timeout=10)
        elapsed = time.time() - start
        try:
            pass
            # message = response.json().get("message", "")
        except ValueError:
            message = response.text
        print(f"{i} | {response.status_code} | {elapsed:.2f}s")
    except requests.exceptions.RequestException as e:
        print(f"{i} | Error: {e}")

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    executor.map(send_request, range(100))
