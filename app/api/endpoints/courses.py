from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List

from app.api import deps
from app.models.models import Course
from app.schemas.course import CourseCreate, CourseUpdate, Course as CourseSchema

router = APIRouter()

@router.post("/", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    創建新課程
    """
    # 檢查課程代碼是否已存在
    db_course = db.query(Course).filter(Course.course_code == course_in.course_code).first()
    if db_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="該課程代碼已存在"
        )
    
    # 創建新課程
    db_course = Course(
        course_code=course_in.course_code,
        title=course_in.title,
        description=course_in.description,
        credits=course_in.credits,
        max_students=course_in.max_students,
        is_active=course_in.is_active
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=List[CourseSchema])
def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    獲取所有課程
    """
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.get("/{course_id}", response_model=CourseSchema)
def read_course(
    course_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    根據ID獲取課程
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該課程"
        )
    return course

@router.put("/{course_id}", response_model=CourseSchema)
def update_course(
    course_id: int,
    course_in: CourseUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    更新課程信息
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該課程"
        )
    
    # 更新字段
    update_data = course_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}", response_model=CourseSchema)
def delete_course(
    course_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    刪除課程
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該課程"
        )
    
    # 執行軟刪除
    course.is_active = False
    db.commit()
    db.refresh(course)
    return course 