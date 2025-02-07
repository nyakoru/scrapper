import requests
from bs4 import BeautifulSoup
from command.tools.ArcaneUtils import fetch_json

class extract_info():

    def __init__(self, url):

        self.url = 'https://en.cf-vanguard.com' + url
        self.page = requests.get(self.url)
    
    def get_img(self):  ##directory is the file path that you would like to save your image in
        card_website = self.url.split('/')
        for parts in card_website:
            if "cardno" in parts:
                card_code = parts
                break
        card_code = card_code.split("cardno=")[1] ##card number is in nested index 1
        card_code = ''.join(filter(str.isalnum, card_code)) ###remove the dash sign
        card_code = card_code.lower() ##lower cast for the links
        images = self.soup.findAll('img')
        for image in images:
            if card_code in image['src']:
                lk = "https://en.cf-vanguard.com" + image['src']
                nme = image['alt']
                break
        
        with open(nme + '.jpg', 'wb') as f:
            im = requests.get(lk)
            f.write(im.content)
            f.close()






    
    
