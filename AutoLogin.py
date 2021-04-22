import logging
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    datefmt='%Y-%m-%d %A %H:%M:%S',
    filename='AutoLogin.log',
    filemode='a')
logging.getLogger()


class AutoLogin:
    url = "https://gw.buaa.edu.cn/srun_portal_pc?ac_id=1&theme=buaa"

    def __init__(self, username, password, checkGap=60):
        self.username = username
        self.password = password
        self.checkGap = checkGap
        self.initDriver()

    def initDriver(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def clock(self):
        while True:
            flag = self.checkState()
            if not flag:
                self.login()
            time.sleep(self.checkGap)

    def checkState(self):
        try:
            time.sleep(0.5)
            self.driver.get(self.url)
            username = self.driver.find_element_by_id("user_name")
            logging.info('Already logged in !')
        except:
            logging.info('Not logged in !')
            return False
        return True

    def login(self):
        try:
            time.sleep(0.5)
            logging.info('Logging in !')
            self.driver.get(self.url)
            self.driver.find_element_by_id("username").send_keys(self.username)
            self.driver.find_element_by_id("password").send_keys(self.password)
            self.driver.find_element_by_id("login").click()
            logging.info('Logging end !')
        except:
            logging.error('Logging error !')
            return False
        return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error('Run paras is insufficient !')
        exit()
    if len(sys.argv) == 3:
        logging.critical('Run paras is 2 !')
        al = AutoLogin(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        logging.critical('Run paras is 3 !')
        al = AutoLogin(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    al.clock()
