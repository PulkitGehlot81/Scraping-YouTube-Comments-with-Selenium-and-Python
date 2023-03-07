from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv

driver = webdriver.Chrome(r"C:/Users/hp/Anaconda3/chromedriver.exe")
driver.get('https://www.youtube.com/watch?v=x9I-c-pediY')

# Scroll down to load comments
driver.execute_script('window.scrollTo(1, 500);')
try:
    # Wait for comments to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content-text"]')))
except TimeoutException:
    print("Timed out waiting for comments to load")
driver.execute_script('window.scrollTo(1, 3000);')

# Extract comments
username_elems = driver.find_elements("xpath",'//*[@id="author-text"]')
comment_elems = driver.find_elements("xpath",'//*[@id="content-text"]')
items = [{'Author': username.text, 'Comment': comment.text} for username, comment in zip(username_elems, comment_elems)]

# Save to CSV
filename = './commentlist.csv'
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Author', 'Comment'])
    writer.writeheader()
    writer.writerows(items)

driver.quit()
