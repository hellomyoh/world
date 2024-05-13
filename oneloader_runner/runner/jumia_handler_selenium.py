from oneloader_runner.modules.one_logging import OneLogger
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from seleniumrequests import Chrome
from time import sleep
import json
from pathlib import Path
import pickle
import re
import shutil
import os

log = OneLogger()

class JumiaBot(object):
    def __init__(self, login_info: dict):
        self.login_info = login_info
        selenium_cookie = f'{self.login_info["shop_name"]}.json'
        selenium_cookie_path = f'{self.login_info["shop_name"]}-chrom-data'
        if os.path.exists(selenium_cookie):
            os.remove(selenium_cookie)
        if os.path.exists(selenium_cookie_path):
            shutil.rmtree(selenium_cookie_path)

        self.service = Service(ChromeDriverManager().install())
        self.chrome_options = Options()
        self.chrome_options.add_argument(
            f"--user-data-dir={selenium_cookie_path}")
        # self.chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
        # self.chrome_options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(
            service=self.service, options=self.chrome_options)

        # Navigate to the Amazon URL.
        try:
            self.driver.get(self.login_info["register_url"])
        except Exception as e:
            log.error(f'Selenium driver get Failed: {e}')
        # sleep(10)
        Path(selenium_cookie).write_text(
            json.dumps(self.driver.get_cookies(), indent=2)
        )

        # retrieve cookies from a json file
        for cookie in json.loads(Path(selenium_cookie).read_text()):
            self.driver.add_cookie(cookie)

        # Obtain the source
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.html = self.soup.prettify('utf-8')
        #log.info(f'{self.html}')

    def click_to_sell_login(self):
        # click `sign in with Email`
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(
                (By.XPATH,
                 '/html/body/jumia-vnp-root/vnp-theme/div/mat-sidenav-container/mat-sidenav-content/jumia-vnp-sign-in/main/mat-card/div[1]/div/button[2]')))
        except Exception as e:
            log.error(f'page loading faild : {e}')

        self.sign_in_with_jumia_btn = self.driver.find_element(
            By.XPATH,
            '/html/body/jumia-vnp-root/vnp-theme/div/mat-sidenav-container/mat-sidenav-content/jumia-vnp-sign-in/main/mat-card/div[1]/div/button[2]').click()

        # input  email/password
        try:
            # wait for login button
            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="kc-login"]')))
        except Exception as e:
            log.error(f'page login faild : {e}')

        # input email
        self.input_email = self.driver.find_element(
            By.XPATH, '//*[@id="username"]').send_keys(self.login_info["user_id"])

        # input password
        self.input_email = self.driver.find_element(
            By.XPATH, '//*[@id="password"]').send_keys(self.login_info["password"])

        # click login button
        self.login_btn = self.driver.find_element(
            By.XPATH, '//*[@id="kc-login"]').click()

        # 로그인 완료되고 다시 로그인 페이지로 잠시 이동 후 home 화면으로 이동한다.
        # 이때 home 화면으로 갈때까지 대기
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be("https://vendorcenter.jumia.com/home"))
        sleep(5)


        # login success and click product
        try:
            # span tab text button click
            self.driver.get('https://vendorcenter.jumia.com/products/add/new')
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
                (By.XPATH,
                 '/html/body/jumia-vnp-root/vnp-theme/div/mat-sidenav-container/mat-sidenav-content/product-add-products/nav/div[1]/div[2]/mat-icon/span'))).click()
        except Exception as e:
            print(f'page click product faild : {e}')


        # self.click_add_product = self.driver.find_element(
        #    By.XPATH, ('/html/body/jumia-vnp-root/vnp-theme/div/mat-sidenav-container/mat-sidenav-content/product-add-products/nav/div[1]/div[1]/p')).click()

        sleep(3)
    def postRequest(self):
        self.driver.request()
def main():
    jumia_login_info = {
        'shop_name': 'jumia',
        'action': 'FeedList',
        'user_id': 'twelfth2023@gmail.com',
        'password': 'Wnaldk124!@',
        'api_key': 'ad145288056c3fee92f158730e4e1a1cf7352fcf',
        'timezone': 'Africa/Lagos',
        'register_url': 'https://vendorcenter.jumia.com/sign-in'
    }
    jumia_bot = JumiaBot(jumia_login_info)
    jumia_bot.click_to_sell_login()
    # log.info('Let\'s start JUMIA')


# juliaBot = JumiaBot()

if __name__ == '__main__':
    main()
else:
    log = OneLogger()
