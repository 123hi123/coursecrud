from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 基本課程模式
class CourseBase(BaseModel):
    course_code: str
    title: str
    description: Optional[str] = None
    credits: int
    max_students: int
    is_active: bool = True

# 創建課程時使用的模式
class CourseCreate(CourseBase):
    pass

# 更新課程時使用的模式
class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    max_students: Optional[int] = None
    is_active: Optional[bool] = None

# API響應中使用的課程模式
class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    } 