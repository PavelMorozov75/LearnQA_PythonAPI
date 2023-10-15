import requests
base_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
success_answer = requests.request('GET', base_url, params={'method': 'GET'}).text
wrong_answer = requests.request('GET', base_url, params={'method': 'POST'}).text
methods = ['', 'HEAD', 'GET', 'POST', 'PUT', 'DELETE']
for method in methods:
    if method == '':
        methods_without_empty = methods
        methods_without_empty.remove('')
        for metod in methods_without_empty:
            response = requests.request(metod, base_url)
            print(f"если параметр не передан в методе {metod}, то ответ: {response.text}")
    elif method == 'GET':
        payload = {'method': method}
        response = requests.request(method, base_url, params=payload)
        print(f"запрос методом {method}, ответ: {response.text}")

    else:
        payload = {'method': method}
        response = requests.request(method, base_url, data=payload)
        print(f"запрос методом {method}, ответ: {response.text}")
methods1 = ['GET', 'POST', 'PUT', 'DELETE']
for method in methods1:
    for param in methods1:
        payload = {'method': param}
        if method == 'GET':
            response = requests.request(method, base_url, params=payload)
            print(f"запрос методом {method}, параметр: {param} , ответ: {response.text}")
            if method != param and response.text == success_answer:
                print(f"при методе {method}, и не совпадающем параметре: {param} успешный ответ")
            elif method == param and response.text == wrong_answer:
                print(f"при методе {method},  и совпадающем параметре: {param} неуспешный ответ")
        else:
            response = requests.request(method, base_url, data=payload)
            print(f"запрос методом {method}, параметр: {param} , ответ: {response.text}")
            if method != param and response.text == success_answer:
                print(f"при методе {method}, и не совпадающем параметре: {param} успешный ответ")
            elif method == param and response.text == wrong_answer:
                print(f"при методе {method},  и совпадающем параметре: {param} неуспешный ответ")
