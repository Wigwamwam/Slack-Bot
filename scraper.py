import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


c = webdriver.ChromeOptions()
c.add_argument("--incognito")

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=c)
driver.implicitly_wait(0.5)

driver.get("https://uk.indeed.com/jobs?q=junior%20backend%20developer&l=London&start=10")
results = []
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
for element in soup.findAll(attrs={'class': 'job_seen_beacon'}):
    title = element.find(attrs={'class': 'jobTitle'})
    results.append(title.text)

driver.quit() # closing the browser


# blog_titles = driver.find_elements(By.CLASS_NAME, "jcs-JobTitle")
# for title in blog_titles:
#     print(title.text)
# driver.quit() # closing the browser
