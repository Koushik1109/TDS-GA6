import requests
url = "https://exam.sanand.workers.dev/716bc14c-2fdb-47a1-a506-7ab753bafb54"
headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get(url, headers=headers)
print(resp.status_code)
print(resp.text[:500])
