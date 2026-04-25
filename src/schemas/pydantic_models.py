from pydantic import BaseModel
from typing import Optional

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
    room_no:int
    room_type_id:str
    status: str = "available"


class Bookings(BaseModel):
    user_id:Optional[int] = None
    room_id: Optional[int] = None
    room_no: Optional[str] = None
    room_type_id:int
    check_in:str
    check_out:str
    guests:int
    price:float
    status: Optional[str] = "pending"


class RoomAvailability(BaseModel):
    check_in:str
    check_out:str
    capacity:int
    room_type_id:int

class Payment(BaseModel):
    booking_id:str
    amount:float
    desc:str
    cust_id:int=None
    cust_name:str=None
    cust_email:str=None
    cust_mobile:str=None