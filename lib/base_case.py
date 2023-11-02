import json.decoder
from requests import Response
from datetime import datetime
import random
import string

class BaseCase:
    def generate_name(self, length):
        all_symbols = string.ascii_letters
        name = ''.join(random.choice(all_symbols) for _ in range(length))
        return name

    def create_email(self, status='good'):
        if status == 'good':
            basepart = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            return f"{basepart}{random_part}@{domain}"
        elif status == 'bad':
            basepart = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            return f"{basepart}{random_part}{domain}"

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"cant find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers,  f"cant find header with name {headers_name} in the last response"
        return response.headers[headers_name]
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is in not json format. Response text is {response.text}"
        assert name in response_as_dict, f"Response json doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            basepart = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{basepart}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_registration_bad_data(self, bad_parametr):

        if bad_parametr == 'email':
            email_parametr = 'bad'
            email = self.create_email(email_parametr)
            return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
            }
        elif bad_parametr == 'too_short_name':
            name_lenght = 1
            too_short_name = self.generate_name(name_lenght)
            email = self.create_email()
            return {
            'password': '123',
            'username': too_short_name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
            }
        elif bad_parametr == 'too_long_name':
            name_lenght = 255
            too_long_name = self.generate_name(name_lenght)
            email = self.create_email()
            return {
            'password': '123',
            'username': too_long_name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
            }

    def prepare_registration_data_without_parametr(self, parametr):
        if parametr == 'password':
            email = self.create_email()
            return {
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }
        elif parametr == 'username':
            email = self.create_email()
            return {
                'password': '123',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }
        elif parametr == 'firstName':
            email = self.create_email()
            return {
                'username': 'learnqa',
                'password': '123',
                'lastName': 'learnqa',
                'email': email
            }
        elif parametr == 'lastName':
            email = self.create_email()
            return {
                'username': 'learnqa',
                'password': '123',
                'firstName': 'learnqa',
                'email': email
            }
        elif parametr == 'email':
            return {
                'username': 'learnqa',
                'password': '123',
                'firstName': 'learnqa',
                'lastName': 'learnqa'
            }







