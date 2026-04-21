from psycopg2.extras import RealDictCursor




class BookingDB:
     
    def __init__(self):
        pass
        

    def book(self, conn, booking):

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                INSERT INTO bookings (user_id, room_id, check_in, check_out, guests, price, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (booking.user_id,
                    booking.room_id,
                    booking.check_in,
                    booking.check_out,
                    booking.guests,
                    booking.price,
                    booking.status)

            with conn.cursor() as cursor:
                cursor.execute(query, values)
            
        
    def delete_booking(self, conn, booking_id):

        query = """
            DELETE
            FROM bookings
            WHERE id = %s
        """

        with conn.cursor() as cursor:
            cursor.execute(query, (booking_id,))
            print(f"rowcount: {cursor.rowcount}")
            if cursor.rowcount == 0:
                return {
                    "status" : "failed",
                    "result" : False,
                    "message" : f"No booking found with booking_id: {booking_id}"
                }
            return {
                    "status" : "success",
                    "result" : True,
                    "message" : "Booking deleted successfully"
                }
    

    def fetch_bookings(self, conn):

        query = """
            SELECT
                r.room_no, b.id, b.room_id, rt.type_name as room_type, b.check_in, b.check_out, b.guests, b.price, b.status
            FROM bookings b
            LEFT JOIN rooms r ON b.room_id = r.id
            LEFT JOIN room_type rt ON r.room_type_id = rt.id
            ORDER BY b.created_at DESC;
        """

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        data = [dict(row) for row in data]
        return data
    