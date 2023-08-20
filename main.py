from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    return {"data":my_posts}


@app.get("/post/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    return {"data": post}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = dict(post)
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)    
    return {"data": post_dict}

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

