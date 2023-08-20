from random import randrange
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"id": 1, "title": "title of post 1", "content": "content of post 1"}, {"id": 2, "title": "My Favourite Food", "content": "pizza"}]

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/createpost")
def create_post(post: Post):
    post_dict = dict(post)
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)    
    return {"data": post_dict}

@app.get("/post/{id}")
def get_post(id):
    print(id)
    return {"data": f"Here is the post with id {id}"}