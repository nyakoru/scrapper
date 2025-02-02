from command.tools.logrecord import logger
from command.API_post import APIpost
from command.API_get import APIget
from command.allPayload import varPL
from requests import Response
import sys

def upload_variant(payload) -> Response:
    response = APIpost('variants').post_(payload)
    return response

def process_upload_variant(variant:str, game_id:str) -> Response:
    logger.info('func process upload variant')
    payload = varPL(variant, game_id)
    response = upload_variant(payload)
    if response.status_code == 200 or response.status_code == 201:
        logger.info("Upload variant successful")
        return response
    else: 
        logger.error(f"PRO-PR2-UPLVARIANT-{response.status_code} {response.json()}")
        sys.exit()
