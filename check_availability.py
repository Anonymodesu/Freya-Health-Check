from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
import winsound


# sometimes an alert pops up when you click on a location
def handle_alert(wait_driver):
    try:
        alert = wait_driver.until(expected_conditions.alert_is_present())
        print("Accepting alert:", alert.text)
        alert.accept()
    except TimeoutException as e:
        pass


def check_availability(postcode, location_index, wait_timeout=3):
    # setup
    options = webdriver.ChromeOptions()
    # https://stackoverflow.com/questions/69441767/error-using-selenium-chrome-webdriver-with-python
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(wait_timeout)
    wait_driver = WebDriverWait(driver, wait_timeout)

    # initial page
    driver.get("https://bmvs.onlineappointmentscheduling.net.au/oasis/Default.aspx")
    new_booking_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnInd")
    new_booking_button.click()

    # look for a location
    suburb_field = driver.find_element(By.ID, "ContentPlaceHolder1_SelectLocation1_txtSuburb")
    suburb_field.send_keys(postcode)
    suburb_search_button = driver.find_element(By.CLASS_NAME, "blue-button")
    suburb_search_button.click()
    location_descriptions = driver.find_elements(By.CLASS_NAME, "tdloc_name")
    location_description = location_descriptions[location_index].text
    location_radio_buttons = driver.find_elements(By.NAME, "rbLocation")
    location_radio_buttons[location_index].click()
    handle_alert(wait_driver)
    location_next_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnCont")
    location_next_button.click()

    # Select medical assessments
    assessment_buttons = driver.find_elements(By.NAME, "TestProduct1")
    assessment_buttons[0].click()
    assessment_buttons[1].click()
    assessment_next_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnCont")
    assessment_next_button.click()

    # check if times are available
    available_times = driver.find_elements(By.ID, "ContentPlaceHolder1_SelectTime1_divSearchResults")
    if available_times:
        available_time = available_times[0].find_element(By.TAG_NAME, "h2").text
        print(f"Available time {available_time} at:\n{location_description}")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    else:
        print(f"No available times for:\n{location_description}")

# check availability for the 4 closest locations
for i in range(0, 4):
    check_availability("2037", i)
