from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import Vote, Post, User  # تأكد من استيراد النماذج
from ..database import get_db  # تأكد من استيراد وظيفة get_db من قاعدة البيانات
from ..schemas import Vote  # تأكد من وجود schema للتصويت
from .. import database,oauth2,models
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

# مسار التصويت على منشور معين
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already voted on this post")
        
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Vote created successfully", "vote": new_vote}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}
