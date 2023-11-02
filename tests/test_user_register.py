import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertion


class TestUserRegister(BaseCase):

    missing_params = ['password', 'username', 'firstName', 'lastName', 'email']

    def test_create_user_successfully(self):

        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 200)
        Assertion.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'winkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 400)
        # ответ приходит с буквой d в начале и требует раскодировки
        assert response.content.decode('utf-8') == f"Users with email 'winkotov@example.com' already exists",\
            f"Unexpected response {response.content}"

    def test_create_user_with_too_short_name(self):
        bad_parametr = 'too_short_name'
        data = self.prepare_registration_bad_data(bad_parametr)
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short", \
        f"Unexpected response {response.content}"

    def test_create_user_with_too_long_name(self):
        bad_parametr = 'too_long_name'
        data = self.prepare_registration_bad_data(bad_parametr)
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too long", \
        f"Unexpected response {response.content}"

    @pytest.mark.parametrize('parametr', missing_params)
    def test_create_user_without_parametr(self, parametr):
        data = self.prepare_registration_data_without_parametr(parametr)
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The following required params are missed: {parametr}", \
            f"Unexpected response {response.content}"





