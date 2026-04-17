import jwt
import bcrypt
from functools import wraps
from fastapi import HTTPException, Request


class Authentication:

    def __init__(self):
        self.salt = "salt"
        self.encryption_algorithm = "HS256"

    def password_encrypt(self, password:str):
        if not password:
            print(f"password is None: {password}")
            return
        password = password.encode("utf-8")
        password_hash = bcrypt.hashpw(password, salt=bcrypt.gensalt())
        print(f"password encrypted successfully")
        print(f"password hash: {password_hash}")
        return password_hash
    
    def password_validate(self, password, password_hash):
        password = password.encode("utf-8")
        validation = bcrypt.checkpw(password, password_hash)
        if not validation:
            print("invalid credentials")
            return False
        print(f"validation: {validation}")
        return validation
    
    def generate_token(self, payload):
        if not payload:
            print(f"payload not found: {payload}")
            return

        token = jwt.encode(payload=payload,
                           key=self.salt,
                           algorithm=self.encryption_algorithm)

        print("token generated successfully")
        print(f"token: {token}")
        return token

# Decorator to validate token
def token_required(func):
    @wraps(func)
    def token_validator(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="request missing")
        token = request.headers.get("Authorization").split(" ")[-1]
        if not token:
            raise HTTPException(status_code=401, detail="token missing")
        payload = jwt.decode(token, key="salt", algorithms="HS256")
        print("token decoded successfully")
        print(f"payload: {payload}")
        return func(*args, **kwargs)
    return token_validator

if __name__ == "__main__":
    authen = Authentication()
    password_hash = authen.password_encrypt("password")
    authen.password_validate(password="password", password_hash=password_hash)
    authen.generate_token(payload={"name":"Vijay Deenanath Chauhan"})