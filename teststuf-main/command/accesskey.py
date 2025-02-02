from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_URL = os.getenv("TOKEN_URL")
API_ADMIN_USER = os.getenv("API_USER")
API_ADMIN_PASSWORD = os.getenv("PASSWORD")

tokenUrl = TOKEN_URL

keyheaders = {
    "Content-Type": "application/json",
    "User-Agent": "insomnia/10.1.1"
}

payload = {
    "email": API_ADMIN_USER,
    "password": API_ADMIN_PASSWORD
}