from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Sauce Demo is a public practice site with a working login-error flow.
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.saucedemo.com/")

    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(
        "wrongUser"
    )
    driver.find_element(By.ID, "password").send_keys("wrongPass")
    driver.find_element(By.ID, "login-button").click()

    error_message = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    ).text.strip()

    expected_message = (
        "Epic sadface: Username and password do not match any user in this service"
    )
    assert error_message == expected_message, (
        f"Expected {expected_message!r}, "
        f"but found {error_message!r}."
    )
    print("Invalid login error-message verification passed.")
finally:
    print("Browser will remain open. Close it manually when you are finished.")
