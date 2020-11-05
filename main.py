from selenium.webdriver.support import expected_conditions as EC

import configparser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Initiate the browser
browser = webdriver.Chrome("C:/Users/natou/Documents/Supreme/chromedriver.exe")

config = configparser.ConfigParser()
config.read('config.txt')

# Open the Website
browser.get('https://www.supremenewyork.com/shop/all/' + config['ITEM']['category'])


def isItemHere() -> bool:
    try:
        browser.find_element_by_link_text(config['ITEM']['name'])
        return True
    except NoSuchElementException:
        browser.refresh()


# add item to cart
def addItem():
    articles = browser.find_elements_by_class_name("inner-article")
    for x in articles:
        try:
            x.find_element_by_link_text(config['ITEM']['name'])
            color = x.find_element_by_link_text(config['ITEM']['color'])
            color.click()
        except NoSuchElementException:
            print("Searching for element")


# Checkout
def checkout():
    try:
        element_present = EC.presence_of_element_located((By.ID, 'fr products show eu'))
        WebDriverWait(browser, 0.5).until(element_present)
        browser.find_element_by_xpath("//select[@name='size']/option[text()='" + config['ITEM']['size'] + "']").click()
    except TimeoutException:
        print("Timed out waiting for page to load")

    try:
        browser.find_element_by_name("commit").click()
        checkoutButton = EC.presence_of_element_located((By.NAME, 'voir le panier'))
        WebDriverWait(browser, 0.5).until(checkoutButton)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        buttons = browser.find_elements_by_xpath("//div/div/div/a")
        for button in buttons:
            if button.text == "commander":
                button.click()


# Payment
def payment():
    try:
        paymentButton = EC.presence_of_element_located((By.NAME, 'voir le panier'))
        WebDriverWait(browser, 0.5).until(paymentButton)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        # User info
        browser.find_element_by_id("order_billing_name").send_keys(config['USERINFO']['name'])
        browser.find_element_by_id("order_email").send_keys(config['USERINFO']['email'])
        browser.find_element_by_id("order_tel").send_keys(config['USERINFO']['phone'])
        browser.find_element_by_id("bo").send_keys(config['USERINFO']['adress'])
        browser.find_element_by_id("order_billing_city").send_keys(config['USERINFO']['city'])
        browser.find_element_by_id("order_billing_zip").send_keys(config['USERINFO']['zip'])
        browser.find_element_by_id("order_billing_country").send_keys(config['USERINFO']['country'])

        # Card info
        browser.find_element_by_id("credit_card_type").send_keys(config['BILLING']['card_type'])
        browser.find_element_by_id("cnb").send_keys(config['BILLING']['number'])
        browser.find_element_by_id("credit_card_month").send_keys(config['BILLING']['month'])
        browser.find_element_by_id("credit_card_year").send_keys(config['BILLING']['year'])
        browser.find_element_by_id("vval").send_keys(config['BILLING']['cvv'])

        # checkbox
        browser.find_element_by_xpath("//div/div/form/div/div/fieldset/p").click()

        # finish
        browser.find_element_by_xpath("//div/div/form/div/div/input").click()


while not isItemHere():
    print("refreshing...")

addItem()
checkout()
payment()
