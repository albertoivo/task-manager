from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Task Manager API running..."}
