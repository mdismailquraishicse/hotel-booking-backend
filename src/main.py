from fastapi import FastAPI
from src.api.v1.routers import api_router


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {"message": "server is running..."}
