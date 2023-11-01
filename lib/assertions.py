from requests import Response
import json
class Assertion:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in json format. Response text is '{response.text}'"
        assert name in  response_as_dict, f"Response json doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in json format. Response text is '{response.text}'"
        assert name in  response_as_dict, f"Response json doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in json format. Response text is '{response.text}'"
        for name in names: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            assert name in response_as_dict, f"Response json doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in json format. Response text is '{response.text}'"
        assert name not in response_as_dict, f"Response json shudtn't have key '{name}'. But it is present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, (f"Unexpected status code! Expected {expected_status_code} "
                                                              f"Actual:  {response.status_code}")