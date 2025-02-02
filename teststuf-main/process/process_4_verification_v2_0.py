from command.tools.ArcaneUtils import misc, Wrapper, fetch_json
from command.tools.logrecord import logger

log = Wrapper.log_function_call
checker = misc.path_check
folder_list = misc.get_folders

@log         
def process_4_verification(folder_path, image_data_check = False) -> bool:

    variant_id = fetch_json(folder_path, 'variant_id.json').read()['variant_id']
    
    if not misc.path_check(folder_path):
        raise FileNotFoundError('Check folder path')
    
    jobs = folder_list(f'{folder_path}')
    if jobs == []:
        raise FileNotFoundError('No files in folder')
    
    for job in jobs:
        check = checker(f'{folder_path}/{job}/set_information.json')
        if not check: 
            raise FileNotFoundError('Pre Checking Error. set_information.json not found')

        set_information = fetch_json(directory=f'{folder_path}/{job}',file_name='set_information.json').read()
        if set_information is None: 
            raise FileNotFoundError(f'{job} set information contains no data')
        try: 
            set_name = set_information['setname']
        except Exception: 
            raise ValueError(f'No setname found in {job}')
        
        if image_data_check:
            card_data = fetch_json(directory=f'{folder_path}/{job}',file_name=f'{job}.json').read()
            for card in card_data:
                product_code = card['product_code']
                image_name = f'{product_code}.png'
                image_check = checker(f'{folder_path}/{job}/{image_name}')
                if not image_check:
                    raise FileNotFoundError(f"Image Missing: {folder_path}/{job}/{image_name}")
    return "P4V Pass"

def verification_4_execution(folder_path, image_data_check = False):
    try:
        return process_4_verification(folder_path, image_data_check)
    except Exception as e:
        logger.error(f"PRO-PR4-V4-{e}")
        return "P4V Failed"