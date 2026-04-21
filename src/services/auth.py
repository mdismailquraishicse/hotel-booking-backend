import jwt
import bcrypt
import datetime
from src.db.auth import AuthDB
from fastapi import HTTPException


auth_db = AuthDB()

class AuthService:

    def __init__(self):
        self.salt = "salt"
        self.encryption_algorithm = "HS256"


    def password_encrypt(self, password:str):
        if not password:
            print(f"password is None: {password}")
            return
        password = password.encode("utf-8")
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        print(f"password encrypted successfully")
        print(f"password hash: {password_hash}")
        return password_hash.decode("utf-8") # always store str = decode utf-8


    def password_validate(self, password, password_hash):

        password = password.encode("utf-8")
        password_hash = password_hash.strip().encode("utf-8")
        validation = bcrypt.checkpw(password, password_hash)
        if not validation:
            print("invalid credentials")
            return False
        print(f"validation: {validation}")
        return validation
    

    def register_user(self, conn, user):

        try:
            user.password = self.password_encrypt(user.password)
            reg_response = auth_db.register_user(conn=conn, user=user)
            print(f"reg_response: {reg_response}")
            conn.commit()
            return reg_response
        except Exception as e:
            print(f"Unknown exception occured: {e}")
            if conn:
                conn.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Registration failed: {str(e)}"
            )


    def generate_token(self, payload):

        if not payload:
            print(f"payload not found: {payload}")
            return

        token = jwt.encode(payload=payload,
                           key=self.salt,
                           algorithm=self.encryption_algorithm)

        print("token generated successfully")
        return token


    def login(self, conn, creds):

        try:
            fetch_creds = auth_db.fetch_user_creds(conn=conn, email=creds.email)
            if not fetch_creds:
                return {
                    "status": "failed",
                    "result": "",
                    "message": "User not found"
                }

            hashed_pass = fetch_creds[2]
            authenticated = self.password_validate(creds.password, hashed_pass)
            if not authenticated:
                return {
                    "status" : "failed",
                    "result" : "",
                    "message" : "Invalid credentials"
                }
            
            payload = {
                "user_id": fetch_creds[0],
                "email": creds.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
            }

            token = self.generate_token(payload=payload)
            return {
                "status" : "success",
                "result" : token,
                "message" : "Login successful"
            }
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Login failed: {str(e)}"
            )
