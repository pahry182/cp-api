import requests

BASE = "http://127.0.0.1:5000/"

data = [{"username": "pahry182", "password" : "1234"},
{"username": "pahry183", "password" : "123defr4"},
{"username": "pahry184", "password" : "123456"}]

for i in range(len(data)):
    response = requests.put(BASE + "account/" + str(i), json=data[i])
    print(response.json())

for i in range(len(data)):
    response = requests.get(BASE + f"account/{i}")
    print(response.json())