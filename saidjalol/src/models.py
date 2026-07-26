import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserRole(str, enum.Enum):
    teacher = "teacher"
    admin = "admin"


class LessonStatus(str, enum.Enum):
    new = "new"
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(32))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), index=True)

    lesson_requests: Mapped[list["LessonRequest"]] = relationship(back_populates="teacher")


class LessonRequest(Base):
    __tablename__ = "lesson_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(32))
    status: Mapped[LessonStatus] = mapped_column(Enum(LessonStatus), default=LessonStatus.new, index=True)
    lesson_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    teacher: Mapped[User | None] = relationship(back_populates="lesson_requests")
