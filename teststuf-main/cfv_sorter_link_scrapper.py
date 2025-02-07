import requests
from bs4 import BeautifulSoup


class extract_info():

    def __init__(self, url):

        self.url = 'https://en.cf-vanguard.com' + url
        self.page = requests.get(self.url)
    
    def get_img(self):  ##image scrape
        soup = BeautifulSoup(self.page.content, 'html.parser')
        card_website = self.url.split('/')
        for parts in card_website:
            if "cardno" in parts:
                card_code = parts
                break
        card_code = card_code.split("cardno=")[1] ##card number is in nested index 1
        card_code = ''.join(filter(str.isalnum, card_code)) ###remove the dash sign
        card_code = card_code.lower() ##lower cast for the links
        images = soup.findAll('img')
        for image in images:
            if card_code in image['src']:
                lk = "https://en.cf-vanguard.com" + image['src']
                nme = image['alt']
                break
        
        with open(nme + '.jpg', 'wb') as f:
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

        card_info = {
        "serial number": serial_number.text,
        "name": name.text,
        "type": typ.text,
        "nation": nation.text,
        "race": race.text,
        "grade": grade.text,
        "power": power.text,
        "critical": critical.text,
        "shield": shield.text,
        "skill": skill.text,
        "effect": effect.text,
        "flavor": flavor.text,
        "rarity": rarity.text
        }
        return card_info






    
    
