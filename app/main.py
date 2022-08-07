from fastapi import FastAPI

from .routers import student

app = FastAPI()

app.include_router(student.router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to my API."}
