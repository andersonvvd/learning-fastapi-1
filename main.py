from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def index():
    return {"data":{"name":"Antonio"}}


@app.get("/about/")
def about():
    return {"data":{"About Page"}}


@app.get("/blog/{id}/")
def show(id: int):
    #fetch blog with id = id
    return {"data": id}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}/comments")
def comments(id):
    #fetch comments of blog with id = id
    return {"data": {'1', "2" }}

