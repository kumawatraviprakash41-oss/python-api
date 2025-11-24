from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Python API Online Working!"}

@app.get("/hello")
def hello():
    return {"status": "success", "message": "Hello from Python API!"}

@app.get("/user")
def user():
    return {
        "name": "Ravi Kumar",
        "age": 25,
        "status": "active"
    }
}
