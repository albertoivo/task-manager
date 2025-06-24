from fastapi import FastAPI

app = FastAPI(prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Task Manager API running..."}
