from src.schemas.pydantic_models import User ,Room, Bookings


class AuthDB:




    def __init__(self):
        pass


    def register_user(self,conn, user:User):

        try:
            query = """
                INSERT INTO users (fullname, gender, email, password)
                VALUES (%s, %s, %s, %s)
            """

            cursor = conn.cursor()
            with conn.cursor() as cursor:
                cursor.execute(query, (user.name, user.gender, user.email, user.password))
                return True

        except Exception as e:
            print(f"DB error during registration: {e}")
            raise Exception(f"User registration failed: {str(e)}")


    def fetch_user_creds(self, conn, email:str):

        try:
            query = """
            SELECT
                id, email, password
            FROM users
            WHERE email = %s
            """

            with conn.cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Not able to fetch the creds for user: {email} {str(e)}")


def get_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return data

def get_rooms(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    return data

def add_room(conn, room:Room):
    cursor = conn.cursor()
    query = f"""
        INSERT INTO rooms (image, room_type, price, capacity, amenities)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (None, room.room_type, room.price, room.capacity, None))
    conn.commit()
    conn.close()

def booking(conn, booking:Bookings):
    cursor = conn.cursor()
    query = f"""
    INSERT INTO bookings (user_id, room_id, check_in, check_out, guests, price)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query, (1,
                booking.room_id,
                booking.check_in,
                booking.check_out,
                booking.guests,
                booking.price)
        )
    conn.commit()
    conn.close()

def get_bookings(conn):
    query = """
        SELECT r.room_id, r.room_type, b.check_in, b.check_out, b.guests, b.price
        FROM rooms r
        RIGHT JOIN bookings b
        ON r.room_id = b.room_id;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data
