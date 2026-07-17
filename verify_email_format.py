from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


PRODUCT_PAGE = Path(__file__).with_name("product_filter_demo.html").resolve().as_uri()


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Remove this line to watch the test run.
options.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    driver.get(PRODUCT_PAGE)

    # Select Electronics and filter products costing between 100 and 500.
    driver.find_element(By.ID, "category-electronics").click()

    min_price = driver.find_element(By.ID, "price-min")
    min_price.clear()
    min_price.send_keys("100")

    max_price = driver.find_element(By.ID, "price-max")
    max_price.clear()
    max_price.send_keys("500")

    driver.find_element(By.ID, "applyFilters").click()

    wait.until(
        lambda browser: len(
            browser.find_elements(By.CSS_SELECTOR, ".product-item:not([hidden])")
        )
        > 0
    )
    products = driver.find_elements(By.CSS_SELECTOR, ".product-item:not([hidden])")

    assert products, "No products matched the selected category and price range."
    for product in products:
        assert product.get_attribute("data-category") == "electronics"
        price_value = product.get_attribute("data-price")
        assert price_value is not None, "A displayed product is missing its price."
        price = float(price_value)
        assert 100 <= price <= 500

    print(f"Product-filter test passed: {len(products)} Electronics product(s) found.")
finally:
    driver.quit()
