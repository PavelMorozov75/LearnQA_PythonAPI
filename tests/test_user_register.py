from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertion


class TestUserRegister(BaseCase):

    # def setup(self):
    #     base_part = 'learnqa'
    #     domain = 'example.com'
    #     random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    #     self.email = f"{base_part}{random_part}@{domain}" #!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def test_create_user_successfully(self):
        # data = {
        #     'password': '123',
        #     'username': 'learnqa',
        #     'firstName': 'learnqa',
        #     'lastName': 'learnqa',
        #     'email': self.email
        # }

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
