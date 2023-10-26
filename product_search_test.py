import requests

session = requests.Session()

base_url = "http://127.0.0.1:5000"

data1 = {'username': 'AdminAndy', 'password': 'password123'}

response1 = session.post("http://127.0.0.1:5000/login", json=data1)
print(response1.text)

response1 = session.get("http://127.0.0.1:5000/getUser")
print(response1.text)

response1 = session.get("http://127.0.0.1:5000/getProducts")
print(response1.text)

response1 = session.get("http://127.0.0.1:5000/getTags")
print(response1.text)

response1 = session.get("http://127.0.0.1:5000/getCategories")
print(response1.text)

response1 = session.get("http://127.0.0.1:5000/searchProducts?query=almond")
print(response1.text)

response2 = session.get("http://127.0.0.1:5000/logout")
print(response2.text)

session.close()