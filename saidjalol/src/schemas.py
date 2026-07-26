from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from src.models import LessonStatus, UserRole


class UserRegisterRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LessonRequestCreate(BaseModel):
    first_name: str
    phone_number: str


class LessonRequestPublicResponse(BaseModel):
    id: int
    first_name: str
    phone_number: str
    status: LessonStatus
    lesson_time: datetime | None
    teacher_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentInfo(BaseModel):
    first_name: str
    phone_number: str


class TeacherLessonItem(BaseModel):
    id: int
    status: LessonStatus
    lesson_time: datetime | None
    student: StudentInfo


class TeacherLessonListResponse(BaseModel):
    lessons: list[TeacherLessonItem]


class AdminTeacherInfo(BaseModel):
    id: int
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class AdminLessonRequestItem(BaseModel):
    id: int
    first_name: str
    phone_number: str
    status: LessonStatus
    lesson_time: datetime | None
    teacher: AdminTeacherInfo | None
    created_at: datetime


class AdminLessonRequestListResponse(BaseModel):
    lesson_requests: list[AdminLessonRequestItem]


class ScheduleLessonRequest(BaseModel):
    teacher_id: int
    lesson_time: datetime


class ScheduleLessonResponse(BaseModel):
    id: int
    status: LessonStatus
    teacher_id: int
    lesson_time: datetime

    model_config = ConfigDict(from_attributes=True)
