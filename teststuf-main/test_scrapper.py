from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup

mode = 'extract'



path_to_file = r'C:\Users\tanwe\Desktop\scrapper\\'
if mode == 'scrape':
    s = Service('C:/Users/tanwe/Desktop/scrapper/teststuf-main/tmp/chromedriver/chromedriver.exe') ###Directory of your chromedriver.exe
    driver = webdriver.Chrome(service = s)
    driver.get('https://en.cf-vanguard.com/cardlist/cardsearch/?regulation=D&nation=&clan=&keyword=&keyword_type%5B%5D=all&kind%5B%5D=all&grade%5B%5D=all&power_from=&power_to=&rare=&trigger%5B%5D=all')
    time.sleep(3)
    driver.find_element(By.XPATH,"//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']").click() #click to pass cookie wall
    time.sleep(3)
    previous_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        previous_height = new_height

    page_source = driver.page_source

    f = open(path_to_file + "source.txt", "w", encoding= "utf-8")
    f.write(page_source)
    f.close()

### Bs4 test
if mode != 'scrape':
    data = []

    f = open(path_to_file + "source.txt", "r", encoding= "utf-8")
    page_source = f.read()
    f.close()
    soup = BeautifulSoup(page_source, features='lxml')

    items = soup.findAll('div', class_ = 'cardlist_gallerylist')

    for item in items:
        item_out = {}

        print(type(items))
        exit()
    