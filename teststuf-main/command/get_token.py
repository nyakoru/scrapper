from command.arcadia_functions import arcadia, time
from command.tools.ArcaneUtils import fetch_json
from command.accesskey import tokenUrl, keyheaders, payload
from command.tools.logrecord import logger
import sys

TOKEN_TERM = "access_token"
EXPIRY_TERM = "expiration_timestamp"

def get_token(tokenUrl:str=tokenUrl, keyheaders:dict=keyheaders, payload:dict=payload) -> tuple[str, int, int]:
    """
    Function returns Access Token String, and Time of Expiry Integer\n
    No Input is required unless there is a change
    """
    token_data = arcadia(url=tokenUrl, headers=keyheaders).posting(payload=payload).json()
    if token_data == False:
        print('Unable to get key')
        sys.exit()
    else: print('Token Response received')
    data_header = True
    if data_header: token_data = token_data["data"]
    access_token = token_data.get(TOKEN_TERM)
    timeStampNow = time.timeStamp()
    hourglass = token_data.get("expires")
    expiryTime = int(timeStampNow + hourglass/1000)
    token_data[EXPIRY_TERM] = expiryTime
    savingfile = fetch_json(file_name='api_access_token').dump([token_data])
    if not savingfile:
        logger.error('CMD-GTK-TOKEN')
        sys.exit()
    print("Refresh token: ", token_data.get("refresh_token"))
    print("Expires at ", time.readableTimeStamp(timestamp = expiryTime))

    return access_token, int(expiryTime)

def token_details():
    """
    Function returns Access Token String, and Time of Expiry Integer\n
    No Input is required unless there is a change
    """
    API_data:list = fetch_json(file_name='api_access_token').read()
    API_token = API_data[0].get(TOKEN_TERM)
    TimeOfExpiry = int(API_data[0].get(EXPIRY_TERM))
    if time.timeStampExpiryChecker(expiryTime=TimeOfExpiry) == True: API_token, TimeOfExpiry = get_token()
    return API_token

if __name__ == "__main__":
    print(token_details())
    