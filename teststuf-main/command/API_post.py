from command.arcadia_functions import arcadia
from command.get_token import token_details
from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

@dataclass
class APIpost:
    """API endpoint\n 
    game | variants | sets | products | products_files | products_sets | directus_files"""
    endpoint: str
    url: str = field(init=False)
    END_URL: str = field(init=False)
    
    def __post_init__(self):
        self.END_URL = self.locate_endpoint(self.endpoint)
        self.url = f'{BASE_URL}{self.END_URL}'

    def locate_endpoint(self, endpoint: str) -> str:
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
            return API_ENDPOINT[endpoint]
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
    
    def files_access(self):
        API_TOKEN = token_details()
        headers = { 
            "Authorization": f'Bearer {API_TOKEN}'
        }
        return arcadia(url=self.url, headers=headers)
    
    def post_(self, payload):
        data = self.access()
        response = data.posting(payload)
        return response
    
    def post_files(self, files):
        data = self.files_access()
        response = data.posting_files(files=files)
        return response