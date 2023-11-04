from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertion


class TestUserDelete(BaseCase):
    def test_delete_user_2(self):

        #LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        responce1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(responce1, 'auth_sid')
        token = self.get_header(responce1, 'x-csrf-token')

        #DELETE
        response2 = MyRequests.delete(f"/user/2",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )
        Assertion.assert_code_status(response2, 400)

        # GET
        response3 = MyRequests.get(f"/user/2",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )
        # проверим, что имя не изменилось
        expected_email = 'vinkotov@example.com'
        Assertion.assert_json_value_by_name(response3,
                                            'email', expected_email,
                                            "expected email don't exist, presumably "
                                            "the user has been deleted")

    def test_successful_deletion_of_an_authorized_user(self):
        # REGISTER1
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
        login_data = {
            'email': email,
            'password': password
        }
        responce2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(responce2, 'auth_sid')
        token = self.get_header(responce2, 'x-csrf-token')

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )
        Assertion.assert_code_status(response3, 200)
        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )
        #проверим, что пользователь удален и не доступен к получению
        Assertion.assert_code_status(response4, 404)

    def test_deleting_another_user(self):
        # REGISTER1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email1 = register_data1['email']
        first_name1 = register_data1['firstName']
        last_name1 = register_data1['lastName']
        password1 = register_data1['password']
        user_id1 = self.get_json_value(response1, 'id')

        # LOGIN1
        login_data = {
            'email': email1,
            'password': password1
        }
        responce2 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(responce2, 'auth_sid')
        token1 = self.get_header(responce2, 'x-csrf-token')

        # REGISTER2

        register_data2 = self.prepare_registration_data()
        response3 = MyRequests.post("/user/", data=register_data2)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, 'id')
        email2 = register_data2['email']
        first_name2 = register_data2['firstName']
        last_name2 = register_data2['lastName']
        password2 = register_data2['password']
        user_id2 = self.get_json_value(response3, 'id')

        # LOGIN2
        login_data2 = {
            'email': email2,
            'password': password2
        }
        responce4 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2= self.get_cookie(responce4, 'auth_sid')
        token2 = self.get_header(responce4, 'x-csrf-token')

        # DELETE
        response5 = MyRequests.delete(f"/user/{user_id2}",
                                      headers={'x-csrf-token': token1},
                                      cookies={'auth_sid': auth_sid1}
                                      )
        Assertion.assert_code_status(response5, 200)

        # GET получим неавторизованного ранее пользователя
        response6 = MyRequests.get(f"/user/{user_id2}",
                                   headers={'x-csrf-token': token2},
                                   cookies={'auth_sid': auth_sid2}
                                   )
        # проверим, что пользователь удален и не доступен к получению, а он получен!!!
        Assertion.assert_code_status(response6, 200)

        # GET получим авторизованного пользователя
        response6 = MyRequests.get(f"/user/{user_id1}",
                                   headers={'x-csrf-token': token1},
                                   cookies={'auth_sid': auth_sid1}
                                   )
        # оказывается авторизованный пользователь удален !!
        Assertion.assert_code_status(response6, 404)




