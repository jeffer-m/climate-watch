# seed.py
from application import create_app
from application.extensions import db
from application.models import Post

app = create_app()

with app.app_context():
    db.create_all()

    if Post.query.count() == 0:
        post1 = Post(title="Welcome!", content="This is the first system post.", user_id=1)
        post2 = Post(title="Info", content="Please register to post.", user_id=1)
        db.session.add_all([post1, post2])
        db.session.commit()
        print("Initial posts seeded.")
    else:
        print("Posts already exist.")
