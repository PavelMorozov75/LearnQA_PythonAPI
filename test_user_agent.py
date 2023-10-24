import requests
import csv
import pytest
from json.decoder import JSONDecodeError
from requests import Response

base_url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'

def read_csv():
    with open("data_user_agent.csv") as f:
        reader = csv.reader(f)
        return [[row[0], row[1], row[2], row[3]] for row in reader]

data_for_test = read_csv()

def check_user_agent(user_agent, response: Response, expected_platform, expected_browser, expected_device):
    try:
        response_as_dict = response.json()
    except JSONDecodeError:
        assert False, f"it is not jsom format"
    received_platform = response_as_dict['platform']
    received_browser = response_as_dict['browser']
    received_device = response_as_dict['device']
    assert received_platform == expected_platform, (f"для User_Agent {user_agent} ждали платформу {expected_platform}, "
                                                     f"получили {received_platform}")
    assert received_browser == expected_browser, (f"для User_Agent {user_agent} ждали браузер {expected_browser}, "
                                                   f"получили {received_browser}")
    assert received_device == expected_device, (f"для User_Agent {user_agent} ждали девайс {expected_device},"
                                                f" получили {received_device}")
@pytest.mark.parametrize('user_agent, expected_platform, expected_browser, expected_device', data_for_test)
def test_user_agent(user_agent, expected_platform, expected_browser, expected_device):
    payload = {'User-Agent': user_agent}
    response = requests.get(base_url, headers=payload)
    check_user_agent(user_agent, response, expected_platform, expected_browser, expected_device)








