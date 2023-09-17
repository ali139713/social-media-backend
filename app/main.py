from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
     db= SessionLocal()
     try:
          yield db
     finally:
          db.close()

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
while True:

    try:
         conn = psycopg2.connect(host='localhost', database='social_media_db', user='postgres', password='aLi721A#dh', cursor_factory=RealDictCursor)
         cursor=conn.cursor()
         print('Database connected successfully')
         break
    except Exception as error:
         print('Connecting to database failed')
         print('Error:', error)
         time.sleep(2)


my_posts = [{"id": 1, "title": "title of post 1", "content": "content of post 1"}, {"id": 2, "title": "My Favourite Food", "content": "pizza"}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post 
        
def find_index_of_post(id):
    for i,post in enumerate(my_posts):
        if post["id"] == id:
            return i 

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts  """)
    posts = cursor.fetchall()
    return {"data":posts}


@app.get("/post/{id}")
def get_post(id: str):
     cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
     post = cursor.fetchone()
     if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
     return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
        cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
        new_post = cursor.fetchone()
        conn.commit()
        return {"data": new_post}

@app.put("/post/{id}")
def update_post(id:int, post:Post):
        cursor.execute(""" UPDATE posts SET title = %s,  content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
        updated_post  = cursor.fetchone()
        conn.commit()
        if updated_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
        return {"data": updated_post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE    FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

