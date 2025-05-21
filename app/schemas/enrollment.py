from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 選課操作模式
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

# 取消選課操作模式
class EnrollmentDelete(BaseModel):
    student_id: int
    course_id: int

# 選課響應模式
class Enrollment(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: datetime
    is_active: bool

    class Config:
        orm_mode = True 