import requests
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertion
# import allure

# @allure.epic("Кейсы по авторизации")
class TestUserAuth(BaseCase):

    exlude_params = ['no_cookie', 'no_token']
    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")


    # @allure.description("Тест на успешную авторизацию по email и password")
    def test_auth_user(self):
        response2 = MyRequests.get("/user/auth",
                                 headers={'x-csrf-token': self.token},
                                 cookies={'auth_sid': self.auth_sid})
        Assertion.assert_json_value_by_name(response2, 'user_id', self.user_id_from_auth_method,
                                            "User id from auth method is not equal to user_id "
                                            "from check method")

    # @allure.description("Тест на неуспешную  авторизацию без куки, без токена")
    @pytest.mark.parametrize('condition', exlude_params)
    def test_negativ_auth_check(self, condition):
        if condition == 'no_cookie':
            response2 = MyRequests.get("/user/auth",
                                     headers={'x-csrf-token': self.token})
        else:
            response2 = MyRequests.get("/user/auth",
                                     cookies={'auth_sid': self.auth_sid})
        Assertion.assert_json_value_by_name(response2, 'user_id', 0,
                                            f"user is authorised with condition {condition}")
