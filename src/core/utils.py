import jwt
from functools import wraps
from fastapi import HTTPException, Request




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
        request.state.user_id = payload.get("user_id")
        request.state.fullname = payload.get("fullname")
        request.state.email = payload.get("email")
        request.state.mobile = payload.get("mobile")
        print("token decoded successfully")
        print(f"payload: {payload}")
        return func(*args, **kwargs)
    return token_validator