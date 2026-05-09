import requests

token = '-'
resp = requests.get(f'https://api.telegram.org/bot{token}/getMe')
print(resp.json())

