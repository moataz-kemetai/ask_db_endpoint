from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Egypt API", description="Simple API responding with تحيا مصر")

class TaskInput(BaseModel):
    query: str

class TaskResponse(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "تحيا مصر"}

@app.post("/ask_db")
async def process_task(task: TaskInput):
    return TaskResponse(message="تحيا مصر")

@app.get("/task")
async def get_task():
    return {"message": "تحيا مصر"}

# To run locally: uvicorn main:app --reload