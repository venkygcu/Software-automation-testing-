from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# example.com/products is a placeholder. The local demo supplies these controls.
PRODUCT_PAGE = Path(__file__).with_name("cart_demo.html").resolve().as_uri()

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Remove this line to watch the test.
options.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    driver.get(PRODUCT_PAGE)

    # Add Product 1 ($200) and Product 2 ($400).
    driver.find_element(By.ID, "addProduct1").click()
    driver.find_element(By.ID, "addProduct2").click()

    # Navigate to the cart and wait for it to become visible.
    driver.find_element(By.ID, "cartLink").click()
    wait.until(lambda browser: browser.find_element(By.ID, "cart").is_displayed())

    total = driver.find_element(By.CSS_SELECTOR, ".cart-total").text
    assert total == "Total: $600", f"Expected Total: $600, got {total!r}."
    print("Cart total verification passed!")

    qty1 = driver.find_element(By.ID, "product1-quantity").get_attribute("value")
    qty2 = driver.find_element(By.ID, "product2-quantity").get_attribute("value")
    assert qty1 == "1" and qty2 == "1", (
        f"Expected both quantities to be 1, got Product 1={qty1}, Product 2={qty2}."
    )
    print("Product quantity verification passed!")
finally:
    driver.quit()
