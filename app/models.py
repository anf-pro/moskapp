from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(String)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    owner= relationship("User")

class User(Base):
    __tablename__ = "users"   # اسم الجدول في قاعدة البيانات

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Vote (Base):
    __tablename__="votes"
  
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
