from src.db.bookings import BookingDB

booking_db = BookingDB()

class BookingService:




    def __init__(self):
        pass


    def book(self, conn, booking):
        booking_db.book(conn=conn, booking=booking)
        return True


    def fetch_bookings(self, conn):

        booking_data = booking_db.fetch_bookings(conn=conn)
        return booking_data
    

    def delete_booking(self, booking_id, conn):
        
        return booking_db.delete_booking(conn = conn, booking_id = booking_id)