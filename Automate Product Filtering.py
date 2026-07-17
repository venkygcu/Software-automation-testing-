from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# example.com/products is a placeholder and has no filter controls. This local
# page contains the exact IDs/classes used by the test so it is runnable.
PRODUCT_PAGE = Path(__file__).with_name("product_filter_demo.html").resolve().as_uri()

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Remove to watch the browser run.
options.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    driver.get(PRODUCT_PAGE)

    driver.find_element(By.ID, "category-electronics").click()

    min_price = driver.find_element(By.ID, "price-min")
    min_price.clear()
    min_price.send_keys("100")

    max_price = driver.find_element(By.ID, "price-max")
    max_price.clear()
    max_price.send_keys("500")

    driver.find_element(By.ID, "applyFilters").click()

    wait.until(
        lambda browser: browser.find_elements(
            By.CSS_SELECTOR, ".product-item:not([hidden])"
        )
    )
    products = driver.find_elements(By.CSS_SELECTOR, ".product-item:not([hidden])")

    assert products, "No products matched the filters."
    for product in products:
        assert product.get_attribute("data-category") == "electronics"
        price_text = product.get_attribute("data-price")
        assert price_text is not None, "A displayed product is missing data-price."
        assert 100 <= float(price_text) <= 500

    print(f"Test passed: {len(products)} matching Electronics product(s) found.")
finally:
    driver.quit()
