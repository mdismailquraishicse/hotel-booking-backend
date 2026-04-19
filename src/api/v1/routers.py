from fastapi import APIRouter

# Import all endpoint routers
from src.api.v1.endpoints import auth, bookings, rooms

# Create main router for v1
api_router = APIRouter()

# Include individual route modules
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

# Include individual route modules
api_router.include_router(
    bookings.router,
    prefix="/bookings",
    tags=["Bookings"]
)

# Include individual route modules
api_router.include_router(
    rooms.router,
    prefix="/rooms",
    tags=["Rooms"]
)