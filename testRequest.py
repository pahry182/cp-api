from ast import For
import requests

BASE = "http://127.0.0.1:5000/"

data = [{"username": "pahry182", "password" : "1234"},
{"username": "pahry183", "password" : "123defr4"},
{"username": "pahry184", "password" : "123456"}]

for i in range(len(data)):
    response = requests.post(BASE + "account/" + data[i]['username'], json=data[i])
    print(response.json())

for i in range(len(data)):
    response = requests.get(BASE + f"account/{data[i]['username']}")
    print(response.json())

response = requests.get(BASE + f"account/{0}")
print(response.json())

score_data = [{'username': 'pahry182', 'tictactoe_score_easy' : 2 },
{'username': 'pahry183', 'tictactoe_score_easy' : 3 },
{'username': 'pahry184', 'tictactoe_score_easy' : 2 },
{'username' : 'telolet2',  'tictactoe_score_easy' : 19 }]

for i in range(len(score_data)):
    response = requests.put(BASE + f"tictactoe/{score_data[i]['username']}", json=score_data[i])
    print(response.json())

for i in range(len(score_data)):
    response = requests.get(BASE + f"tictactoe/{score_data[i]['username']}")
    print(response.json())

response = requests.get(BASE + f"tictactoe/all")
print(response.json())