from fastapi import APIRouter

from app.api.endpoints import students, courses, enrollments
from app.core.config import API_V1_STR

api_router = APIRouter()

# 子路由
api_router.include_router(students.router, prefix="/students", tags=["學生管理"])
api_router.include_router(courses.router, prefix="/courses", tags=["課程管理"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["選課管理"]) 