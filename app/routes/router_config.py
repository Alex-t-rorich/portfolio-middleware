from fastapi import APIRouter

from app.routes import cv_routes, education_routes, experience_routes, skill_routes, user_routes, website_routes

api_router = APIRouter()

api_router.include_router(cv_routes.router)
api_router.include_router(education_routes.router)
api_router.include_router(experience_routes.router)
api_router.include_router(skill_routes.router)
api_router.include_router(user_routes.router)
api_router.include_router(website_routes.router)
