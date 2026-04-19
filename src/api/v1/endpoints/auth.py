import traceback
from fastapi import APIRouter, Depends
from src.db.session import get_db
from src.schemas.pydantic_models import User, Creds
from src.services.auth import AuthService

router = APIRouter()

auth_service = AuthService()

@router.post("/register")
def register(user:User, conn = Depends(get_db)):

    try:
        registered = auth_service.register_user(user=user, conn=conn)
        if not registered:
            return {
                "status" : "failed",
                "result" : registered,
                "error" : None,
                "message" : "Service temporarily not available"
            }
        
        return {
                "status" : "success",
                "result" : registered,
                "error" : None,
                "message" : "User registered successfully"
            }
    except Exception as e:
        return {
                "status" : "success",
                "result" : False,
                "error" : traceback.format_exc(),
                "message" : str(e)
            }


@router.post("/login")
def login(creds:Creds, conn = Depends(get_db)):

    try:
        logged_in = auth_service.login(conn=conn, creds= creds)
        logged_in["error"] = None
        return logged_in
    except Exception as e:
        return {
            "status" : "failed",
            "result" : None,
            "error" : traceback.format_exc(),
            "message" : str(e)
        }
