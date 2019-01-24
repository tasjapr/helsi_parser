import time

import lxml.html
import openpyxl
import requests
from openpyxl import workbook
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class HelsiParser:

    def __init__(self, driver):
        self.driver = driver

    def get_page(self):
        try:
            res = requests.get(self.base_url)
        except requests.ConnectionError:
            return

        if res.status_code < 400:
            return res.content

    def to_declarations(self):

        self.driver.implicitly_wait(10)

        # main page
        self.driver.get("https://reform.helsi.me/")
        self.driver.find_element_by_xpath(".//a[@href='#login-modal']").click()
        self.driver.find_element_by_xpath(".//input[@id='user.email']").send_keys("rovenska10@bigmir.net",
                                                                                  Keys.ENTER)
        # auth page
        el = self.driver.find_element_by_name("password")
        el.send_keys("140290Rovenska1")
        el.submit()

        # continue page
        el = self.driver.find_element_by_xpath(".//button[@type='button']")
        el.click()

        # declaration page
        el = self.driver.find_element_by_xpath(".//a[@href='/declarations/my/signed']")
        el.click()

        # go to last page
        self.driver.find_element_by_xpath(".//a[@href='?page_number=60']").click()

    def parse(self):
        wb = workbook.Workbook()
        ws = wb.active
        for i in range(60):
            cp_page(self.driver, ws, wb)
            try:
                self.driver.find_element_by_link_text("chevron_left").click()
            except WebDriverException:
                print("Element is not clickable")


def update_names(driver):
    names = driver.find_elements_by_xpath(".//div[@class='declaration-td name']")

    names.reverse()
    names = names[:len(names) - 1]
    names = [i for i in names]

    return names


def cp_page(driver, ws, wb):
    dates = driver.find_elements_by_xpath(".//div[@class='declaration-td birthday-date']")
    dates.reverse()
    dates = [i.text for i in dates]
    dates = dates[:len(dates)]

    for i in range(20):
        names = update_names(driver)

        person = [""] * 5
        person[0] = names[i].text
        person[2] = dates[i]

        driver.find_element_by_partial_link_text(names[i].text).click()

        # Yep, it`s stupid, but otherwise the db of MoH is breaking down
        time.sleep(5)

        person[1] = driver.find_element_by_id("person.gender").get_attribute("value")
        person[3] = driver.find_element_by_id("person.phones.0.number").get_attribute("value")

        if driver.find_element_by_id("person.addresses.0.apartment").get_attribute("value") == ' ':
            person[4] = driver.find_element_by_id("person.addresses.0.street").get_attribute("value") + ' ' \
                        + driver.find_element_by_id("person.addresses.0.building").get_attribute("value")
        else:
            person[4] = driver.find_element_by_id("person.addresses.0.street").get_attribute("value") + ' ' \
                        + driver.find_element_by_id("person.addresses.0.building").get_attribute("value") + '-' \
                        + driver.find_element_by_id("person.addresses.0.apartment").get_attribute("value")


        ws.append(person)
        # enter your name for doc here
        wb.save('decl.xlsx')
        print(*person)

        driver.back()
    print("#######################")


if __name__ == "__main__":
    parser = HelsiParser(webdriver.Chrome())

    parser.to_declarations()
    parser.parse()
