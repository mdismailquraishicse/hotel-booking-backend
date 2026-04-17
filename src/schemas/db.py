import psycopg2 as pg
from src.models.pydantic_models import User, Room, Bookings

def get_connection():
    creds = {
        "host": "db",
        "database": "hotel_db",
        "user": "user",
        "password": "password",
        "port": 5432
    }
    
    conn = pg.connect(**creds)
    return conn

def register_user(conn, user:User):
    cursor = conn.cursor()
    query = f"""
        INSERT INTO users (name, gender, email, password)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (user.name, user.gender, user.email, user.password))
    conn.commit()
    conn.close()

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

def search_available_rooms(conn, check_in=None, check_out=None, capacity=None):
    query = """
        SELECT DISTINCT ON (r.room_type)
        r.room_id, r.image, r.room_type, r.price, r.capacity, r.amenities
        FROM rooms r
        WHERE 1=1
    """

    params = []

    # 🔹 Filter by capacity
    if capacity:
        query += " AND r.capacity >= %s"
        params.append(capacity)

    # 🔹 Filter by availability (VERY IMPORTANT)
    if check_in and check_out:
        query += """
        AND r.room_id NOT IN (
            SELECT b.room_id
            FROM bookings b
            WHERE NOT (
                b.check_out <= %s OR b.check_in >= %s
            )
        )
        """
        params.extend([check_in, check_out])

    # 🔹 Order for DISTINCT ON (required in PostgreSQL)
    query += " ORDER BY r.room_type, r.price ASC"

    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    return data