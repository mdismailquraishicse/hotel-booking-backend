from typing import Optional
from fastapi import Request, FastAPI
from src.services.auth import Authentication
from src.models.pydantic_models import Creds, User, Room, Bookings
from src.schemas.db import get_connection, get_users, register_user, get_rooms, add_room, booking as book_room, get_bookings, search_available_rooms

app = FastAPI()
authentication = Authentication()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "server is running..."}

@app.post("/register")
def register(request:Request, user:User):
    user.password = authentication.password_encrypt(user.password).decode("utf-8")
    conn = get_connection()
    register_user(conn=conn, user=user)
    conn.close()

    return {"message": "User registered successfully"}

@app.post("/login")
def login(request:Request, creds:Creds):
    token = None
    conn = get_connection()

    query = f"""
        SELECT email, password
        FROM users
        WHERE email = '{creds.email}'
    """
    cursor = conn.cursor()
    cursor.execute(query)
    user_cred = cursor.fetchone()
    print(f"user_cred in login: {user_cred}")
    if not user_cred:
        return "user not registered"
    hashed_password = user_cred[1]
    is_authenticated = authentication.password_validate(password=creds.password,
                                                        password_hash=hashed_password.encode("utf-8"))
    print(f"authentication: {is_authenticated}")
    if is_authenticated:
        token_payload = {
            "email": user_cred[0]
        }
        token = authentication.generate_token(token_payload)
        print(f"tokennnn: {token}")
    return {"token":token}

@app.get("/fetch-users")
def fetch_users():
    conn = get_connection()
    users = get_users(conn=conn)
    print(f"users: {users}")
    return users

@app.get("/rooms")
def get_rooms():
    conn = get_connection()
    rooms = get_rooms(conn=conn)
    print(f"rooms: {rooms}")

@app.get("/room/{room_id}")
def get_room(room_id):
    return table_rooms.get(room_id)

@app.post("/post")
def create_room(room:Room):
    conn = get_connection()
    add_room(conn=conn, room=room)
    return {
        "message": "room added successfully"
    }


@app.delete("/room/{room_id}")
def delete_room(room_id):
    table_rooms.pop(room_id)
    print(f"room deleted: {room_id}")
    print(f"available rooms: {table_rooms}")

@app.post("/bookings")
def bookings(booking:Bookings):
    conn = get_connection()
    book_room(conn=conn, booking=booking)
    return "successfully booked"

@app.delete("/bookings/{booking_id}")
def bookings():
    pass

@app.get("/bookings")
def bookings():
    conn = get_connection()
    bookings = get_bookings(conn=conn)
    booking_result = [
        {
            "room_id":booking[0],
            "room_type":booking[1],
            "check_in": booking[2],
            "check_out": booking[3],
            "capacity": booking[4],
            "price": booking[5]
            } for booking in bookings
        ]
    print(f"fetched bookings: {bookings}")
    print(f"booking_result: {booking_result}")
    return booking_result

@app.get("/booking-by-user/{email}")
def bookings_by_user(email:str):
    pass

@app.get("/rooms/{room_id}/{check_in}/{check_out}")
def availability(room_id:int, check_in:str, check_out:str):
    """
    return: True/False
    """
    rooms = list(table_bookings.values())
    print(f"rooms: {rooms}")
    room = None
    for i,r in enumerate(rooms):
        print(f"compare:  {i}: {r}")
        if r.room_id == int(room_id):
            room = r
    # room= table_rooms.get(room_id)
    print(f"room: {room}")
    if not room:
        return f"No room found with the id: {room_id}"
    if (room.check_in == check_in):
        print(f"room already occupied")
        return f"room already occupied: {room_id}"
    return f"room is available"

@app.get("/search-available-rooms")
def search_room(check_in:Optional[str]=None,
                check_out:Optional[str]=None,
                capacity:Optional[str]=None):
    print(f"searcing room availability...")
    print(f" params: {check_in} {check_out} {capacity}")

    conn = get_connection()
    data = search_available_rooms(conn=conn,
                                  check_in=check_in,
                                  check_out=check_out,
                                  capacity=capacity)
    rooms = [
        {"room_id" : room[0],
            "image" : room[1],
            "room_type" : room[2],
            "price" : room[3],
            "capacity" : room[4],
            "amenities" : room[5]} for room in data
    ]
    return {
        "status": "success",
        "result": rooms
    }