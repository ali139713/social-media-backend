from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":"These are your posts"}

@app.post("/createpost")
def create_post(post: Post):
    print(post)
    return {"data": dict(post)}