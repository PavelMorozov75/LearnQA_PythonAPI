import requests
import json
from time import sleep


base_url = "https://playground.learnqa.ru/ajax/api/longtime_job"
job_is_ok = 'Job is ready'
job_is_not_ready = 'Job is NOT ready'
response1 = requests.request('GET', base_url)
answer_dict1 = json.loads(response1.text)
payload = {'token': answer_dict1['token']}
response2 = requests.request('GET', base_url, params=payload)
answer_dict2 = json.loads(response2.text)
if answer_dict2['status'] == job_is_not_ready:
    print("Пока не готово, надо бы подождать")
waiting_time = answer_dict1['seconds']
sleep(waiting_time)
response3 = requests.request('GET', base_url, params=payload)
answer_dict3 = json.loads(response3.text)
if answer_dict3['status'] == job_is_ok:
    print('А вот теперь все норм.')
    print(f"Результат :  {answer_dict3['result']}")
