from psycopg2.extras import RealDictCursor
from src.schemas.pydantic_models import User




class AuthDB:




    def __init__(self):

        pass


    def register_user(self,conn, user:User):

        try:

            query = """
                INSERT INTO users (fullname, gender, email, password)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """

            cursor = conn.cursor()
            with conn.cursor(cursor_factory = RealDictCursor) as cursor:
                cursor.execute(query, (user.name, user.gender, user.email, user.password))
                return cursor.fetchone()

        except Exception as e:

            print(f"DB error during registration: {e}")
            raise Exception(f"User registration failed: {str(e)}")


    def fetch_user_creds(self, conn, email:str):

        try:

            query = """
            SELECT
                id, email, fullname, gender, password, mobile
            FROM users
            WHERE email = %s
            """

            with conn.cursor(cursor_factory = RealDictCursor) as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except Exception as e:

            raise Exception(f"Not able to fetch the creds for user: {email} {str(e)}")
