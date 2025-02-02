from command.tools.ArcaneUtils import fetch_csv
from command.API_post import APIpost
from command.API_get import APIget
from command.correction import correction
from command.tools.ArcaneUtils import misc
from command.tools.logrecord import logger
from requests import Response
import os
import sys

def payload(set, variant_id):
    """ 
    _____________________________________\n
    |   name   |product_code|in database|\n
    |__________|____________|___________|\n
    | Example  |   Ex-01    |    FALSE  |\n
    |__________|____________|___________|\n
    """
    ret = {
        'name':set[0],
        'product_code':set[1],
        'variant_id':variant_id,
    }
    return ret

def upload_set(payload)->Response:
    response = APIpost('sets').post_(payload)
    return response

def getallvariants(variant_id):
    ret = APIget('sets').ByVariantId(variant_id)
    data = ret['data']
    return data

def process_set_upload(folder_path, variant_id):
    logger.info('func process set upload')
    #sets = fetch_csv(f'{folder_path}/set.csv').readlist()
    sets = fetch_csv(folder_path, 'set.csv').read()
    for set in sets:
        if set[2] == 'FALSE': 
            PL = payload(set, variant_id)
            response = upload_set(PL)
            if response.status_code not in [200, 201]:
                logger.error(f"PRO-PR3-UPLSET-{response.status_code}")
                sys.exit()
            print(response.status_code)
            print(response.json())
            set[2] = 'TRUE'
    print(sets)
    fetch_csv(folder_path, 'set.csv').overwrite(sets)


def get_all_folder_names(parent_folder):
    """
    Returns a list of all subfolder names within the specified parent folder.
    
    :param parent_folder: The path of the parent directory to search
    :return: List of subfolder names
    """
    folder_names = []
    for entry in os.listdir(parent_folder):
        entry_path = os.path.join(parent_folder, entry)
        if os.path.isdir(entry_path):
            folder_names.append(entry)
    return folder_names

def process_3_verification(folder_path):
    folder_names = get_all_folder_names(folder_path)
    sets = fetch_csv(folder_path, 'set.csv').read()
    #sets = fetch_csv(f'{folder_path}/set.csv').readlist()
    for set in sets:
        if len(set)!=3: 
            raise Exception(f'set information not aligned: {set}')
        name = set[0]
        name = correction(name)
        if name not in folder_names:
            print(name)
            raise Exception(f'name not in folder: {set}')
        if not misc.path_check(f"{folder_path}/{name}/{name}.json"):
            print(name)
            raise Exception(f'json file not in folder: {set}')
