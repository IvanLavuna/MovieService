import pytest
from movie_app import app
from movie_app.models import User, Movie, MovieSchedule, Reservation
from movie_app.models import db_session


@pytest.fixture(scope='module')
def new_user():
    user = User(id=2, username="Pikachu", firstname="Borys", lastname="Laplas", email="Lapko@gmail.com",
                password_hash=User.hash_password("laplap2002"), phone_number="901231233", photo="photo.jpeg")
    return user


@pytest.fixture(scope='module')
def admin():
    session = db_session()

    admin = User(id=101,
                 username="admin",
                 firstname="admin",
                 lastname="admin",
                 email="admin@gmail.com",
                 password_hash=User.hash_password("admin"),
                 phone_number=".!.",
                 photo="photo.jpeg",
                 role='admin')

    session.add(admin)
    session.commit()
    return admin


@pytest.fixture(scope='module')
def client():
    flask_app = app

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

    # TODO : rewrite it normally ( normally means not shitty))
    # clearing data base
    session = db_session()

    session.query(Reservation).delete()
    session.query(MovieSchedule).delete()

    session.query(User).delete()
    session.query(Movie).delete()

    session.commit()



