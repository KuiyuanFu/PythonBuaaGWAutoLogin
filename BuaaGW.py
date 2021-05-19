import logging
import sys
import time
import os

rootPath = os.path.dirname(sys.path[0])
os.chdir(rootPath)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class BuaaGw:
    url = "https://gw.buaa.edu.cn/srun_portal_pc?ac_id=1&theme=buaa"

    def __init__(self, ):

        self.initDriver()

    def initDriver(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="chromedriver",
                                       options=options)

    def logout(self):
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver,
                          1).until(lambda driver: driver.find_element_by_id(
                              "logout-dm").is_displayed())
            self.driver.find_element_by_id("logout-dm").click()
            print('Logout!')
        except:
            print('Not logged in!')
            return

    def login(self, username, password):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver,
                          1).until(lambda driver: driver.find_element_by_id(
                              "username").is_displayed())
            WebDriverWait(self.driver,
                          1).until(lambda driver: driver.find_element_by_id(
                              "password").is_displayed())
            WebDriverWait(self.driver,
                          1).until(lambda driver: driver.find_element_by_id(
                              "login").is_displayed())

            self.driver.find_element_by_id("username").send_keys(username)
            self.driver.find_element_by_id("password").send_keys(password)
            self.driver.find_element_by_id("login").click()

            print('Login!')
        except:
            print('Already logged in!')
            return False
        return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('buaagw login USERNAME PASSWORD')
        print('buaagw logout')
        sys.exit()
    gw = BuaaGw()
    if sys.argv[1] == 'login':
        if len(sys.argv) < 4:
            print('Insufficient parameters!')
            sys.exit()
        gw.login(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'logout':
        gw.logout()
