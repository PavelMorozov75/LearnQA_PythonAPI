from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertion
import time
import allure

@allure.epic("Задача по расстановке тегов allure")
@allure.suite("Тесты на редактирование данных пользователя")
class TestUserEdit(BaseCase):
    @allure.tag("API")
    @allure.description("успешное редактирование данных только что созданного авторизованного пользователя")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email = register_data['email']
        first_name = register_data['firstName']
        last_name = register_data['lastName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data ={
            'email': email,
            'password': password
        }
        responce2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(responce2, 'auth_sid')
        token = self.get_header(responce2, 'x-csrf-token')

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid },
                                 data={'firstName': new_name}
                                 )
        Assertion.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid}
                                 )
        Assertion.assert_json_value_by_name(response4,
                                            'firstName', new_name,
                                            "Wrong name of the user after edit")
        Assertion.assert_json_value_by_name(response4,
                                            'lastName', last_name,
                                            "Wrong name of the user after edit")

    @allure.tag("API")
    @allure.description("не успешное редактирование данных неавторизованного пользователя")
    def test_edit_unauthorized_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        #EDIT
        new_name = "Changed Name"
        response2 = MyRequests.put(f"/user/{user_id}", data={'firstName': new_name}
                                   )
        Assertion.assert_code_status(response2, 400)

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        responce3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(responce3, 'auth_sid')
        token = self.get_header(responce3, 'x-csrf-token')

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )
        #проверим, что имя не изменилось
        Assertion.assert_json_value_by_name(response4,
                                            'firstName',first_name,
                                            "Wrong name of the user after edit")

    @allure.tag("API")
    @allure.description("не успешное редактирование данных неавторизаванного пользователя при указании регистрационных"
                        ""
                        " данных другого авторизованного пользователя")
    def test_authorized_user_edit_another_user(self):
        # REGISTER1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email1 = register_data1['email']
        first_name1 = register_data1['firstName']
        password1 = register_data1['password']

        # LOGIN1
        login_data1 = {
            'email': email1,
            'password': password1
        }
        responce2 = MyRequests.post("/user/login", data=login_data1)
        auth_sid1 = self.get_cookie(responce2, 'auth_sid')
        token1 = self.get_header(responce2, 'x-csrf-token')

        # REGISTER2
        time.sleep(1) #делаем так чтобы у мользователей не был одинаковый email
        register_data2 = self.prepare_registration_data()
        response3 = MyRequests.post("/user/", data=register_data2)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email2 = register_data2['email']
        password2 = register_data2['password']
        user_id2 = self.get_json_value(response3, 'id')

        # EDIT редактируем второго пользователя используя авторицационные данные первого
        new_name = "Changed Name"

        response4 = MyRequests.put(f"/user/{user_id2}",
                                   headers={'x-csrf-token': token1},
                                   cookies={'auth_sid': auth_sid1},
                                   data={'firstName': new_name}
                                   )
        Assertion.assert_code_status(response4, 200)

        # LOGIN2 авторизуем второго пользователя
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response5 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response5, 'auth_sid')
        token2 = self.get_header(response5, 'x-csrf-token')

        # GET получаем данные по второму пользователю будучи авторизованными
        response6 = MyRequests.get(f"/user/{user_id2}",
                                   headers={'x-csrf-token': token2},
                                   cookies={'auth_sid': auth_sid2}
                                   )
        # проверим, что имя НЕ изменилось
        Assertion.assert_json_value_by_name(response6,
                                              'firstName', first_name1,
                                              "Wrong name of the user after edit")

    @allure.tag("API")
    @allure.description("не успешное редактирование данных пользователя: изменение email на новый без символа @")
    def test_edit_email_new_email_without_at(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        responce2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(responce2, 'auth_sid')
        token = self.get_header(responce2, 'x-csrf-token')

        # EDIT
        email_status = 'bad'
        new_email = self.create_email(email_status)
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'email': new_email}
                                   )
        Assertion.assert_code_status(response3, 400)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                  )
        #проверяем, что email не изменился
        Assertion.assert_json_value_by_name(response4,
                                            'email', email,
                                            "Wrong email after edit")

    @allure.tag("API")
    @allure.description("не успешное редактирование пользователя, новое имя длиной в 1 символ")
    def test_edit_firstname_new_name_is_too_short(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        responce2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(responce2, 'auth_sid')
        token = self.get_header(responce2, 'x-csrf-token')

        # EDIT
        number_of_characters = 1
        new_name = self.generate_name(number_of_characters)
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'email': new_name}
                                   )
        Assertion.assert_code_status(response3, 400)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )
        Assertion.assert_json_value_by_name(response4,
                                            'firstName', first_name,
                                            "Wrong name of the user after edit")


