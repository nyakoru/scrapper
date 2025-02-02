from command.tools.logrecord import logger
from command.API_post import APIpost
from command.API_get import APIget
from command.allPayload import gamePL
from requests import Response
import sys

def upload_game(payload) -> Response:
    response = APIpost('game').post_(payload)
    return response

def process_upload_game(name:str) -> Response:
    logger.info('func process upload game')
    payload = gamePL(name)
    response = upload_game(payload)
    if response.status_code == 200 or response.status_code == 201:
        logger.info("Upload game name successful")
        return response
    else: 
        logger.error(f"PRO-PR1-UPG-{response.status_code} {response.json()}")
        sys.exit()
    

def check_name_in_api(name:str) -> bool | dict:
    response:Response = APIget('game').ByExactName(name)
    if response.status_code == 200:
        data = response.json()['data']
        if data['name'] == name: 
            return True, data
        else: 
            return False, data