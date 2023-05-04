import requests

payload = {
    "email": "admin@admin.net",
    "password": "12345"
}
resp = requests.put("http://localhost:8080/admin/setup", data=payload)
print(resp.status_code)
print(resp.text)
'''
curl -X 'PUT' \
  'http://localhost:8080/admin/setup?email=admin%40admin.net&password=12345' \
  -H 'accept: application/json'
'''