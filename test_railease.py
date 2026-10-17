import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Target RailEase Portal URL
BASE_URL = "https://railease-india-eyq2.vercel.app"

# Directory to save test run screenshots
SCREENSHOT_DIR = Path(__file__).resolve().parent.joinpath("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

def get_driver(browser_name):
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        return webdriver.Chrome(options=options)
    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("-headless")
        return webdriver.Firefox(options=options)
    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        options.add_argument("--headless=new")
        return webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

def test_booking_portal(browser_name):
    print("==========================================")
    print(f" Running Tests on: {browser_name.upper()}")
    print("==========================================")

    driver = get_driver(browser_name)
    driver.set_window_size(1440, 900)
    driver.get(BASE_URL)
    time.sleep(3)

    try:
        # Test 1: Page Title Verification
        assert "RailEase" in driver.title, f"Title mismatch! Got: {driver.title}"
        print(f"[PASS] Test 1: Page Title verified ('{driver.title}')")

        # Test 2: Validation Check on Destination Station Picker
        to_box = driver.find_element(By.XPATH, "//span[text()='To']/..//div[contains(@class, 'cursor-pointer')]")
        driver.execute_script("arguments[0].click();", to_box)
        time.sleep(1)

        station_input = driver.find_element(By.XPATH, "//input[@placeholder='Search city or station...']")
        station_input.clear()
        station_input.send_keys("XYZInvalidStation")
        time.sleep(0.5)

        invalid_options = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer') and .//span[contains(text(), 'XYZInvalidStation')]]")
        assert len(invalid_options) == 0, "Validation failed: Invalid station options found!"
        print("[PASS] Test 2: Form validation verified (No station matches for invalid destination)")

        # Test 3: Select Valid Destination and Search Trains
        station_input.clear()
        station_input.send_keys("Pune")
        time.sleep(1)

        pune_option = driver.find_element(By.XPATH, "//*[contains(text(), 'Pune')]")
        driver.execute_script("arguments[0].click();", pune_option)
        time.sleep(1)

        search_btn = driver.find_element(By.XPATH, "//button[contains(., 'Search Trains')]")
        driver.execute_script("arguments[0].click();", search_btn)
        time.sleep(3)

        train_cards = driver.find_elements(By.XPATH, "//h3")
        assert len(train_cards) > 0, "No train search results found!"
        print(f"[PASS] Test 3: Search results verified ({len(train_cards)} trains listed)")

        # Capture and Save Screenshot
        screenshot_file = SCREENSHOT_DIR / f"{browser_name.lower()}_result.png"
        driver.save_screenshot(str(screenshot_file))
        print(f"[SAVED] Screenshot captured: {screenshot_file.name}\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    browsers = ["chrome", "firefox", "edge"]
    for b in browsers:
        test_booking_portal(b)
