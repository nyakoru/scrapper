import requests
from bs4 import BeautifulSoup
from command.tools.ArcaneUtils import fetch_json

url = "https://en.cf-vanguard.com/cardlist/?cardno="
format = 'DZ'
booster = 'BT05'
serial = '000'
endpoint = f'{format}-{booster}/{serial}EN' #card set number in the format of format-booster/serial, add EN at the back if you are scrapping EN cards
page = requests.get(url + endpoint)
soup = BeautifulSoup(page.content, 'html.parser')
name = soup.find('span', class_ = 'face')

max_card = 119 #max number of base rare cards in the booster
file = fetch_json(directory = "", file_name = f"cfv {booster}_scrapper")
for card_num in range(1, max_card + 1):
    if card_num < 10:
        serial = "00" + str(card_num)
    elif card_num < 100:
        serial = "0" + str(card_num)
    else:
        serial = str(card_num)
    endpoint = f'{format}-{booster}/{serial}EN' #card set number in the format of format-booster/serial, add EN at the back if you are scrapping EN cards
    page = requests.get(url + endpoint)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    ##Image Scrapping
    images = soup.findAll('img')
    for image in images:
        format_boost = format + booster
        format_boost = format_boost.lower()
        if format_boost in image['src']:
            lk = "https://en.cf-vanguard.com" + image['src']
            nme = image['alt']
    with open(nme + '.jpg', 'wb') as f:
        im = requests.get(lk)
        f.write(im.content)
        f.close()
    ##Webpage scrapping
    name = soup.find('span', class_ = 'face')
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
    card = {
        "serial number": endpoint,
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
    file.add(card)
##FFR scraping
#Identify how many FFRs there are in the set 


ffr_count = 18 #input in number of ffrs in this set

for card_num in range(1, ffr_count + 1):
    if card_num < 10:
        serial = "FFR" + "0" + f"{card_num}"
    else: #FFRs and FR are generally below 100
        serial = "FFR" + f"{card_num}"
    endpoint = f'{format}-{booster}/{serial}EN'
    page = requests.get(url + endpoint)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    ##Image Scrapping
    images = soup.findAll('img')
    for image in images:
        format_boost = format + booster
        format_boost = format_boost.lower()
        if format_boost in image['src']:
            lk = "https://en.cf-vanguard.com" + image['src']
            nme = image['alt']
    with open(nme + "_FFR" '.jpg', 'wb') as f:
        im = requests.get(lk)
        f.write(im.content)
        f.close()
    ##Webpage data scrapping
    name = soup.find('span', class_ = 'face')
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
    card = {
        "serial number": endpoint,
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
    file.add(card)

fr_count = 48 #input in number of frs in this set

for card_num in range(1, fr_count + 1):
    if card_num < 10:
        serial = "FR" + "0" + f"{card_num}"
    else: #FFRs and FR are generally below 100
        serial = "FR" + f"{card_num}"
    endpoint = f'{format}-{booster}/{serial}EN'
    page = requests.get(url + endpoint)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    ##Image Scrapping
    images = soup.findAll('img')
    for image in images:
        format_boost = format + booster
        format_boost = format_boost.lower()
        if format_boost in image['src']:
            lk = "https://en.cf-vanguard.com" + image['src']
            nme = image['alt']
    with open(nme + "_FR" '.jpg', 'wb') as f:
        im = requests.get(lk)
        f.write(im.content)
        f.close()
    ##Webpage data scrapping
    name = soup.find('span', class_ = 'face')
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
    card = {
        "serial number": endpoint,
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
    file.add(card)

sr_count = 42 #input in number of SRs in this set

for card_num in range(1, sr_count + 1):
    if card_num < 10:
        serial = "SR" + "0" + f"{card_num}"
    else: #FFRs and FR are generally below 100
        serial = "SR" + f"{card_num}"
    endpoint = f'{format}-{booster}/{serial}EN'
    page = requests.get(url + endpoint)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    ##Image Scrapping
    images = soup.findAll('img')
    for image in images:
        format_boost = format + booster
        format_boost = format_boost.lower()
        if format_boost in image['src']:
            lk = "https://en.cf-vanguard.com" + image['src']
            nme = image['alt']
    with open(nme + "_SR" + '.jpg', 'wb') as f:
        im = requests.get(lk)
        f.write(im.content)
        f.close()
    ##Webpage data scrapping
    name = soup.find('span', class_ = 'face')
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
    card = {
        "serial number": endpoint,
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
    file.add(card)

SEC_count = 5 #input in number of frs in this set

for card_num in range(1, SEC_count + 1): #the last SEC of the set is not captured if set to +1
    if card_num < 10:
        serial = "SEC" + "0" + f"{card_num}"
    else: #FFRs and FR are generally below 100
        serial = "SEC" + f"{card_num}"
    endpoint = f'{format}-{booster}/{serial}EN'
    page = requests.get(url + endpoint)
    ##Image Scrapping
    images = soup.findAll('img')
    for image in images:
        format_boost = format + booster
        format_boost = format_boost.lower()
        if format_boost in image['src']:
            lk = "https://en.cf-vanguard.com" + image['src']
            print(lk)
            nme = image['alt']
    with open(nme + '_SEC' + '.jpg', 'wb') as f:
        im = requests.get(lk)
        f.write(im.content)
        f.close()
    ##Webpage data scrapping
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.find('span', class_ = 'face')
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
    card = {
        "serial number": endpoint,
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
    file.add(card)