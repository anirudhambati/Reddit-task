import requests

files = {'file': open('file.txt','rb')}
r = requests.post('http://127.0.0.1:8000/api/', files=files)
print(r)
