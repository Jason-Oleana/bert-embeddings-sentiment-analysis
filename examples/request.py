import requests
import json

headers = {'accept': 'application/json',
           'Content-Type': 'application/json'
          }

text = 'i am not happy'
json_data = {'text': text}

url = 'http://localhost:8000/predict'

response = requests.post(url=url, headers=headers, json=json_data)
result = json.loads(response.text)

print(result)