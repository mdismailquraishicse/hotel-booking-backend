from src.db.bookings import BookingDB
from src.db.rooms import RoomsDB

booking_db = BookingDB()
rooms_db = RoomsDB()

class BookingService:




    def __init__(self):
        pass


    def book(self, user_id, conn, booking):
        available_rooms = rooms_db.fetch_rooms2book(conn=conn,
                                  check_in=booking.check_in,
                                  check_out=booking.check_out,
                                  capacity=booking.guests,
                                  room_type_id=booking.room_type_id)
        print(f"available rooms: {available_rooms}")
        if not available_rooms:
            return {
                "result": "",
                "message": "Room not available"
            }
        
        room_id = available_rooms[0].get("id")
        booking_response = booking_db.book(user_id = user_id,
                             room_id = room_id,
                             conn=conn, booking=booking)
        return {
                "result": booking_response.get("id"),
                "message": "Room booked successfully"
            }


    def fetch_bookings(self, conn):

        booking_data = booking_db.fetch_bookings(conn=conn)
        return booking_data
    

    def delete_booking(self, booking_id, conn):
        
        return booking_db.delete_booking(conn = conn, booking_id = booking_id)
    

    def fetch_available_rooms(self, conn, check_in, check_out, capacity):

        return booking_db.fetch_available_room(conn=conn, check_in=check_in, check_out=check_out, capacity=capacity)