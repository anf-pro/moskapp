from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from pydantic.types import conint


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostBase(BaseModel):
        title: str
        content: str
        published: bool = True

class CreatePost(PostBase):
      pass

class BaseUser(BaseModel):
      email: EmailStr
      #password: str we can bring anything from User table due to owner= relationship("User")
      #which is in models.py

class Confirm (PostBase):
        id:int
        owner_id:int
        owner: BaseUser #is relatioship from another table so it has to be here as call
        
        #created_at: datetime......dont want it at the moment 
        #the rest will come from PostBase class 
class PostWithVotes(BaseModel):
    Post: Confirm   # من نفس النوع الذي تستخدمه للعرض
    votes: int

   

    model_config = {
        "from_attributes": True
    }


    
      #password: str
class CreateUser(BaseUser):#when creating user we use this as we enter the
      #email and password, so this does not bring out any data
      password: str
      

class UserCreateConfirm(BaseUser):
      created_at: datetime
      
class UserOut(BaseUser):
        id:int

class UserLogin(BaseModel):
      email:EmailStr
      password:str


class Token(BaseModel):
      access_token:str
      token_type: str

class Tokendata(BaseModel):
      id: Optional[str] = None

class Vote(BaseModel):
    post_id: int  # ID of the post the vote is associated with
    dir: int

    @field_validator('dir')
    def validate_dir(cls, value):
        if value not in (0, 1):
            raise ValueError("dir يجب أن يكون 0 أو 1 فقط")
        return value
  

      

