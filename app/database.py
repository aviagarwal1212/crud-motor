import motor.motor_asyncio

from .config import settings

MONGO_DETAILS = settings.database_url
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.students.get_collection("students_collection")


# helper
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course": student["course"],
        "year": student["year"],
        "gpa": student["gpa"],
    }
