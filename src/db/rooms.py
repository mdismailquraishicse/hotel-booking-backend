from psycopg2.extras import RealDictCursor



class RoomsDB:

    def __init__(self):
        pass


    def create_room(self, conn, room):
        
        query = """
            INSERT INTO rooms (room_no, room_type_id, status)
            VALUES (%s, %s, %s)
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (room.room_no, room.room_type_id, room.status))
            return True
        

    def delete_room(self, conn, room_id):

        query = """
            DELETE
            FROM rooms
            WHERE id = %s
        """

        with conn.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query, (room_id,))
            print(f"rowcount: {cursor.rowcount}")
            if cursor.rowcount == 0:
                return {
                    "status" : "failed",
                    "result" : False,
                    "message" : f"No room found with room_id: {room_id}"
                }
            return {
                    "status" : "success",
                    "result" : True,
                    "message" : "Room deleted successfully"
                }


    def fetch_available_rooms(self, conn, check_in=None, check_out=None, capacity=None):

        query = """
        SELECT
        rt.id AS room_type_id, rt.image, rt.type_name AS room_type, rt.price, rt.capacity, rt.amenities, rt.descriptions
        FROM room_type rt
        WHERE 1=1
        """

        params = []

        if capacity:
            query += " AND rt.capacity >= %s"
            params.append(capacity)

        if check_in and check_out:
            query += """
            AND rt.id NOT IN (
                SELECT b.room_id
                FROM bookings b
                WHERE NOT (
                    b.check_out <= %s OR b.check_in >= %s
                )
            )
            """
            params.extend([check_in, check_out])

        query += " ORDER BY rt.id, rt.type_name, rt.price ASC"

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            data = cursor.fetchall()
            cursor.close()
            return data
        

    def find_room_by_id(self, conn, id):

        query = """
            SELECT *
            FROM rooms
            WHERE id = %s
        """
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id,))
            room = cursor.fetchone()
            return room
        

    def fetch_rooms2book(self, conn, check_in, check_out, capacity, room_type_id):


        query = """
            SELECT
                r.id,
                r.room_no,
                rt.type_name AS room_type
            FROM rooms r
            JOIN room_type rt
                ON r.room_type_id = rt.id
                AND rt.capacity >= %s
                AND rt.id = %s
            LEFT JOIN bookings b
                ON b.room_id = r.id
                AND b.check_in < %s
                AND b.check_out > %s
            WHERE b.id IS NULL
        """

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (capacity, room_type_id, check_out, check_in,))
            data = cursor.fetchall()
            data = [dict(row) for row in data]
            print(f"data: {data}")
            return data

