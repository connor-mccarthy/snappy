import requests

url = "http://localhost:9000/2015-03-31/functions/function/invocations"

payload = '{"name": "connor"}'
headers = {"Content-Type": "text/plain"}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
