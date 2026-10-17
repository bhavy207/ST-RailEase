from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

opt = Options()
opt.add_argument('--headless=new')
driver = webdriver.Chrome(options=opt)
driver.set_window_size(1440, 900)

driver.get('https://railease-india-eyq2.vercel.app/results?from=st-nsk&to=')
time.sleep(3)

print("Title:", driver.title)
print("Page text snippet:")
lines = [l for l in driver.find_element(By.TAG_NAME, 'body').text.splitlines() if l.strip()]
for l in lines[:15]:
    try:
        print("Line:", l)
    except:
        pass

driver.quit()
