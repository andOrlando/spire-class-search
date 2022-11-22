#! /usr/bin/env nix-shell
#! nix-shell -i python3
import time
from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from twilio.rest import Client

config = dotenv_values(".env")

driver = webdriver.Firefox()
driver.get("https://www.spire.umass.edu")
driver.implicitly_wait(10)
driver.maximize_window()
wait = WebDriverWait(driver,10)


# log in
driver.find_element(By.ID, "userid").send_keys(config["USERNAME"])
driver.find_element(By.ID, "pwd").send_keys(config["PASSWORD"])
driver.find_element(By.CSS_SELECTOR, "input.btn").click()

# get to search window
driver.find_element(By.XPATH, "//h1[text()='Manage Classes']").click()
driver.find_element(By.XPATH, "//span[text()='Add, Drop & Edit Classes']").click()

# wait until clickable then go to browse
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "body:not([style])")))
driver.find_element(By.XPATH, "//span[text()='Browse Course Catalog']").click()

# open popup
driver.find_element(By.XPATH, "//a[text()='Additional ways to search']").click()

# switch to iframe, input stuff and search
driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
Select(driver.find_element(By.CSS_SELECTOR, "select.ps-dropdown")).select_by_visible_text(config["MAJOR"])
driver.find_element(By.CSS_SELECTOR, "input.ps-edit").send_keys(config["NUMBER"])
driver.find_element(By.ID, "SSR_CLSRCH_FLDS_SSR_SEARCH_PB_1\\$0").click()

# switch back and click first option
driver.switch_to.default_content()
wait.until(expected_conditions.presence_of_element_located((By.ID, "win8div\\$ICField65")))
driver.find_element(By.CSS_SELECTOR, "li[id^='PTS_RSLTS_LIST']").click()

# this is really shady but click view classes
wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//a[text()='View Classes']")))
time.sleep(2)
driver.find_element(By.XPATH, "//a[text()='View Classes']").click()

# still shady but click the semester button
wait.until(expected_conditions.presence_of_element_located((By.XPATH, f"//a[text()='{config['SEMESTER']}']")))
time.sleep(2)
driver.find_element(By.XPATH, f"//a[text()='{config['SEMESTER']}']").click()

# wait until clickable and then a little more
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "body:not([style])")))
time.sleep(2)

# get result as an array of possibly "closed"s but hopefully not
res = sum(map(lambda elem: [*map(lambda span: span.text, elem.find_elements(By.CSS_SELECTOR, "span"))], driver.find_elements(By.CSS_SELECTOR, "tr.psc_rowact > td:nth-child(9)")), [])

# check if there's anything that's not "Closed"
if (len([*filter(lambda a: a != "Closed", res)]) > 0):
    # send myself a message
    client = Client(config["TWILIO_SID"], config["TWILIO_AUTH"])
    client.messages.create(to=config["YOUR_NUM"], from_=config["TWILIO_NUM"], body=f"FOUND OPENING FOR {config['MAJOR']} {config['NUMBER']}")

driver.quit()

