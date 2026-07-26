from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.database import Base, engine
from src.dependencies import get_db, get_current_user, require_role
from src.models import LessonRequest, LessonStatus, User, UserRole
from src.schemas import (
    AdminLessonRequestItem,
    AdminLessonRequestListResponse,
    LessonRequestCreate,
    LessonRequestPublicResponse,
    ScheduleLessonRequest,
    ScheduleLessonResponse,
    TeacherLessonItem,
    TeacherLessonListResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from src.security import create_access_token, hash_password, verify_password


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Lesson Request Service",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "users", "description": "Authentication and profile endpoints for teachers and admins."},
        {"name": "students", "description": "Public endpoint for students to submit lesson requests."},
        {"name": "teachers", "description": "Endpoints available only to teachers."},
        {"name": "admin", "description": "Administrative endpoints for managing lesson requests."},
    ],
)


@app.post("/v1/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> User:
    existing_user = db.scalar(select(User).where(User.email == payload.email))
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")

    user = User(
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone_number=payload.phone_number,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/v1/users/login", response_model=TokenResponse, tags=["users"])
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(str(user.id))
    return TokenResponse(access_token=access_token)


@app.get("/v1/users/me", response_model=UserResponse, tags=["users"])
def get_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@app.post(
    "/v1/lesson-requests",
    response_model=LessonRequestPublicResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["students"],
)
def create_lesson_request(payload: LessonRequestCreate, db: Session = Depends(get_db)) -> LessonRequest:
    lesson_request = LessonRequest(
        first_name=payload.first_name,
        phone_number=payload.phone_number,
        status=LessonStatus.new,
    )
    db.add(lesson_request)
    db.commit()
    db.refresh(lesson_request)
    return lesson_request


@app.get("/v1/teacher/my-lessons", response_model=TeacherLessonListResponse, tags=["teachers"])
def get_my_lessons(
    current_user: User = Depends(require_role(UserRole.teacher)),
    db: Session = Depends(get_db),
) -> TeacherLessonListResponse:
    lesson_requests = db.scalars(
        select(LessonRequest)
        .where(LessonRequest.teacher_id == current_user.id)
        .order_by(LessonRequest.lesson_time.is_(None), LessonRequest.lesson_time, LessonRequest.id)
    ).all()

    return TeacherLessonListResponse(
        lessons=[
            TeacherLessonItem(
                id=lesson.id,
                status=lesson.status,
                lesson_time=lesson.lesson_time,
                student={"first_name": lesson.first_name, "phone_number": lesson.phone_number},
            )
            for lesson in lesson_requests
        ]
    )


@app.get("/v1/admin/lesson-requests", response_model=AdminLessonRequestListResponse, tags=["admin"])
def get_all_lesson_requests(
    _: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
) -> AdminLessonRequestListResponse:
    lesson_requests = db.scalars(
        select(LessonRequest)
        .options(joinedload(LessonRequest.teacher))
        .order_by(LessonRequest.created_at.desc(), LessonRequest.id.desc())
    ).all()

    return AdminLessonRequestListResponse(
        lesson_requests=[
            AdminLessonRequestItem(
                id=lesson.id,
                first_name=lesson.first_name,
                phone_number=lesson.phone_number,
                status=lesson.status,
                lesson_time=lesson.lesson_time,
                teacher=lesson.teacher,
                created_at=lesson.created_at,
            )
            for lesson in lesson_requests
        ]
    )


@app.patch(
    "/v1/admin/lesson-requests/{lesson_request_id}/schedule",
    response_model=ScheduleLessonResponse,
    tags=["admin"],
)
def schedule_lesson(
    lesson_request_id: int,
    payload: ScheduleLessonRequest,
    _: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
) -> LessonRequest:
    lesson_request = db.get(LessonRequest, lesson_request_id)
    if lesson_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson request not found")

    teacher = db.get(User, payload.teacher_id)
    if teacher is None or teacher.role != UserRole.teacher:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher not found")

    lesson_request.teacher_id = teacher.id
    lesson_request.lesson_time = payload.lesson_time
    lesson_request.status = LessonStatus.scheduled
    db.commit()
    db.refresh(lesson_request)
    return lesson_request
