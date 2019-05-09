import urllib.parse
import urllib.request

url = 'http://127.0.0.1:5000/wanderer/newlevel'
values = {
          'level' : 2,
         }

data = urllib.parse.urlencode(values)
data = data.encode('ascii') # data should be bytes
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
       response_data = response.read()

print(response_data)

