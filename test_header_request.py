import requests
url = 'https://playground.learnqa.ru/api/homework_header'
expected_header = 'Some secret value'


def test_get_header_value():
    response = requests.request('GET', url)
    print(response.headers)
    assert response.headers.get('x-secret-homework-header') == expected_header, f"expected header not received"
