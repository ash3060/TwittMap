import requests

r = requests.post("http://127.0.0.1:8000/", data={'number': 12524, 'type': 'issue', 'action': 'show'})
print(r.status_code, r.reason)
