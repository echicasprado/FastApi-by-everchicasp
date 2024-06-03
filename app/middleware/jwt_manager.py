import os
from dotenv import load_dotenv
from jwt import encode, decode

load_dotenv()

TOKEN_KEY = os.getenv("MY_KEY")

def create_token(data: dict):
    token: str = encode(payload=data, key=TOKEN_KEY, algorithm="HS256")
    return token

def validate_token(token:str) -> dict:
    return decode(token,key=TOKEN_KEY,algorithms=["HS256"])