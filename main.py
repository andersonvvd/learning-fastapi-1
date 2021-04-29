from fastapi import FastAPI


app = FastAPI()


@app.get("/blog")
def index(limit, published):
    # only get 10 published blogs
    if published:
        return {"data": f"{limit} published blogs from the database"}
    else:
        return {"data": f"{limit} blogs from the database"}
        


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}/comments")
def comments(id):
    #fetch comments of blog with id = id
    return {"data": {'1', "2" }}

