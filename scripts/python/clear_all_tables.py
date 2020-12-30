from movie_app.models import User, Movie, MovieSchedule, Reservation
from movie_app import db_session


def clear_db():
    session = db_session()

    session.query(Reservation).delete()
    session.query(MovieSchedule).delete()

    session.query(User).delete()
    session.query(Movie).delete()

    session.commit()


if __name__ == '__main__':
    clear_db()
