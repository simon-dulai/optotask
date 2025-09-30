from fastapi import FastAPI
from schemas import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "It works!"}