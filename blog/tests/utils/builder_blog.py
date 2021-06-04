from faker import Faker
from .schemas import BlogFaker


def generate_blog(has_title: bool = True, has_body: bool = True) -> BlogFaker:
    faker = Faker()
    blog_faker = BlogFaker()
    if has_title:
        blog_faker.title = faker.paragraph(nb_sentences=1)
    if has_body:
        blog_faker.body = faker.paragraph(nb_sentences=5)
    return blog_faker
