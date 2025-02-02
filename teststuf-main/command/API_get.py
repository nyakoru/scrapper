from ast import Param
from command.arcadia_functions import arcadia
from command.get_token import token_details
from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

@dataclass
class APIget:
    """API endpoint\n 
    game | variants | sets | products | products_files | products_sets"""
    endpoint: str
    url: str = field(init=False)
    END_URL: str = field(init=False)
    
    def __post_init__(self):
        self.END_URL = self.locate_endpoint()
        self.url = f'{BASE_URL}{self.END_URL}'

    def locate_endpoint(self) -> str:
        API_ENDPOINT = {
            'games': '/items/game',
            'variants': '/items/variants',
            'sets': '/items/sets',
            'products': '/items/products',
            'products_files':'/items/products_files',
            'products_sets':'/items/products_sets',
            'directus_files':'/files'
        }
        try:
            return API_ENDPOINT[self.endpoint]
        except KeyError:
            raise ValueError('Invalid API endpoint. Choose from: game, variants, sets, products_files, products_sets, directus_files')

    def access(self):
        API_TOKEN = token_details()
        headers = { 
            "Content-Type": "application/json",
            "User-Agent": "insomnia/10.1.1",
            "Authorization": f'Bearer {API_TOKEN}'
        }
        return arcadia(url=self.url, headers=headers)
    
    def All(self):
        data = self.access()
        params = {"name": "all"}
        return data.getting(params=params)
    
    def ByExactName(self, name: str):
        data = self.access()
        params = {"filter[name][_eq]": name}
        return data.getting(params=params)
    
    def ByLevelId(self, id:str):
        data = self.access()
        params = {"filter[name][_eq]": id}
        return data.getting(params=params)

    def BySetId(self, set_id: str):
        data = self.access()
        params = {"filter[set_id][_eq]": set_id}
        return data.getting(params=params)
    
    def ByVariantId(self, variant_id: str):
        data = self.access()
        params = {"filter[variant_id][_eq]": variant_id}
        return data.getting(params=params)