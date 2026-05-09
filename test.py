import requests

token = '7839084541:AAERFX89zJlduW59IdJjUduUpstZxx4RDCs'
resp = requests.get(f'https://api.telegram.org/bot{token}/getMe')
print(resp.json())

