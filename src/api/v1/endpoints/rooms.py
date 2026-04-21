import traceback
from typing import Optional
from src.db.session import get_db
from fastapi import APIRouter, Depends
from src.schemas.pydantic_models import Room, RoomAvailability
from src.services.rooms import RoomService


router = APIRouter()
room_service = RoomService()


@router.get("/search-available-rooms")
def search_room(check_in:Optional[str]=None,
                check_out:Optional[str]=None,
                capacity:Optional[str]=None,
                conn=Depends(get_db)):
    
    try:        
        rooms = room_service.search_available_rooms(check_in = check_in,
                                                    check_out = check_out,
                                                    capacity = capacity,
                                                    conn=conn)


        return {
            "status": "success",
            "result": rooms,
            "error" : None,
            "message" : "Available rooms fetched successfully"
        }
    except Exception as e:
        return {
            "status": "failed",
            "result": [],
            "error" : traceback.format_exc(),
            "message" : str(e)
        }


@router.post("/create-room")
def create_room(room:Room, conn=Depends(get_db)):
    try:
        res = room_service.create_room(conn=conn, room=room)
        conn.commit()
        return {
            "status" : "success",
            "result" : res,
            "error" : None,
            "message" : "Room added successfully"
        }
    except Exception as e:
        return {
            "status" : "failed",
            "result" : False,
            "error" : traceback.format_exc(),
            "message" : str(e)
        }


@router.delete("/delete-room/{room_id}")
def delete_room(room_id, conn=Depends(get_db)):

    try:
        deleted = room_service.delete_room(conn = conn, room_id = room_id)
        conn.commit()
        deleted["error"] = None
        return deleted
    except Exception as e:
        return {
            "status" : "failed",
            "result" : False,
            "error" : traceback.format_exc(),
            "message" : str(e)
        }


@router.get("/get-room-by-id/{id}")
def get_room_by_id(id:int, conn=Depends(get_db)):

    try:
        room = room_service.find_room_by_id(conn= conn, id=id)
        if not room:
            return {
                "status" : "failed",
                "result" : room,
                "error" : None,
                "message" : f"Room not found with the given id: {id}"
            }
        
        return {
            "status" : "success",
            "result" : room,
            "error" : None,
            "message" : f"Room found successfully"
        }
    except Exception as e:
        return {
            "status" : "failed",
            "result" : [],
            "error" : traceback.format_exc(),
            "message" : str(e)
        }


@router.post("/fetch-rooms-to-book")
def fetch_rooms2book(available_rooms:RoomAvailability, conn = Depends(get_db)):
    y = room_service.fetch_rooms2book(conn=conn,
                                         check_in=available_rooms.check_in,
                                         check_out=available_rooms.check_out,
                                         capacity=available_rooms.capacity,
                                         room_type_id=available_rooms.room_type_id)
    print(y)
    return y