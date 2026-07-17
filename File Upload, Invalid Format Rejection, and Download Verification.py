from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


BASE_DIR = Path(__file__).parent
FILES_PAGE = BASE_DIR.joinpath("file_upload_demo.html").resolve().as_uri()
VALID_FILE = BASE_DIR / "test_files" / "valid.pdf"
INVALID_FILE = BASE_DIR / "test_files" / "invalid.exe"


with TemporaryDirectory() as download_directory:
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,800")
    options.add_experimental_option("detach", True)
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(FILES_PAGE)

        # Upload a valid PDF file.
        upload = driver.find_element(By.ID, "fileUpload")
        upload.send_keys(str(VALID_FILE))
        driver.find_element(By.ID, "uploadButton").click()
        wait.until(
            lambda browser: browser.find_element(By.CSS_SELECTOR, ".upload-success").text
            == "File uploaded successfully."
        )
        print("Valid file upload test passed!")

        # Upload an unsupported file format.
        upload.clear()
        upload.send_keys(str(INVALID_FILE))
        driver.find_element(By.ID, "uploadButton").click()
        wait.until(
            lambda browser: browser.find_element(By.CSS_SELECTOR, ".upload-error").text
            == "Unsupported file format."
        )
        print("Invalid file rejection test passed!")

        # Download a file and verify it exists and contains the expected text.
        driver.find_element(By.ID, "downloadButton").click()
        wait.until(
            lambda browser: browser.find_element(By.CSS_SELECTOR, ".download-success").text
            == "File downloaded successfully."
        )
        downloaded_file = Path(download_directory) / "downloaded-report.txt"
        for _ in range(50):
            if downloaded_file.exists():
                break
            sleep(0.1)
        assert downloaded_file.exists(), "The expected download was not created."
        assert downloaded_file.read_text(encoding="utf-8") == "Download verified.\n"
        print("File download verification passed!")
    finally:
        print("The browser will remain open. Close the Chrome window when you are finished.")
