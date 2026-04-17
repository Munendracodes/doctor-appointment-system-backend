from fastapi import FastAPI
from app.redis.client import redis_client
from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
import app.db.models
from app.api.v1.doctor_routes import router as doctors_router
from app.api.v1.slot_routes import router as slot_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",
    "https://munendracodes.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/", include_in_schema=False)
async def root():
    all_redis_keys = await redis_client.keys("*")
    print(f"[DEBUG] Redis Keys: {all_redis_keys}")
    return {"message": "Welcome to the FastAPI OTP Service!"} 

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(doctors_router)
app.include_router(slot_router)




    