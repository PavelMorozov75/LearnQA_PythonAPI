import requests
'''
from json.decoder import JSONDecodeError
payload ={"name": "User"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response.text)
print(response.json()['answer'])

print(response.content)
print(response.headers)

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
try :
    parsed_text = response.json()
    print((parsed_text))
except JSONDecodeError:
    print('it is not jsom format')
'''

'''
response = requests.post("https://playground.learnqa.ru/api/check_type")
print(response.text)
'''

'''
response = requests.get("https://playground.learnqa.ru/api/check_type", params={'param1': 'value1'})
print(response.text)
print((response.status_code))

response = requests.post("https://playground.learnqa.ru/api/check_type", data={'param1': 'value1'})
print(response.text)
'''

'''
response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects= False)
print(response.status_code)
'''


response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects= True)
firs_response = response.history[0]
print(len(response.history))
second_responce = response
print(firs_response.url)
print(firs_response.headers)
print(second_responce.url)
print(response.text) #запрос
print(response.headers) #ответ сервера
print(response.request.headers) #заголовки отправляемые библиотекой requests


'''
headers ={'some_header': '123'}
response = requests.get('https://playground.learnqa.ru/api/show_all_headers', headers)
print(response.text) #запрос
print(response.headers) #ответ сервера
print(response.request.headers) #заголовки отправляемые библиотекой requests
'''
'''
payload = {"login":"secret_login", "password":"secret_pass1"}
response1 = requests.post('https://playground.learnqa.ru/api/get_auth_cookie', data=payload)
cookie_value = response1.cookies.get('auth_cookie')#Вернет None, если такой куки нет
print(cookie_value)
#cookie_value1 = response1.cookies['auth_cookie']
#print(cookie_value1)
cookies ={}
if cookie_value is not None:
    cookies.update({'auth_cookie': cookie_value})
print(cookies)
response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
print(response2.text)
'''

'''
import json,requests
json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
dict_text = json.loads(json_text)
print(dict_text['messages'][1]['message'])
'''