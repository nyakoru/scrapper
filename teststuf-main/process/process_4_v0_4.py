from command.tools.ArcaneUtils import fetch_csv
from command.tools.logrecord import logger
from command.tools.ArcaneUtils import misc
from pathlib import Path
from command.API_get import APIget
from command.API_post import APIpost
from process.process_image import process_image_upload
from requests import Response
from command.allPayload import prodPL
import sys

checker = misc.path_check
folder_list = misc.get_folders

PARENT = Path(__file__).parent

def retrieveSet(setname) -> list:
    logger.info(f'func retrieveSet {setname}')
    set_information = APIget('sets').ByExactName(setname)
    data = set_information['data']
    if data == []:  logger.error(f'No entry found by the name {setname}')
    return data

def payload(card, set_id, variant_id):
    logger.info('func payload')
    if card['metadata'] == None: card['metadata'] = None
    PL = prodPL(
        name = card['name'],
        description = card['description'],
        rarity = card['rarity'],
        metadata = card['metadata'],
        product_code = card['product_code'],
        variant_id = variant_id,
        set_id = set_id
    )

    return PL

def upload_card(payload):
    logger.info(f"func upload_card {payload}")
    response = APIpost('products').post_(payload)
    return response

def extract_image_id(image_json):
    logger.info("func extract_image_id ", image_json)
    return image_json["data"]["filename_disk"]

def single_card_upload_process(card_json, set_id, variant_id, job, index)-> str | bool:
    card = card_json[index]
    logger.info(f"func single_card_upload_process {card}")

    PL = payload(card, set_id=set_id, variant_id = variant_id)# need to change
    print(f"Uploading set: {job} index: {index}, name: {card_json[index]['name']}")
    logger.info(f"index:{index}")
    response:Response = upload_card(PL)
    upload_status = False

    if response.status_code == 200 or response.status_code == 201: 
        logger.info('Upload card information success')
        product_json = response.json()
        product_id = product_json['data']['id']
        upload_status = True
    else:  logger.error(f'PRO-PRD-CRD-{response.status_code} Upload card failed')
    return product_id, upload_status

def card_image_upload_process(card_json, index, directory)-> str | bool:
    card = card_json[index]
    product_code = card["product_code"]
    logger.info(f"func card_image_upload_process {card}")

    image_location = f'{directory}/{product_code}.png'
    print(image_location)
    response = process_image_upload(file_path=image_location)
    image_json = response.json()
    print(image_json)
    image_id = extract_image_id(image_json).replace('.png','')

    upload_status = False
    if response.status_code == 201 or response.status_code == 200: upload_status = True
    else: logger.error(f'PRO-PRD-IMG-{response.status_code} Upload image failed')
    return image_id, upload_status

def products_files_upload_process(product_id, image_id) -> bool:
    logger.info(f"func products_files_upload_process {product_id} {image_id}")
    payload = {"products_id" : product_id, 
               "directus_files_id"   : image_id}
    response:Response = APIpost('products_files').post_(payload)

    upload_status = False
    print(response.status_code)
    if response.status_code == 200 or response.status_code == 201: upload_status = True
    else: logger.error(f'PRO-PRD-IDS-{response.status_code} Upload id failed')
    return upload_status

def extract_set_name(directory):
    logger.info(f'func extract_set_name {directory}')
    set_information = fetch_csv(directory=directory, file_name='set_information.json').read()
    set_name = set_information['setname']
    return set_name

def extract_set_id(SET_API_JSON_DATA, set_name):
    logger.info(f'func extract_set_id {set_name}')
    try: set_id = SET_API_JSON_DATA[0]['id']
    except Exception:
        logger.warning(f'set id not found - {set_name}')
        set_id = ""
    return set_id

def status_checker(product_status, id_status, image_status):
    if (product_status or id_status or image_status) == False: 
        print(f'Product status: {product_status}')
        print(f'img id tatus: {image_status}')
        print(f'id status: {id_status}')
        sys.exit()
    
def process_card_upload(folder_path, variant_id, starting_index=0):
    logger.info('process func card upload')
    jobs = folder_list(path=f'{folder_path}')
    for job in jobs:
        directory = f'{folder_path}/{job}'
        set_name = extract_set_name(directory)
        SET_API_JSON_DATA = retrieveSet(set_name)
        set_id = extract_set_id(SET_API_JSON_DATA, set_name)

        card_json = fetch_csv(directory=f'{folder_path}/{job}',file_name=f'{job}.json').read()
        for i in range(starting_index, len(card_json)): 
            product_id, product_status = single_card_upload_process(card_json, set_id, variant_id, job, i)
            image_id, image_status = card_image_upload_process(card_json, i, directory)
            id_status = products_files_upload_process(product_id, image_id)
            status_checker(product_status, id_status, image_status)

def process_4_verify_process(folder_path) -> bool:
    logger.info('func process_4_pre_checker')
    jobs = folder_list(path=f'{folder_path}')
    for job in jobs:
        check = checker(f'{folder_path}/{job}/set_information.json')
        if not check: raise Exception('Pre Checking Error. set_information.json not found')

        set_information = fetch_csv(directory=f'{folder_path}/{job}',file_name='set_information.json').read()
        if set_information is None: raise Exception(f'{job} set information contains no data')

        try: set_name = set_information['setname']
        except Exception: raise Exception(f'No setname found in {job}')

        print(job,' ',check)

    return True


"""
example

given setlist

jobs = createjobs(setlist)
process_4_pre_checker(jobs, directory)

# jobs = [(name1, set_id1), (name2, set_id2), ...]
for job in jobs:
    setname = job[0]
    set_id = job[1]
    process_4(data:dict, upload_function, set_id, setname, default_language, attain_card_data)
"""

"""
attain_card_data function example:

def attain_card_data(setname):
    setname = correction(setname)
    directory = './YGO/yugioh_sets/{setname}'
    file = fetch_csv(directory=directory, filename=setname)
    data =  file.read()
    return data
"""