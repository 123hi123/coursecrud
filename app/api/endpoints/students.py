from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List

from app.api import deps
from app.models.models import Student
from app.schemas.student import StudentCreate, StudentUpdate, Student as StudentSchema

router = APIRouter()

@router.post("/", response_model=StudentSchema, status_code=status.HTTP_201_CREATED)
def create_student(
    student_in: StudentCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    創建新學生
    """
    # 檢查學號是否已存在
    db_student = db.query(Student).filter(Student.student_id == student_in.student_id).first()
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="該學號已存在"
        )
    
    # 檢查郵箱是否已存在
    db_student = db.query(Student).filter(Student.email == student_in.email).first()
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="該郵箱已存在"
        )
    
    # 創建新學生
    db_student = Student(
        student_id=student_in.student_id,
        name=student_in.name,
        email=student_in.email,
        phone=student_in.phone,
        is_active=student_in.is_active
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/", response_model=List[StudentSchema])
def read_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    獲取所有學生
    """
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

@router.get("/{student_id}", response_model=StudentSchema)
def read_student(
    student_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    根據ID獲取學生
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該學生"
        )
    return student

@router.put("/{student_id}", response_model=StudentSchema)
def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    更新學生信息
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該學生"
        )
    
    # 更新字段
    update_data = student_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}", response_model=StudentSchema)
def delete_student(
    student_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    刪除學生
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該學生"
        )
    
    # 執行軟刪除
    student.is_active = False
    db.commit()
    db.refresh(student)
    return student 