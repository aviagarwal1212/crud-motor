from typing import List

from app.database import db, student_helper
from app.models.student import OutStudent, Student, UpdateStudent
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[OutStudent])
async def get_students():
    students = [student_helper(student) async for student in db.find()]
    return students


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OutStudent)
async def create_students(student_data: Student):
    student_data = jsonable_encoder(student_data)
    student = await db.insert_one(student_data)
    new_student = await db.find_one({"_id": student.inserted_id})
    new_student = student_helper(new_student)
    return new_student


@router.get("/{id}", response_model=OutStudent)
async def get_student(id: str):
    student = await db.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"student with id {id} not found"
        )
    student = student_helper(student)
    return student


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(id: str):
    student = await db.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"student with id {id} not found"
        )
    _ = await db.delete_one({"_id": ObjectId(id)})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=OutStudent)
async def update_student(id: str, updated_student_data: UpdateStudent):
    student = await db.find_one({"_id": ObjectId(id)})
    updated_student_data = jsonable_encoder(updated_student_data)
    if not student:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"student with id {id} not found"
        )
    _ = await db.update_one({"_id": ObjectId(id)}, {"$set": updated_student_data})
    updated_student = await db.find_one({"_id": ObjectId(id)})
    updated_student = student_helper(updated_student)
    return updated_student
