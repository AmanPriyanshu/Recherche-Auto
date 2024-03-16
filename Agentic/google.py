from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import numpy as np

def scrape_and_save_text(search_query, top_n, path="C:\\Users\\amanp\\AppData\\Local\\Google\\Chrome\\User Data", directory="saved_pages", binary_location="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"):
    directory = "saved_pages"
    if not os.path.exists(directory):
        os.makedirs(directory)
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-data-dir={path}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.binary_location = binary_location
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    time.sleep(np.random.randint(3, 5))
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    driver.implicitly_wait(2)
    search_box.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    search_results = driver.find_elements(By.CSS_SELECTOR, ".tF2Cxc")
    print(search_results)
    print()
    for idx, result in enumerate(search_results):
        title = result.find_elements(By.CSS_SELECTOR, ".DKV0Md")[0].text
        link_url = result.find_elements(By.CSS_SELECTOR, ".yuRUbf a")[0].get_attribute("href")
        print(f"Title: {title}, Link: {link_url}")
        time.sleep(5)
        driver.execute_script("window.open(arguments[0]);", link_url)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)
        page_source = driver.page_source
        filename = f"page_{idx}.txt"
        filepath = os.path.join(directory, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(page_source)
        print(f"Page source saved to {filename}")
        try:
            driver.close()
        except:
            pass
        driver.switch_to.window(driver.window_handles[0])
        if idx>top_n-1:
            break
    driver.quit()

if __name__ == '__main__':
    scrape_and_save_text("Differential Privacy", 4)