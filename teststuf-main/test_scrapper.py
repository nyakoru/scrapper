from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from cfv_sorter_link_scrapper import extract_info
from command.tools.ArcaneUtils import fetch_json
import os

mode = 'extract'  ##change accordingly

path_to_file = r'C:/Users/tanwe/Desktop/scrapper/'  ###Path where you want your source.txt to be


if mode == 'scrape':
    s = Service('C:/Users/tanwe/Desktop/scrapper/teststuf-main/tmp/chromedriver/chromedriver.exe') ###Directory of your chromedriver.exe
    driver = webdriver.Chrome(service = s)
    driver.get('https://en.cf-vanguard.com/cardlist/cardsearch/?regulation=D&nation=&clan=&keyword=&keyword_type%5B%5D=all&kind%5B%5D=all&grade%5B%5D=all&power_from=&power_to=&rare=&trigger%5B%5D=all')
    time.sleep(3)
    driver.find_element(By.XPATH,"//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']").click() #click to pass cookie wall
    time.sleep(5)
    previous_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        time.sleep(3)
        if new_height == previous_height:
            break
        previous_height = new_height

    page_source = driver.page_source

    f = open(path_to_file + "source.txt", "w", encoding= "utf-8")
    f.write(page_source)
    f.close()

    ###Scrapping for DivineZ standard regulation
'''
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

'''

def scrape_names(f_name):

    f = open(f_name, "r", encoding= "utf-8")
    page_source = f.read()
    f.close()
    soup = BeautifulSoup(page_source, features='lxml')

    items = soup.findAll('a', href = True)
    all_card_lst = []

    for item in items:
        item_out = {}
        if "/cardlist/?cardno=" in item['href']: ##Only D standard released cards to avoid old backwards compatible cards
            all_card_lst.append(item['href'])
    return all_card_lst


### Bs4 test
if mode != 'scrape':
    all_d_sets =  scrape_names(path_to_file + "source.txt")
    all_cards = []
 
    for website in all_d_sets:
        while(website):
            try:
                wbp = extract_info(website)
                card_data = wbp.get_info()
                print(card_data['serial number'])
                serial_num = card_data['serial number']
                set_num = serial_num.split('/')
                set_num = set_num[0]
                folder_name = f"{set_num}"
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                wbp.get_img("C:/Users/tanwe/Desktop/scrapper/teststuf-main", serial_num)
                ##file = fetch_json(directory = f"{set_num}", file_name = f"cfv {set_num}_scrapper") ###Change directory accordingly
                ##file.add(card_data)
                print("Card added into db")
                break
            
            except:
                continue




##Test