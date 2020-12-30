import pytest
from movie_app import app
from scripts.python.clear_all_tables import clear_db
from movie_app.models import User, Movie, MovieSchedule, Reservation
from movie_app import db_session
from sqlalchemy.util import b64encode


@pytest.fixture(scope="module")
def default_user():
    user = User(username="DefaultUser",
                firstname="DefaultUser",
                lastname="DefaultUser",
                email="DefUser@gmail.com",
                password_hash=User.hash_password("user"),
                phone_number=".!.",
                photo="user.png",
                role='user')

    user.password = 'user'
    user.credentials = b64encode(b'DefaultUser:user')
    user.wrong_credentials = b64encode(b'DefaultUser:user1')
    user.headers = {"Authorization": "Basic {}".format(user.credentials)}
    user.wrong_credentials_headers = {"Authorization": "Basic {}".format(user.wrong_credentials)}

    session = db_session()
    session.add(user)
    session.commit()

    return user


@pytest.fixture(scope="module")
def default_movie():
    movie = Movie(name="DefaultMovie",
                  picture="DefaultMovie.png",
                  info="Default info.",
                  actors="Default actors",
                  duration="2:00:00")
    session = db_session()
    session.add(movie)
    session.commit()

    return movie


@pytest.fixture(scope="module")
def admin():
    admin = User(username="admin",
                 firstname="admin",
                 lastname="admin",
                 email="admin@gmail.com",
                 password_hash=User.hash_password("admin"),
                 phone_number=".!.",
                 photo="photo.jpeg",
                 role='admin')

    admin.password = 'admin'
    admin.credentials = b64encode(b'admin:admin')
    admin.wrong_credentials = b64encode(b'admin:admin1')
    admin.headers = {"Authorization": "Basic {}".format(admin.credentials)}
    admin.wrong_credentials_headers = {"Authorization": "Basic {}".format(admin.wrong_credentials)}

    session = db_session()
    session.add(admin)
    session.commit()

    return admin


@pytest.fixture(scope="module")
def client():
    flask_app = app

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()
    clear_db()


@pytest.fixture(scope="module")
def session():
    session = db_session()
    return session


@pytest.fixture(scope="module")
def new_user():
    user = User(username="Uncle_Stiv",
                firstname="Stiven",
                lastname="Black",
                email="stiven@gmail.com",
                password_hash=User.hash_password("password123"),
                phone_number=".!.",
                photo="stiven.png",
                role='user')
    return user


@pytest.fixture(scope="module")
def new_movie():
    movie = Movie(name="Sponge Bob",
                  picture="Sponge-bob.png",
                  info="Movie about real life under the bottom",
                  actors="Sponge bob, patrick, squidward",
                  duration="1:40:50")
    return movie



