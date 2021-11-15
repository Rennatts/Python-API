from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


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
    
    
@app.get("/")
def root(): 
    return {"message": "hello world"}


@app.get("/posts", response_model= List[schemas.PostResponse])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    

''' @app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts} '''


@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


''' @app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published))
    
    new_post= cursor.fetchone()
    
    conn.commit();
    
    return {"data": new_post} '''


@app.get("/posts/lastest")
def get_lastest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at desc""")
    post = cursor.fetchone()
    return post



@app.get("/posts/{id}", response_model= schemas.PostResponse)
def get_post(id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail ="post not found")
    
    return post


''' @app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts where id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail ="post not found")
    return{"post_detail": post} '''



@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first()  == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with this id do not exist")
    
    post.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


''' @app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id = %s returning *""", (str(id)))
    post = cursor.fetchone()
    conn.commit();
    
    if post  == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with this id do not exist")
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)
 '''
 
 
@app.put("/posts/{id}", response_model= schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)  
    
    post = post_query.first() 
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id {id} does not exist")
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
        
    return post_query.first()



''' @app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING *""",
    (post.title, post.content, post.published, str(id)))
    
    post = cursor.fetchone()
    conn.commit()
    print(post)
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id {id} does not exist")
        
    return {'data':  post} '''
    