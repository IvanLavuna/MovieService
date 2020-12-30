from movie_app.models import User
from movie_app import db_session

session = db_session()

admin = User(id=101,
             username="admin",
             firstname="admin",
             lastname="admin",
             email="admin@gmail.com",
             password_hash=User.hash_password("admin"),
             phone_number="90123123",
             photo="photo.jpeg",
             role='admin')

session.add(admin)
session.commit()
