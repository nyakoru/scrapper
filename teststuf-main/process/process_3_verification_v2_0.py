from command.tools.ArcaneUtils import fetch_csv, fetch_json, misc, Wrapper
from command.API_get import APIget
from command.correction import correction
from command.tools.logrecord import logger

@Wrapper.log_function_call
def process_3_verification(folder_path, API_online=False):
    variant_id = fetch_json(folder_path, 'variant_id.json').read()['variant_id']
    if API_online:
        api_var = APIget("variants").ByLevelId(variant_id)['data']
        if api_var == None: raise Exception(f'variant id do not exist.')
        data = APIget("sets").ByVariantId(variant_id)['data']
    folder_names = misc.get_folders(folder_path)
    sets = fetch_csv(folder_path, 'set.csv').read()
    for set in sets:
        if len(set)!=3: 
            raise Exception(f'set information not aligned: {set}')
        name = set[0]
        corrected_name = correction(name)
        in_database = set[2]
        if in_database == "FALSE" or "RECURRENT":    
            if corrected_name not in folder_names:
                raise Exception(f'name not in folder: {set}')
            if not misc.path_check(f"{folder_path}/{corrected_name}/{corrected_name}.json"):
                raise Exception(f'json file not in folder: {set}')
        if API_online:
            if in_database == "FALSE":
                for item in data:
                    API_name = item['name']
                    if name == API_name:
                        raise FileExistsError('set name in API')
    return "P3V Pass"
        
def verification_3_execution(folder_path, API_online=False):
    try:
        return process_3_verification(folder_path, API_online=API_online)
    except Exception as e:
        logger.error(f"PRO-PR3-V3-{e}")
        return "P3V Failed"