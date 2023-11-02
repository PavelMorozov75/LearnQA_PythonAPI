from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertion

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertion.assert_json_has_key(response, "username")
        Assertion.assert_json_has_not_key(response, "email")
        Assertion.assert_json_has_not_key(response, "firstName")
        Assertion.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1,"x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        # print(user_id_from_auth_method)
        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid})
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertion.assert_json_has_keys(response2, expected_fields)

    def test_get_data_from_another_user(self):
        #создание первого пользователя
        data_user_1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data_user_1)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        data = {
            'email': data_user_1['email'],
            'password': data_user_1['password']
        }
        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")
        #успешное получение решистрационных данных залогиненным пользователем
        response3 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertion.assert_json_has_keys(response3, expected_fields)
        #создание второго пользователя
        data_user_2 = self.prepare_registration_data()
        response4 = MyRequests.post("/user/", data=data_user_2)
        Assertion.assert_code_status(response4, 200)
        Assertion.assert_json_has_key(response1, 'id')
        user_2_user_id = self.get_json_value(response4, 'id')
        #попытка получить регистрационные данные втого пользователя с токеном и куки первого
        response5 = MyRequests.get(f"/user/{user_2_user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        Assertion.assert_json_has_key(response5, "username")
        Assertion.assert_json_has_not_key(response5, "email")
        Assertion.assert_json_has_not_key(response5, "firstName")
        Assertion.assert_json_has_not_key(response5, "lastName")

