from fastapi import APIRouter

# Import all endpoint routers
from src.api.v1.endpoints import auth, bookings, rooms, pay

# Create main router for v1
api_router = APIRouter()

# Auth
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

# Bookings
api_router.include_router(
    bookings.router,
    prefix="/bookings",
    tags=["Bookings"]
)

# Rooms
api_router.include_router(
    rooms.router,
    prefix="/rooms",
    tags=["Rooms"]
)

# Payment
api_router.include_router(
    pay.router,
    prefix="/pay",
    tags=["Payment"]
)