"""Register a new user with valid data on a public practice store.

Install Selenium first if needed:
    pip install selenium
"""

from time import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# A timestamp makes the email address unique, so the test can be run repeatedly.
full_name = "Jane Doe"
first_name, last_name = full_name.split(" ", maxsplit=1)
email = f"jane.doe.{int(time())}@example.com"
password = "SecurePass123!"

try:
    # Magento's public demo store provides a functioning registration page.
    driver.get("https://magento.softwaretestingboard.com/customer/account/create/")

    wait.until(EC.visibility_of_element_located((By.ID, "firstname"))).send_keys(
        first_name
    )
    driver.find_element(By.ID, "lastname").send_keys(last_name)
    driver.find_element(By.ID, "email_address").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password-confirmation").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.action.submit.primary").click()

    success_message = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.message-success"))
    ).text.strip()
    expected_message = "Thank you for registering with Main Website Store."

    assert success_message == expected_message, (
        f"Expected {expected_message!r}, but found {success_message!r}."
    )
    print(f"Registration verification passed for {full_name} ({email}).")
finally:
    print("Browser will remain open. Close it manually when you are finished.")
