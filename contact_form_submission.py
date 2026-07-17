from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # Selenium's public demonstration form is a live, working form page.
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    wait.until(EC.visibility_of_element_located((By.NAME, "my-text"))).send_keys(
        "John Doe"
    )
    driver.find_element(By.NAME, "my-password").send_keys("john@example.com")
    driver.find_element(By.NAME, "my-textarea").send_keys("Test message")
    driver.find_element(By.CSS_SELECTOR, "button").click()

    success_message = wait.until(
        EC.visibility_of_element_located((By.ID, "message"))
    ).text
    assert success_message == "Received!", (
        f"Expected 'Received!', found {success_message!r}."
    )
    print("Contact form submission verification passed.")
finally:
    print("Browser will remain open. Close it manually when you are finished.")
