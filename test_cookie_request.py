import requests
url ='https://playground.learnqa.ru/api/homework_cookie'
def test_get_cookie_value():
    response = requests.request('GET', url)
    assert response.cookies.get('HomeWork') == 'hw_value'
