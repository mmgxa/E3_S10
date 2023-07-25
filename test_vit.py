import requests
import time
url = "http://127.0.0.1:8080/infer"

payload={}
files=[
  ('image',('dog.jpg',open('dog.jpg','rb'),'image/jpeg'))
]
headers = {}


start = time.perf_counter()
for _ in range(100):
  response = requests.request("GET", url, headers=headers, data=payload, files=files)
request_time = time.perf_counter() - start
print(f"Avg. Response time: {round(request_time/100*1000)}ms")
# print(response.text)
