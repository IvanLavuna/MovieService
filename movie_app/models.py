from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:password@localhost/cinema_db')
engine.connect()
db_session = scoped_session(sessionmaker(bind=engine))
BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    firstname = Column(String(35), nullable=False)
    lastname = Column(String(35), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password_hash = Column(String(240), nullable=False)
    phone_number = Column(String(25))
    photo = Column(String(50), default="men_who_watch_the_sky.jpg")

    def __repr__(self):
        return f"User('{self.username}','{self.firstname}','{self.lastname}','{self.email}','{self.phone_number}')"


class Movie(BaseModel):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    picture = Column(String(30), default="movie.png")
    info = Column(String(500), default="...")
    actors = Column(String(200), default="...")
    duration = Column(String(20), nullable=False)

    def __repr__(self):
        return f"Movie('{self.name}','{self.picture}','{self.info}','{self.actors}','{self.duration}')"


class Reservation(BaseModel):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    date = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    movie = relationship(Movie)
    user = relationship(User)

    def __repr__(self):
        return f"User('{self.date}','{self.time}','{self.movie_id}','{self.user_id}')"


class MovieSchedule(BaseModel):
    __tablename__ = 'movie_schedule'

    id = Column(Integer, primary_key=True)
    date = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)

    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    movie = relationship(Movie)

    def __repr__(self):
        return f"User('{self.movie_id}','{self.date}','{self.time}')"
