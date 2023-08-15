from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
import pickle
import tabulate

browser = webdriver.Chrome(ChromeDriverManager().install())

loss_count = 0


def login():

    browser.refresh()

    time.sleep(30)

    browser.get("https://m.skybet.com/virtual-football")

    initial_balance = browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/header[1]/div[3]/span[1]/div[1]/a[1]/span[1]/span[1]").text

    print(initial_balance)

    return float(initial_balance)


def was_win():

    browser.get("https://m.skybet.com/virtual-football")

    time.sleep(4)

    browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/button[1]").click()

    time.sleep(2)

    result = browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[7]/div[1]/div[1]/div[2]/div[1]/div[1]").text

    if "Under" in result:
        return True
    else:
        return False


def place_bet(amount):

    browser.get("https://m.skybet.com/virtual-football")

    time.sleep(8)

    time.sleep(3)
    browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]").click()

    time.sleep(3)

    browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/div[3]/div[1]/span[1]/span[3]/i[1]").click()

    time.sleep(6)

    browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/aside[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(amount)

    time.sleep(3)

    browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/aside[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/button[1]").click()

    time.sleep(3)

    browser.refresh()


def get_balance():

    browser.refresh()

    current_balance = browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/header[1]/div[3]/span[1]/div[1]/a[1]/span[1]/span[1]").text

    return float(current_balance)


def is_ready():

    bet_time = browser.find_element(
        By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[1]/span[2]").text

    while bet_time != "0:40":
        bet_time = browser.find_element(
            By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[1]/span[2]").text

    return True


def get_losses(amount):
    loss_count = 0
    while is_ready() and loss_count != amount:
        if not was_win():
            loss_count = loss_count + 1
        else:
            loss_count = 0
    print("Got Losses")
    return True


def start_bot():

    browser.get("https://m.skybet.com/virtual-football")

    # cookies = pickle.load(open("cookies.pkl", "rb"))
    # for cookie in cookies:
    #     browser.add_cookie(cookie)

    time.sleep(15)

    intitial_balance = login()

    target_balance = intitial_balance + 10.00

    amount = 0.15
    loss_count = 0

    while is_ready() and loss_count <= 7:

        current_balance = get_balance()

        if not was_win():
            loss_count = loss_count + 1
            if target_balance < current_balance:
                print("Target Achieved")
                time.sleep(86400)

            print("Loss")
            amount = amount * 3.00
            place_bet(amount)
        else:
            loss_count = 0
            if target_balance < current_balance:
                time.sleep(86400)

            print("Win")
            amount = 0.15
            place_bet(amount)


start_bot()
