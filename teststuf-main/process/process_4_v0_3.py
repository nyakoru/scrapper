from command.tools.ArcaneUtils import fetch_csv, misc
from command.tools.logrecord import logger
from command.correction import reverse_correction
from pathlib import Path
from command.API_get import APIget
from command.API_post import APIpost
from process.process_image import process_image_upload

checker = misc.path_check
folder_list = misc.get_folders

PARENT = Path(__file__).parent

def retrieveSet(setname):
    logger.info(f'func retrieveSet {setname}')
    setname = reverse_correction(setname)
    print(setname)
    ret = APIget('sets').ByExactName(setname) #need to change to directus
    data = ret['data']
    if data == []:  logger.error(f'No entry found by the name {setname}')
    return data

def payload(card, set_id, variant_id, image_id):
    logger.info('func payload')
    card['sets'] = set_id
    card['variant'] = variant_id
    card['display_images'] = image_id
    return card

def upload_card(payload):
    logger.info(f"func upload_card {payload}")
    response = APIpost('products').post_(payload)
    return response

def extract_image_id(image_json):
    logger.info("func extract_image_id ", image_json)
    return image_json["data"]["filename_disk"]

def single_card_upload_process(card_json, set_id, variant_id, job, i, directory):
    card = card_json[i]
    product_code = card["product_code"]
    logger.info(f"func single_card_upload_process {card}")

    image_location = f'{directory}/{product_code}.png'
    response = process_image_upload(file_path=image_location)
    image_json = response.json()
    image_id = extract_image_id(image_json)

    PL = payload(card, set_id=set_id, variant_id = variant_id, image_id = image_id)# need to change
    print(f"Uploading set: {job} index: {i}, name: {card_json[i]['name']}")
    response = upload_card(PL)
    if response.status_code == 200: logger.info('Upload card information success')
    else:  logger.error(f'40003 Upload card failed {response.status_code}')

def extract_set_name(directory):
    logger.info(f'func extract_set_name {directory}')
    set_information = fetch_csv(directory=directory, file_name='set_information.json').read()
    set_name = set_information['setname']
    return set_name

def extract_set_id(SET_API_JSON_DATA, set_name):
    logger.info(f'func extract_set_id {set_name}')
    try: set_id = SET_API_JSON_DATA['id']
    except Exception:
        logger.warning(f'set id not found - {set_name}')
        set_id = ""
    return set_id
    
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
            single_card_upload_process(card_json, set_id, variant_id, job, i, directory)
            import sys
            sys.exit()
        
def process_4_pre_checker(folder_path) -> bool:
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