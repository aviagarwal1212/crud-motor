from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Student(BaseModel):
    fullname: str
    email: EmailStr
    course: str
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., gt=0.0, le=4.0)


class UpdateStudent(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    year: Optional[int]
    gpa: Optional[float]


class OutStudent(Student):
    id: str
