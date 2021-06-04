from fastapi.testclient import TestClient
from blog.tests.utils import builder_blog
from blog.main import app, get_db
from blog.database import Base
from blog.models import Blog
from blog.tests.database import TestingSessionLocal, engine
from blog.tests.schemas import BlogFaker

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        return db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_post_blog():
    faker_blog = builder_blog.generate_blog()

    response = client.post("/blog", json=faker_blog.dict())

    blog_result = response.json()

    assert response.status_code == 201
    assert faker_blog.title == blog_result['title']
    assert faker_blog.body == blog_result['body']


def test_get_blog():
    test_db = override_get_db()

    faker_blog = builder_blog.generate_blog()

    blog = Blog(title=faker_blog.title, body=faker_blog.body, user_id=1)
    test_db.add(blog)
    test_db.commit()
    test_db.refresh(blog)

    response = client.get(f"/blog/{blog.id}")
    blog_result = response.json()

    assert response.status_code == 200
    assert faker_blog.title == blog_result['title']
    assert faker_blog.body == blog_result['body']


def test_delete_blog():
    test_db = override_get_db()

    faker_blog = builder_blog.generate_blog()

    blog = Blog(title=faker_blog.title, body=faker_blog.body, user_id=1)
    test_db.add(blog)
    test_db.commit()
    test_db.refresh(blog)

    response = client.delete(f"/blog/{blog.id}")

    assert response.status_code == 204

    blog_inserted = test_db.query(Blog).filter(Blog.id != blog.id).first()

    assert blog_inserted == None


def test_update_blog():
    test_db = override_get_db()

    faker_blog = builder_blog.generate_blog()

    blog = Blog(title=faker_blog.title, body=faker_blog.body, user_id=1)
    test_db.add(blog)
    test_db.commit()
    test_db.refresh(blog)

    blog.title = "New Title"

    response = client.put(f"/blog/{blog.id}", json=BlogFaker(
        title=blog.title,
        body=blog.body
    ))

    blog_result = response.json()

    assert blog_result['title'] == "New Title"
    assert blog_result['body'] == faker_blog.body
