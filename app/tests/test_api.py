from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app

# 創建測試數據庫
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 設置測試客戶端
client = TestClient(app)

# 測試依賴項覆寫
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    # 創建測試數據庫表
    Base.metadata.create_all(bind=engine)
    yield
    # 清理
    Base.metadata.drop_all(bind=engine)

def test_read_main(test_db):
    response = client.get("/")
    assert response.status_code == 200
    assert "歡迎使用" in response.json()["message"]

def test_create_student(test_db):
    student_data = {
        "student_id": "S001",
        "name": "測試學生",
        "email": "test@example.com",
        "phone": "1234567890"
    }
    response = client.post("/api/v1/students/", json=student_data)
    assert response.status_code == 201
    data = response.json()
    assert data["student_id"] == "S001"
    assert data["name"] == "測試學生"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_course(test_db):
    course_data = {
        "course_code": "C001",
        "title": "測試課程",
        "description": "這是一個測試課程",
        "credits": 3,
        "max_students": 30
    }
    response = client.post("/api/v1/courses/", json=course_data)
    assert response.status_code == 201
    data = response.json()
    assert data["course_code"] == "C001"
    assert data["title"] == "測試課程"
    assert data["credits"] == 3
    assert "id" in data

def test_enrollment(test_db):
    # 創建學生
    student_data = {
        "student_id": "S002",
        "name": "選課測試學生",
        "email": "enroll@example.com",
        "phone": "1234567890"
    }
    student_response = client.post("/api/v1/students/", json=student_data)
    student_id = student_response.json()["id"]
    
    # 創建課程
    course_data = {
        "course_code": "C002",
        "title": "選課測試課程",
        "description": "這是選課測試課程",
        "credits": 3,
        "max_students": 30
    }
    course_response = client.post("/api/v1/courses/", json=course_data)
    course_id = course_response.json()["id"]
    
    # 選課
    enrollment_data = {
        "student_id": student_id,
        "course_id": course_id
    }
    enrollment_response = client.post("/api/v1/enrollments/", json=enrollment_data)
    assert enrollment_response.status_code == 201
    
    # 檢查學生的選課記錄
    student_courses = client.get(f"/api/v1/enrollments/students/{student_id}/courses")
    assert student_courses.status_code == 200
    assert len(student_courses.json()) == 1
    assert student_courses.json()[0]["course_id"] == course_id 