from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 基本學生模式
class StudentBase(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool = True

# 創建學生時使用的模式
class StudentCreate(StudentBase):
    pass

# 更新學生時使用的模式
class StudentUpdate(BaseModel):
    student_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

# API響應中使用的學生模式
class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 