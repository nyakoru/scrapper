from command.tools.ArcaneUtils import fetch_csv, fetch_json, misc
from command.tools.logrecord import logger
from pathlib import Path
from command.API_get import APIget
from command.API_post import APIpost
from process.process_image import process_image_upload
from requests import Response
from command.allPayload import prodPL
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import sys
import os

checker = misc.path_check
folder_list = misc.get_folders

PARENT = Path(__file__).parent
ROOT = PARENT.parent

def retrieveSet(setname) -> list:
    logger.info(f'func retrieveSet {setname}')
    set_information = APIget('sets').ByExactName(setname)
    data = set_information['data']
    if data == []:  logger.error(f'PRO-PR4-RETRIEVE-No entry found by the name {setname}')
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

def single_card_upload_process(card_json, set_id, variant_id, job, index, iset)-> str | bool:
    card = card_json[index]
    logger.info(f"func single_card_upload_process {card}")

    PL = payload(card, set_id=set_id, variant_id = variant_id)
    logger.info(f"Uploading set: {job} index: {index}, name: {card_json[index]['name']}, set_index:{iset}")
    response:Response = upload_card(PL)
    upload_status = False

    if response.status_code == 200 or response.status_code == 201: 
        logger.info('Upload card information success')
        product_json = response.json()
        product_id = product_json['data']['id']
        upload_status = True
    else:  logger.error(f'PRO-PR4-CARDUPL-{response.status_code} Upload card failed')
    return product_id, upload_status

def card_image_upload_process(card_json, index, directory)-> str | bool:
    card = card_json[index]
    product_code = card["product_code"]
    logger.info(f"func card_image_upload_process {card}")

    image_location = f'{directory}/{product_code}.png'
    response = process_image_upload(file_path=image_location)
    image_json = response.json()
    image_id = extract_image_id(image_json).replace('.png','')

    upload_status = False
    if response.status_code == 201 or response.status_code == 200: upload_status = True
    else: logger.error(f'PRO-PR4-IMG-{response.status_code} Upload image failed')
    return image_id, upload_status

def products_files_upload_process(product_id, image_id) -> bool:
    logger.info(f"func products_files_upload_process {product_id} {image_id}")
    payload = {"products_id"        : product_id, 
               "directus_files_id"  : image_id}
    response:Response = APIpost('products_files').post_(payload)

    upload_status = False
    if response.status_code == 200 or response.status_code == 201: upload_status = True
    else: logger.error(f'PRO-PR4-IDUP-{response.status_code} Upload id failed')
    return upload_status

def extract_set_name(directory):
    logger.info(f'func extract_set_name {directory}')
    set_information = fetch_json(directory=directory, file_name='set_information.json').read()
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
    
def process_card_upload(folder_path, variant_id, starting_index=0, set_index=0, max_workers = os.cpu_count()):
    logger.info('process func card upload')
    jobs = folder_list(path=f'{folder_path}')
    for isets in range(set_index, len(jobs)):
        job = jobs[isets]
        directory = f'{folder_path}/{job}'
        set_name = extract_set_name(directory)
        SET_API_JSON_DATA = retrieveSet(set_name)
        set_id = extract_set_id(SET_API_JSON_DATA, set_name)

        card_json = fetch_json(directory=f'{folder_path}/{job}',file_name=f'{job}.json').read()
        def upload_process(card_json, set_id, variant_id, job, i, directory, iset):
            product_id, product_status  = single_card_upload_process(card_json, set_id, variant_id, job, i, iset)
            image_id,   image_status    = card_image_upload_process(card_json, i, directory)
            id_status                   = products_files_upload_process(product_id, image_id)
            status_checker(product_status, id_status, image_status)

        total_tasks = len(card_json) - starting_index
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            with tqdm(total=total_tasks, desc="Uploading", unit="card") as progress_bar:
                futures = {executor.submit(upload_process, card_json, set_id, variant_id, job, i, directory, isets): i for i in range(starting_index, len(card_json))}
                for future in as_completed(futures):
                    try: future.result()
                    except Exception as e: logger.error(f"PRO-PR4-PROCARDUPL-THREAD-Error in upload_process: {e}")
                    finally: progress_bar.update(1)