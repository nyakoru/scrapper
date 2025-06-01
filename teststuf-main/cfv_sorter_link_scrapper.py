import requests
from bs4 import BeautifulSoup
import os

class extract_info():

    def __init__(self, url):

        self.url = 'https://en.cf-vanguard.com' + url
        self.page = requests.get(self.url)
    
    def get_img(self, path_to_file, serial_code):  ##image scrape
        soup = BeautifulSoup(self.page.content, 'html.parser')
        card_website = self.url.split('/')
        for parts in card_website:
            if "cardno" in parts:
                card_code = parts
                break
        card_code = card_code.split("cardno=")[1] ##card number is in nested index 1
        card_code = ''.join(filter(str.isalnum, card_code)) ###remove the dash sign
        print(card_code)
        images = soup.findAll('img')
        for image in images:
            if "cardlist" in image['src']:
                lk = "https://en.cf-vanguard.com" + image['src']
                break
        path_to_file = os.path.join(path_to_file, serial_code) ##direct to the exact location
        with open(path_to_file + '.png', 'wb') as f: ##ensure data is an image
            im = requests.get(lk)
            f.write(im.content)
            f.close()
    
    def get_info(self):

        soup = BeautifulSoup(self.page.content, 'html.parser')
        name = soup.find('span', class_ = 'face')
        serial_number = soup.find('div', class_ = "number")
        typ = soup.find('div', class_ = "type")
        nation = soup.find('div', class_ = "nation")
        race = soup.find('div', class_ = "race")
        grade = soup.find('div', class_ = "grade")
        power = soup.find('div', class_ = "power")
        critical = soup.find('div', class_ = "critical")
        shield = soup.find('div', class_ = "shield")
        skill = soup.find('div', class_ = "skill")
        effect = soup.find('div', class_ = "effect")
        flavor = soup.find('div', class_ = "flavor")
        rarity = soup.find('div', class_ = "rarity")
        
        try:
            serial_num = serial_number.text
        except:
            serial_num = "No serial number"
            print(self)

        card_info = {
        "product_code": serial_num,
        "name": name.text,
        "description": skill.text,
        "rarity": rarity.text
        }
        return card_info
    
    def get_set_info(self): 
        ##Not every set has info on it so this will skip all the sets if no info regarding the set can be loaded up

        card_website = self.url.split('/')
        for parts in card_website:
            if "cardno" in parts:
                card_code = parts
                break
        card_code = card_code.split("cardno=")[1]
        set_product_code = card_code
        card_code = ''.join(filter(str.isalnum, card_code))
        card_code = card_code.lower()
        product_site = "https://en.cf-vanguard.com/products/" + card_code
        try:
            product_page = requests.get(product_site)
            soup = BeautifulSoup(product_page.content, "html,parser")
            name = soup.find("div", class_= "title")
            table = soup.find('table')
            for row in table.find_all('tr'):
                table_header = row.find('th')
                value = row.find('td')
                if table_header and value:
                    header_text = table_header.text.strip()
                    value_text = value.text.strip()
                    
                    if header_text == 'Release Date':
                        release_date = value_text
                    elif header_text == 'Card Types':
                        card_types = value_text
            game_info = {
                "setname": name,
                "set_description":card_types,
                "set_product_code":set_product_code,
                "release_date":release_date,
                "variant_id":null,
                "set_id":null,
                "status":"published",
                "total": 0
            }
            return game_info

        except:
            print(f"{set_product_code} is not a valid product, might be a tournament exclusive")
        










    
    
