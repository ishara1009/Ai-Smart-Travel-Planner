from fastapi import APIRouter

from app.api.v1.endpoints import auth, feedback, health, planner, trips, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(trips.router)
api_router.include_router(planner.router)
api_router.include_router(feedback.router)
api_router.include_router(health.router)
