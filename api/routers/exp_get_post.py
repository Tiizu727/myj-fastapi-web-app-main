from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body
from sqlalchemy.orm import Session

import api.cruds.task as task_crud
from api.db import get_db
from api.extra_modules.auth.core import get_current_user
from api.extra_modules.image.core import save_image

router = APIRouter()


@router.get("/getone")
def get_one():
    return {"message": "Hello World"}


@router.get("/getmulti")
def get_multi():
    multi = [
        {"message": "Python"},
        {"message": "FastAPI"},
        {"message": "JavaScript"},
        {"message": "MySQL"},
    ]
    return multi

@router.post("/posttest")
def post_reply(data:dict):
    first_text = data.get("ft")
    second_text = data.get("st")
    connected_text  = first_text + second_text
    return {"reply": connected_text}
