import requests
from datetime import datetime
from datetime import timedelta
import sys
from dataclasses import dataclass
from requests import Response

verify = True

@dataclass
class arcadia:

    url:str
    headers:set
    
    def posting(self, payload:set) -> Response:
        response = requests.post(url=self.url, headers=self.headers, json=payload, verify=verify)
        if response.status_code in [200, 201]: return response
        else:
            print(f'Response Error: {response.status_code} - {response.text}')
            sys.exit()
        
    def posting_files(self, files) -> Response:
        response = requests.post(url=self.url, headers=self.headers, files=files, verify=verify)
        if response.status_code in [200, 201]: return response
        else:
            print(f'Response Error: {response.status_code} - {response.text}')
            sys.exit()

    def getting(self, params):
        response = requests.get(url=self.url, headers=self.headers, params=params, verify=verify)
        if response.status_code == 200:
            sets = response.json()
            if sets: return sets
            else: return None
        else: print(f'Response Error: {response.status_code} - {response.text}')

    def deleting(self, setid):
        url = f'{self.url}/{setid}'
        response = requests.delete(url=url, headers=self.headers, verify=verify)
        if response.status_code in [200, 204]: 
            print(f'Deletion {setid} Successful')
            return True
        else: 
            print(response.status_code)
            return True

    def patching_(self, changes) -> Response:
        response = requests.patch(url=self.url, headers=self.headers, json=changes, verify=verify)
        if response.status_code in [200, 201]: return response
        else: 
            print(f'Response Error: {response.status_code} - {response.text}')
            sys.exit()

    def patching_files(self, changes):
        response = requests.patch(url=self.url, headers=self.headers, files=changes, verify=verify)
        if response.status_code in [200, 204]:
            return response
        else:
            print(f'Response Error: {response.status_code} - {response.text}')
            sys.exit()
        
class datasearch:
    def __init__(self) -> None:
        pass

    def data_return(self, input_dict:dict, *keys:str):
        """
        Requires input dictionary and *keys
        """
        values = []
        for key in keys:
            if key in input_dict: values.append(input_dict[key])
            else: values.append(None)
        return values
    
    def data_search(self, input_dict:dict, name:str) -> bool:
        """
        response json dictionary (with 'data:' key included)\n
        Requires input dictionary and name
        """
        database = input_dict['data']
        for json in database:
            if name in json.values(): return True
        return False
    
    def data_search_ret_key(self, input_dict:dict, name:str):
        database:list = input_dict['data']
        for json in database:
            if name in json.values(): return json
        return False

    def ret_from_set(self, dict_data):
        database:dict = dict_data
        self.data_return(database, "id", "default_language",)
        
class time:

    def timeNow():
        return datetime.now()
    
    def timeElapsed(start_time):
        return start_time - time.timeNow()
        
    def timeDelta(start_time, target_elapsed_time)-> bool:
        """
        Returns True, if X amount of time have elapsed from the initial time\n
        X = target_elapsed_time\n
        start_time = initial time
        """
        if time.timeElapsed(start_time) >= timedelta(seconds=target_elapsed_time): return True
        else: return False

    def timeStamp()->int:
        now=time.timeNow()
        return int(now.timestamp())
    
    def timeStampExpiryChecker(expiryTime)->bool:
        """
        Takes the time of expiry as input\n
        Returns True if current time has cross threshold
        """
        if time.timeStamp() >= expiryTime: return True
        else: return False

    def readableTimeStamp(timestamp)->str:
        return datetime.fromtimestamp(timestamp)
