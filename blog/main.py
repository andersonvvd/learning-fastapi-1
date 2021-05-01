from fastapi import FastAPI
from pydantic import BaseModel
import schemas

app = FastAPI()


@app.post("/blog")
def create(request: schemas.Blog):
    return request