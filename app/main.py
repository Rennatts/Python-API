from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


try:
    conn = psycopg2.connect(host ='localhost', database='fastapi', user='postgres', password='zoeylina_11',
    cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was successfully created!")
except Exception as error:
    print("connecting to database failed")
    print("Error: ", error)
    
 
 
app.include_router(post.router)   
app.include_router(user.router)  
app.include_router(auth.router)  


@app.get("/")
def root(): 
    return {"message": "hello world"}


   