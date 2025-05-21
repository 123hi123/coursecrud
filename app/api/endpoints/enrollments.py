from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from datetime import datetime

from app.api import deps
from app.models.models import Student, Course, enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentDelete, Enrollment as EnrollmentSchema

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment_in: EnrollmentCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    學生選課
    """
    # 檢查學生是否存在
    student = db.query(Student).filter(Student.id == enrollment_in.student_id).first()
    if not student or not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該學生或學生已停用"
        )
    
    # 檢查課程是否存在
    course = db.query(Course).filter(Course.id == enrollment_in.course_id).first()
    if not course or not course.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該課程或課程已停用"
        )
    
    # 檢查是否已選課
    for enrolled_course in student.courses:
        if enrolled_course.id == enrollment_in.course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="學生已選修該課程"
            )
    
    # 檢查課程人數是否已滿
    if len(course.students) >= course.max_students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="課程人數已滿"
        )
    
    # 選課操作
    student.courses.append(course)
    db.commit()
    
    # 組裝返回數據
    result = {
        "student_id": student.id,
        "course_id": course.id,
        "enrollment_date": datetime.now(),
        "is_active": True
    }
    
    return result

@router.get("/students/{student_id}/courses", response_model=List[EnrollmentSchema])
def read_student_enrollments(
    student_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    獲取學生選課記錄
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該學生"
        )
    
    # 獲取選課記錄
    enrollments = []
    for course in student.courses:
        # 獲取選課表中的記錄
        stmt = enrollment.select().where(
            enrollment.c.student_id == student_id,
            enrollment.c.course_id == course.id
        )
        enrollment_record = db.execute(stmt).first()
        
        enrollments.append({
            "student_id": student_id,
            "course_id": course.id,
            "enrollment_date": enrollment_record.enrollment_date,
            "is_active": enrollment_record.is_active
        })
    
    return enrollments

@router.get("/courses/{course_id}/students", response_model=List[EnrollmentSchema])
def read_course_enrollments(
    course_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    獲取課程選課記錄
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該課程"
        )
    
    # 獲取選課記錄
    enrollments = []
    for student in course.students:
        # 獲取選課表中的記錄
        stmt = enrollment.select().where(
            enrollment.c.student_id == student.id,
            enrollment.c.course_id == course_id
        )
        enrollment_record = db.execute(stmt).first()
        
        enrollments.append({
            "student_id": student.id,
            "course_id": course_id,
            "enrollment_date": enrollment_record.enrollment_date,
            "is_active": enrollment_record.is_active
        })
    
    return enrollments

@router.delete("/", status_code=status.HTTP_200_OK)
def delete_enrollment(
    enrollment_in: EnrollmentDelete,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    取消選課
    """
    # 檢查學生是否存在
    student = db.query(Student).filter(Student.id == enrollment_in.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該學生"
        )
    
    # 檢查課程是否存在
    course = db.query(Course).filter(Course.id == enrollment_in.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該課程"
        )
    
    # 檢查是否已選課
    is_enrolled = False
    for enrolled_course in student.courses:
        if enrolled_course.id == enrollment_in.course_id:
            is_enrolled = True
            break
    
    if not is_enrolled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="學生未選修該課程"
        )
    
    # 刪除選課記錄
    student.courses.remove(course)
    db.commit()
    
    return {"status": "success", "message": "已取消選課"} 