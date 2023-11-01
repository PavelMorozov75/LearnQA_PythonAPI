import os
#set ENV=dev

class Environment:
    DEV = 'dev'
    PROD = 'prod'

    URLS = {
        DEV: "https://playground.learnqa.ru/api_dev",
        PROD: "https://playground.learnqa.ru/api"
    }

    def __init__(self):
        try:
            self.env = os.environ['ENV']
            print('переменная среды', self.env)
        except KeyError:
            self.env = self.DEV

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Unknown value ENV variable {self.env}")

ENV_OBJECT = Environment()