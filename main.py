from fastapi import FastAPI
import models
from database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/c_db")
def c_db():
    return "DB is created"
