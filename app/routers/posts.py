
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
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from typing import List
from .. import oauth2

router = APIRouter(prefix="/posts",tags=["Posts"])


#Get all posts
@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(
    db: Session = Depends(database.get_db),
    limit: int = 4,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).filter(
        models.Post.title.contains(search)
    ).group_by(
        models.Post.id
    ).limit(limit).offset(skip).all()

    return posts

#Create post
@router.post("/", status_code=201, response_model = schemas.Confirm)
def Create_post(post: schemas.CreatePost, db: Session = Depends(database.get_db,), 
                 current_user:int = Depends(oauth2.get_current_user)):
        print(current_user.email)
        new_post = models.Post(owner_id=current_user.id,**post.model_dump())

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post




@router.get("/{id}",response_model=schemas.PostWithVotes)
def get_post(id: int, db: Session = Depends(database.get_db),
             current_user:int = Depends(oauth2.get_current_user)):
    # Use SQLAlchemy ORM to query the post by id
    post_with_votes = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).filter(
        models.Post.id == id
    ).group_by(
        models.Post.id
    ).first()

    if not post_with_votes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post_with_votes


#Update post
@router.patch("/{id}",response_model=schemas.Confirm)
def edit_post(id: int, post: schemas.CreatePost, db: Session = Depends(database.get_db),
              current_user:int = Depends(oauth2.get_current_user)):
    # العثور على المنشور في قاعدة البيانات
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if existing_post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                             detail=f"not your post")

    # تحديث الحقول فقط إذا كانت موجودة
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published

    db.commit()  # تنفيذ التحديث
    db.refresh(existing_post)  # تحديث الكائن بعد التحديث

    return existing_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db),
                current_user:int = Depends(oauth2.get_current_user)):  # Using the database session here
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()

    if post_to_delete is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post_to_delete.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                             detail=f"not your post")

    db.delete(post_to_delete)
    db.commit()
    
    return {"message": "Deleted successfully"}
