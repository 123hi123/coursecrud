import logging
from sqlalchemy.orm import Session
from datetime import datetime
import random

from app.db.database import SessionLocal
from app.models.models import Student, Course

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 示例學生數據
SAMPLE_STUDENTS = [
    {"student_id": "S1001", "name": "王小明", "email": "wang@example.com", "phone": "1234567890"},
    {"student_id": "S1002", "name": "李小華", "email": "lee@example.com", "phone": "1234567891"},
    {"student_id": "S1003", "name": "張三", "email": "zhang@example.com", "phone": "1234567892"},
    {"student_id": "S1004", "name": "劉四", "email": "liu@example.com", "phone": "1234567893"},
    {"student_id": "S1005", "name": "陳五", "email": "chen@example.com", "phone": "1234567894"},
]

# 示例課程數據
SAMPLE_COURSES = [
    {"course_code": "CS101", "title": "計算機導論", "description": "計算機科學基礎課程", "credits": 3, "max_students": 30},
    {"course_code": "CS201", "title": "數據結構", "description": "基本數據結構與算法", "credits": 4, "max_students": 25},
    {"course_code": "CS301", "title": "數據庫系統", "description": "關係數據庫理論與實踐", "credits": 4, "max_students": 20},
    {"course_code": "CS401", "title": "人工智能", "description": "AI基礎與應用", "credits": 3, "max_students": 15},
    {"course_code": "CS501", "title": "軟件工程", "description": "軟件開發方法與實踐", "credits": 4, "max_students": 20},
]

def seed_db():
    """
    向數據庫中填充示例數據，並建立關係
    """
    db = SessionLocal()
    try:
        # 檢查是否已有數據
        student_count = db.query(Student).count()
        course_count = db.query(Course).count()
        
        # 如果已有數據，詢問是否清空
        if student_count > 0 or course_count > 0:
            logger.info(f"數據庫已有 {student_count} 個學生和 {course_count} 門課程")
            logger.info("跳過數據添加。如需重新添加，請先清空數據")
            return
        
        # 創建學生
        students = []
        logger.info("創建示例學生...")
        for student_data in SAMPLE_STUDENTS:
            student = Student(
                student_id=student_data["student_id"],
                name=student_data["name"],
                email=student_data["email"],
                phone=student_data["phone"],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True
            )
            db.add(student)
            students.append(student)
        
        # 創建課程
        courses = []
        logger.info("創建示例課程...")
        for course_data in SAMPLE_COURSES:
            course = Course(
                course_code=course_data["course_code"],
                title=course_data["title"],
                description=course_data["description"],
                credits=course_data["credits"],
                max_students=course_data["max_students"],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True
            )
            db.add(course)
            courses.append(course)
        
        # 提交變更以獲取ID
        db.commit()
        
        # 隨機創建選課關係
        logger.info("創建選課關係...")
        for student in students:
            # 每個學生選擇2-4門課程
            num_courses = random.randint(2, 4)
            chosen_courses = random.sample(courses, num_courses)
            
            for course in chosen_courses:
                student.courses.append(course)
                logger.info(f"學生 {student.name} 選修了 {course.title}")
        
        # 提交所有變更
        db.commit()
        logger.info("示例數據創建完成！")
        
        # 顯示關係摘要
        logger.info("\n關係數據庫摘要:")
        for student in db.query(Student).all():
            course_list = ", ".join([c.title for c in student.courses])
            logger.info(f"學生: {student.name} (ID: {student.id}, 學號: {student.student_id})")
            logger.info(f"  選修課程: {course_list}")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_db() 