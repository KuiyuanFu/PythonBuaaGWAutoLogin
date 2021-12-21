import logging
import sys
import time
import os
import argparse
from typing import List
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def printInfo():
    print('The argument is wrong!')
    print('buaagw login USERNAME PASSWORD')
    print('buaagw logout')
    print('buaagw status')


class BuaaGw:
    url = "https://gw.buaa.edu.cn/srun_portal_pc?ac_id=1&theme=buaa"

    def __init__(self, ):
        pass

    def parse(self, argv: List[str]):
        parser = argparse.ArgumentParser(
            description='BUAA gateway.',
            prog="buaagw",
        )
        # parser.add_argument(
        #     '-t',
        #     dest='t',
        #     metavar='t',
        #     type=float,
        #     default=0.0,
        #     help='t',
        # )
        subparsers = parser.add_subparsers(help='functions')

        parserLogin = subparsers.add_parser('login', help='login')
        parserLogin.set_defaults(func=self.login)
        parserLogin.add_argument(
            'username',
            metavar='username',
            type=str,
            help='buaa gw username.',
        )
        parserLogin.add_argument(
            'password',
            metavar='password',
            type=str,
            help='buaa gw password.',
        )

        parserLogin.add_argument(
            '-r',
            dest='interval',
            metavar='interval',
            type=float,
            default=0.0,
            help='The interval of testing the network connection. ' +
            'Default is 0, not test and retry.',
        )

        parserLogout = subparsers.add_parser('logout', help='logout')
        parserLogout.set_defaults(func=self.logout)
        parserStatus = subparsers.add_parser('status', help='status')
        parserStatus.set_defaults(func=self.status)

        self.args = parser.parse_args(argv)

    def run(self, argv: List[str]):
        if len(argv) == 0:
            argv.append('-h')
        self.parse(argv)

        self.args.func(self.args)

    def initDriver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("log-level=3")
        self.driver = webdriver.Chrome(
            executable_path="chromedriver",
            options=options,
            keep_alive=False,
        )

    def logout(self, argv=None):
        self.initDriver()
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
        self.quit()

    def _login(self):
        self.initDriver()
        flag = True
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

            self.driver.find_element_by_id("username").send_keys(
                self.args.username)
            self.driver.find_element_by_id("password").send_keys(
                self.args.password)
            self.driver.find_element_by_id("login").click()
        except:
            print('Already logged in!')
            flag = False
        if flag:
            try:
                print('Logining!')
                WebDriverWait(self.driver, 1).until(
                    lambda driver: driver.find_element_by_css_selector(
                        "#user_name").is_displayed())
            except:
                print('The password is wrong!')
                flag = False
        self.quit()
        self.status()

        return flag

    def login(self, argv=None):
        self._login()
        if self.args.interval != 0.0:
            interval = self.args.interval
            while True:
                time.sleep(interval)
                if not self._test():
                    self._login()

    def _test(self) -> bool:
        s = subprocess.Popen(
            'ping  -n 1 -w 200  www.baidu.com ',
            shell=True,
            stdout=subprocess.PIPE,
        )

        return s.wait() == 0
        pass

    def status(self, argv=None):
        self.initDriver()
        flag = True
        try:
            self.driver.get(self.url)
            WebDriverWait(
                self.driver,
                1).until(lambda driver: driver.find_element_by_css_selector(
                    "#user_name").is_displayed())

            userName = self.driver.find_element_by_css_selector(
                "#user_name").text
            ip = self.driver.find_element_by_css_selector("#ip").text

            print('user_name:{}\tip:{}\t'.format(userName, ip))
        except:
            print('Not logged in!')

            flag = False
        finally:
            self.quit()
        return flag

    def quit(self):
        self.driver.quit()
        return True


if __name__ == '__main__':
    BuaaGw().run(sys.argv[1:])
