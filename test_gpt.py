import requests
import json
import time

url = "http://127.0.0.1:8080/infer"

payload = json.dumps({
  "text": "hello",
  "max_tokens": 8,
  "temperature": 1
})
headers = {
  'Content-Type': 'application/json'
}

start = time.perf_counter()
for _ in range(100):
  response = requests.request("GET", url, headers=headers, data=payload)
request_time = time.perf_counter() - start
print(f"Avg. Response time: {round(request_time/100*1000)}ms")
# print(response.text)