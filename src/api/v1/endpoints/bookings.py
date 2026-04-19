import traceback
from src.db.session import get_db
from fastapi import APIRouter, Depends
from src.schemas.pydantic_models import Bookings
from src.services.bookings import BookingService

router = APIRouter()
booking_service = BookingService()


@router.post("/book-now")
def bookings(booking:Bookings, conn=Depends(get_db)):
    try:
        booked = booking_service.book(booking=booking, conn=conn)
        conn.commit()
        return {
            "status" : "success",
            "result" : booked,
            "error" : None,
            "message" : "Room booked successfully"
        }
    except Exception as e:
        return {
            "status" : "failed",
            "result" : False,
            "error" : traceback.format_exc(),
            "message" : str(e)
        }


@router.get("/fetch-bookings")
def bookings(conn=Depends(get_db)):

    try:
        booking_data = booking_service.fetch_bookings(conn=conn)
        return {
            "status": "success",
            "result": booking_data,
            "error": None,
            "message": "successfully fetched data"
        }
    except Exception as e:
        return {
            "status": "failed",
            "result": [],
            "error": traceback.format_exc(),
            "message": str(e)
        }
    

@router.delete("/delete-booking/{booking_id}")
def delete_booking(booking_id, conn=Depends(get_db)):

    try:
        deleted = booking_service.delete_booking(conn = conn, booking_id = booking_id)
        conn.commit()
        deleted["error"] = None
        return None
    except Exception as e:
        return {
            "status" : "failed",
            "result" : False,
            "error" : traceback.format_exc(),
            "message" : str(e)
        }
    

@router.get("/get-bookings-by-email/{email}")
def get_booking_by_email(email:str, conn=Depends(get_db)):
    pass
