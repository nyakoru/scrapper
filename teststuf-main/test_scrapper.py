from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup

mode = 'scrape'  ##change accordingly



path_to_file = r'C:\Users\tanwe\Desktop\scrapper\\'
if mode == 'scrape':
    s = Service('C:/Users/tanwe/Desktop/scrapper/teststuf-main/tmp/chromedriver/chromedriver.exe') ###Directory of your chromedriver.exe
    driver = webdriver.Chrome(service = s)
    driver.get('https://en.cf-vanguard.com/cardlist/cardsearch/?regulation=D&nation=&clan=&keyword=&keyword_type%5B%5D=all&kind%5B%5D=all&grade%5B%5D=all&power_from=&power_to=&rare=&trigger%5B%5D=all')
    time.sleep(5)
    driver.find_element(By.XPATH,"//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']").click() #click to pass cookie wall
    time.sleep(5)
    previous_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        previous_height = new_height

    page_source = driver.page_source

    f = open(path_to_file + "source.txt", "w", encoding= "utf-8")
    f.write(page_source)
    f.close()

    ###Scrapping for DivineZ standard regulation
    s = Service('C:/Users/tanwe/Desktop/scrapper/teststuf-main/tmp/chromedriver/chromedriver.exe') ###Directory of your chromedriver.exe
    driver = webdriver.Chrome(service = s)
    driver.get('https://en.cf-vanguard.com/cardlist/cardsearch/?regulation=D&nation=&clan=&keyword=dz&keyword_type%5B%5D=all&kind%5B%5D=all&grade%5B%5D=all&power_from=&power_to=&rare=&trigger%5B%5D=all')
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
    f = open(path_to_file + "source_z.txt", "w", encoding= "utf-8")
    f.write(page_source)
    f.close()

def scrape_names(f_name):

    f = open(f_name, "r", encoding= "utf-8")
    page_source = f.read()
    f.close()
    soup = BeautifulSoup(page_source, features='lxml')

    items = soup.findAll('a', href = True)
    all_card_lst = []

    for item in items:
        item_out = {}
        if "/cardlist/?cardno=" in item['href']:
            all_card_lst.append(item['href'])
    return all_card_lst


### Bs4 test
if mode != 'scrape':
    all_d_sets =  scrape_names(path_to_file + "source.txt")
    all_dz_sets = scrape_names(path_to_file + "source_z.txt")