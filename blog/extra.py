@app.delete("/blog/{id}", status=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.blog.id == id).delete(synchronize_session=False)
    return "done"