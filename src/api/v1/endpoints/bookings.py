import traceback
from fastapi import APIRouter, Depends, Request
from src.db.session import get_db
from src.core.utils import token_required
from src.schemas.pydantic_models import Bookings
from src.services.bookings import BookingService

router = APIRouter()
booking_service = BookingService()


@router.post("/book-now")
@token_required
def bookings(request:Request, booking:Bookings, conn=Depends(get_db)):

    try:
        booked = booking_service.book(
            user_id = request.state.user_id,
            booking = booking,
            conn = conn)
        conn.commit()
        return {
            "status" : "success",
            "result" : booked.get("result"),
            "error" : None,
            "message" : booked.get("message")
        }
    except Exception as e:
        print(f"error: {e}")
        return {
            "status" : "failed",
            "result" : "",
            "error" : traceback.format_exc(),
            "message" : str(e)
        }


@router.get("/fetch-bookings")
@token_required
def bookings(request:Request, conn=Depends(get_db)):

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
@token_required
def delete_booking(request:Request, booking_id, conn=Depends(get_db)):

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
@token_required
def get_booking_by_email(request:Request, email:str, conn=Depends(get_db)):
    pass


@router.get("/update-status")
def update_status(conn = Depends(get_db)):

    try:
        result = booking_service.update_booking_status(conn=conn)
        conn.commit()
        return result
    except Exception as e:

        print(f"exception: {e}")
