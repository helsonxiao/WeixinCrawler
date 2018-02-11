import requests

url = "https://httpbin.org/headers"
headers = {'user-agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
print(r)

s = requests.Session()
s.cookies = requests.utils.cookiejar_from_dict({"a": "c"})
r = s.get("https://httpbin.org/cookies")
print(r.text)
