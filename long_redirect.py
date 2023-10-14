import requests
response = requests.get(" https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
print(f"всего было редиректов:  {len(response.history)}")
for resp in response.history:
    print(f"адрес с которого ушли:  {resp.url}")
print(f"итоговый url:  {response.url}")

