import time
import requests
import lxml.html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class HelsiParser:

    def __init__(self, driver):
        self.driver = driver
        self.last_time = ''

    def get_page(self):
        try:
            res = requests.get(self.base_url)
        except requests.ConnectionError:
            return

        if res.status_code < 400:
            return res.content

    def to_declarations(self):

        driver = self.driver
        #driver = webdriver.Chrome()
        driver.implicitly_wait(10)

        driver.get("https://reform.helsi.me/")

        # main page
        driver.find_element_by_xpath(".//a[@href='#login-modal']").click()
        driver.find_element_by_xpath(".//input[@id='user.email']").send_keys("rovenska10@bigmir.net",
                                                                             Keys.ENTER)
        #auth page
        el = driver.find_element_by_name("password")
        el.send_keys("140290Rovenska1")
        el.submit()

        #continue page
        el = driver.find_element_by_xpath(".//button[@type='button']")
        el.click()

        #declaration page
        el = driver.find_element_by_xpath(".//a[@href='/declarations/my/signed']")
        el.click()

        #go to last page
        driver.find_element_by_xpath(".//a[@href='?page_number=60']").click()

        # TODO add checking
        if 1==1:
            next_page(driver)

def next_page(driver):
    driver.find_element_by_link_text("chevron_left").click()

def parse(self):
    pass


def run(self):
    pass


if __name__ == "__main__":
    parser = HelsiParser(webdriver.Chrome())

    parser.to_declarations()

