import time
import excel
from datetime import datetime
import utils as u
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from config import settings

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)


def open_website():
    driver.get("https://www.elephantbet.co.mz/")
    driver.maximize_window()


def close_popup():
    div_present = EC.presence_of_element_located((By.ID, "onesignal-slidedown-container"))
    element = wait.until(div_present)
    if element.is_displayed():
        close_button = driver.find_element(By.ID, "onesignal-slidedown-cancel-button")
        close_button.click()


def input_email():
    input_field = EC.presence_of_element_located((By.ID, "username-login-form-oneline"))
    element = wait.until(input_field)
    if element.is_displayed():
        email_input = driver.find_element(By.ID, 'username-login-form-oneline')
        email_input.send_keys(settings.user_name)


def input_password():
    password_input = driver.find_element(By.CLASS_NAME, "bto-form-control-password")
    password_input.send_keys(settings.password)


def click_login():
    login_button = driver.find_element(By.ID, "login-form-oneline")
    login_button.click()


def login():
    print("logging in ...")
    input_email()
    input_password()
    click_login()
    time.sleep(5)


def enter_aviator():
    aviator_button = driver.find_element(By.ID, "menu-item-4159").find_element(By.TAG_NAME,"a")
    aviator_button.click()
    time.sleep(5)


def switch_to_aviator_frame():
    driver.switch_to.frame(driver.find_element(By.ID, "game_loader"))
    driver.switch_to.frame(driver.find_element(By.ID, "spribe-game"))


def open_first_bubble():
    try:
        first_bubble = driver.find_element(By.CSS_SELECTOR, "app-bubble-multiplier:nth-child(1) > div")
        first_bubble.click()
    except:
        pass
        # print("Error: Could not open bubble")


def get_rodada() -> int:
    time.sleep(0.1)
    rodada_element = driver.find_element(By.XPATH,'//span[contains(text(), "Rodada")]')
    rodada_text = rodada_element.text.split()[1]
    output = int(rodada_text)
    return output


def get_time():
    try:
        time_element = driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/app-fairness/div[1]/div/div[2]')
        time_text = time_element.text
        output =  u.combine_date_time(time_text)
        return output
    except: 
        pass
        # print("Error: Could not get rodada time.")


def get_multiplier():
    try:
        multiplier_element = driver.find_element(By.XPATH,'//div[contains(text(), "x")]')
        multiplier_text = multiplier_element.text.strip("x")
        output = float(multiplier_text)
        return output
    except: 
        pass
        # print("Error: Could not get multiplier")


def close_header():
    try:
        close_button = driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/app-fairness/div[1]/button/span')
        close_button.click()
    except:
        pass
        # print("Error: Could not close header")


def open_history():
    div_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.button-block > div"))
    element = wait.until(div_present)
    if element.is_displayed():
        close_button = driver.find_element(By.CSS_SELECTOR, "div.button-block > div")
        close_button.click()


def get_history() ->list[float]:
    try:
        open_history()
        payout_elements = driver.find_elements(By.CSS_SELECTOR, "app-stats-dropdown > div > div.payouts-block > div")
        payouts = []
        for element in payout_elements:
            try:payouts.append(float(element.text.strip("x")))
            except: pass
        return payouts

    except: pass


def logout():
    print('logging out ...')
    driver.switch_to.default_content()

    # Scroll to the element
    button = driver.find_element(By.CSS_SELECTOR, "button.btosystem-logout")
    driver.execute_script("arguments[0].scrollIntoView();", button)

    # Click the button using JavaScript
    driver.execute_script("arguments[0].click();", button)


class RollData():
    def __init__(
        self,
        current_roll = 0,
        excel_file_name = "multipliers.xlsx",
        failed_attempts = 0,
        max_failed_attempts = 3000
    ):
        self.current_roll = current_roll
        self.excel_file_name = excel_file_name
        self.failed_attempts = failed_attempts
        self.max_failed_attempts = max_failed_attempts

    def get(self):
        while True:
            open_first_bubble()
            rodada = 0

            try: rodada = get_rodada()
            except:
                self.failed_attempts +=1
                if self.failed_attempts > self.max_failed_attempts: break

            if self.current_roll != rodada and rodada:
                # rodada_datetime = get_time()
                rodada_datetime = datetime.now()
                multiplier = get_multiplier()
                close_header()
                payout_history = get_history()
                open_history()
                excel.add_row_to_excel(self.excel_file_name,rodada, rodada_datetime, multiplier, payout_history, self.failed_attempts)
                self.current_roll = rodada
                self.failed_attempts = 0

            close_header()




