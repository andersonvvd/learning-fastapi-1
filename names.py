from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"data":{"name":"Antonio"}}

#@app -> path operation decorator
#.get -> operation
# "/path" -> path
# def function(): ...  -> path operation function