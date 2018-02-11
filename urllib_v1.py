import ssl

from urllib.request import Request
from urllib.request import urlopen

context = ssl._create_unverified_context()

request = Request(
    url="https://foofish.net/pip.html",
    method="GET",
    headers={"Host": "foofish.net"},
    data=None,
)

response = urlopen(request, context=context)
# response = urlopen(request)
headers = response.info()
content = response.read()
code = response.getcode()

print(headers)
