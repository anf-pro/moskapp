from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
from psycopg2.extras import RealDictCursor
import time
from .. import models, database, schemas,utils
from ..database import engine
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(prefix="/users", tags=["users"])

@router.post("/",status_code=201, response_model=schemas.UserCreateConfirm)
def create_user(user: schemas.CreateUser, db: Session = Depends(database.get_db,)):
    hashed_password=utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    #خذ البيانات من الشيما وضعها في الموديل لارسالها لقاعدة البيانات
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="المستخدم غير موجود")

    return user
