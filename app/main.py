from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

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
    postIndex = find_index_of_post(id)
    if postIndex == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    print(postIndex)
    post_dict = dict(post)
    post_dict["id"] = id
    my_posts[postIndex] = post_dict
    return {"data": post_dict}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    postIndex = find_index_of_post(id)
    if postIndex == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    print(postIndex)
    my_posts.pop(postIndex)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

