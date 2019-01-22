import time

import lxml.html
import openpyxl
import requests
import array
from openpyxl import workbook
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


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

        self.driver.implicitly_wait(10)

        self.driver.get("https://reform.helsi.me/")

        # main page

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
        for i in range(60):
            cp_page(self.driver)
            try:
                self.driver.find_element_by_link_text("chevron_left").click()
            except WebDriverException:
                print("Element is not clickable")


#################################################################
def update_names(driver):
    names = driver.find_elements_by_xpath(".//div[@class='declaration-td name']")

    names.reverse()
    names = names[:len(names) - 1]
    names = [i for i in names]

    return names


def cp_page(driver):


    dates = driver.find_elements_by_xpath(".//div[@class='declaration-td birthday-date']")
    dates.reverse()
    dates = [i.text for i in dates]
    dates = dates[:len(dates)]

    for i in range(20):
        names = update_names(driver)

        person = [""] * 6
        person[0] = i
        person[1] = names[i].text

        person[2] = dates[i]

        names[i].click()

        #Yep, it`s stupid, but otherwise the db of MoH is breaking down
        time.sleep(5)

        person[3] = driver.find_elements_by_xpath(".//input[@id='person.gender']")[0].get_attribute("value")
        person[4] = driver.find_element_by_id("person.phones.0.number").get_attribute("value")
        person[5] = driver.find_element_by_id("person.addresses.0.street").get_attribute("value") + ' ' \
                    + driver.find_element_by_id("person.addresses.0.building").get_attribute("value") + '-' \
                    + driver.find_element_by_id("person.addresses.0.apartment").get_attribute("value")

        print(*person)
        driver.back()
    print("#######################")


# def find_bday(driver):
#     dates = driver.find_elements_by_xpath(".//div[@class='declaration-td birthday-date']")
#
#     dates.reverse()
#     dates = [i.text for i in dates]
#     dates = dates[:len(dates)]
#
#     return dates


def excel_operations():
    wb = workbook.Workbook()
    ws = wb.active


def cp_single_person(driver):
    pass


if __name__ == "__main__":
    parser = HelsiParser(webdriver.Chrome())

    parser.to_declarations()
    parser.parse()

# excel_operations()
