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
        r.id AS room_id, r.image, r.type_name AS room_type, r.price, r.capacity, r.amenities, r.descriptions
        FROM room_type r
        WHERE 1=1
        """

        params = []

        if capacity:
            query += " AND r.capacity >= %s"
            params.append(capacity)

        if check_in and check_out:
            query += """
            AND r.id NOT IN (
                SELECT b.room_id
                FROM bookings b
                WHERE NOT (
                    b.check_out <= %s OR b.check_in >= %s
                )
            )
            """
            params.extend([check_in, check_out])

        query += " ORDER BY r.id, r.type_name, r.price ASC"

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

