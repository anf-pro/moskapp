

from fastapi import FastAPI
from .config import settings
from . import models
from .database import engine

from .routers import posts, users, auoth, vote
# هذا السطر ينشئ الجداول بناءً على الموديلات



models.Base.metadata.create_all(bind=engine)




  



app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auoth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "::::::::اهلا وسهلا"}



        
 
    
