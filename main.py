from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import requests
import sys
import pathlib

path = sys.argv[1]
url = sys.argv[2]
print(url)
print("Loading...")
#URL = "https://docs.yandex.ru/docs/view?url=ya-disk-public%3A%2F%2F51lAr%2BMDAn9Ekpi5y1rsjwmx2CUVdVbXre4Db3G2Kqf7LJTfhj%2Bf9amh0OPNnJCgq%2FJ6bpmRyOJonT3VoXnDag%3D%3D&name=%D0%A1.%D0%9E.%20%D0%A0%D0%B0%D1%87%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%9F%D0%BE%D1%81%D0%BE%D0%B1%D0%B8%D0%B5%20%D0%BF%D0%BE%20%D1%81%D0%BE%D0%BB%D1%8C%D1%84%D0%B5%D0%B4%D0%B6%D0%B8%D0%BE%201-4%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B.pdf&nosw=1"
op = webdriver.ChromeOptions()

op.add_argument("headless")

driver = webdriver.Chrome(executable_path='../chromedriver.exe', options=op)
driver.get(url)

pages_container_class = "pages_M4f5cH028VlVHUDpNlQcm"
print("Searching for the frame...")
frame = driver.find_element(By.TAG_NAME, "iframe")
print("Got frame. Redirecting...")
driver.get(frame.get_attribute("src"))
time.sleep(1)
el = driver.find_element(By.CLASS_NAME, pages_container_class)
els = el.find_elements(By.CSS_SELECTOR, "*")
print("Searching for pages...")
pages = []
for e in els:
    try:
        cname = e.get_attribute("class")
    except StaleElementReferenceException:
        continue
    if cname.startswith("js-doc-page"):
        pages.append(e)
print(f"Found {len(pages)} pages. Downloading...")
time.sleep(2)
page = driver.find_element(By.CLASS_NAME, "__page-1")
pattern = page.find_element(By.TAG_NAME, "img").get_attribute("src")
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer': 'https://www.google.com/'
}

pages_total = len(pages)
for i in range(len(pages)):
    print(f"Progress: {i+1}/{pages_total} ({int((i+1) / pages_total * 100)}%)")
    time.sleep(2)
    url = pattern.replace("name=bg-0.png", f"name=bg-{i}.png")
    response = requests.get(url, headers=header)
    with open(pathlib.Path(path, f"{i}.png"), "wb") as f:
        f.write(response.content)
