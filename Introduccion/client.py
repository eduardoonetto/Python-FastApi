from urllib import request

URL = 'http://localhost:8082'

response = request.urlopen(URL)

print(response.read())