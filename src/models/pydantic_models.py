from pydantic import BaseModel
from typing import List, Optional

class Creds(BaseModel):
    email:str
    password:str

class User(BaseModel):
    user_id:int=None
    name:str
    gender:str
    email:str
    password:str

class Room(BaseModel):
    room_id:int = None
    image:str = None
    room_type:str
    price:float
    capacity:int
    amenities:List[str] = []

class Bookings(BaseModel):
    email:str
    room_id:int
    room_type:str
    check_in:str
    check_out:str
    guests:int
    price:float

class Payment(BaseModel):
    mode:str
    card_no: str
    amount:float