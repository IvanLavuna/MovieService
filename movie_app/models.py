import random
import string
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

BaseModel = declarative_base()


# secret key to create and verify tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    firstname = Column(String(35), nullable=False)
    lastname = Column(String(35), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password_hash = Column(String(240), nullable=False)
    phone_number = Column(String(25))
    photo = Column(String(300), default="men_who_watch_the_sky.jpg")
    role = Column(String(64), default='user')

    def __repr__(self):
        return f"User('{self.username}','{self.firstname}','{self.lastname}','{self.email}','{self.phone_number}')"

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "phone_number": self.phone_number,
            "photo": self.photo
        }

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user_id = data['id']
        return user_id


class Movie(BaseModel):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    picture = Column(String(300), default="https://asianwiki.com/images/8/88/Default-KM-engsubtrailer.jpg")
    info = Column(String(500), default="...")
    actors = Column(String(200), default="...")
    duration = Column(String(20), nullable=False)

    def __repr__(self):
        return f"Movie('{self.name}','{self.picture}','{self.info}','{self.actors}','{self.duration}')"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "info": self.info,
            "actors": self.actors,
            "duration": self.duration
        }


class MovieSchedule(BaseModel):
    __tablename__ = 'movie_schedule'

    id = Column(Integer, primary_key=True)
    date = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)

    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    movie = relationship(Movie)

    def __repr__(self):
        return f"User('{self.movie_id}','{self.date}','{self.time}')"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "time": self.time,
            "movie_id": self.movie_id
        }


class Reservation(BaseModel):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    movie_schedule_id = Column(Integer, ForeignKey('movie_schedule.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    movie_schedule = relationship(MovieSchedule)
    user = relationship(User)

    def __repr__(self):
        return f"User('{self.movie_schedule_id}','{self.user_id}')"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "date": self.movie_schedule.date,
            "time": self.movie_schedule.time,
            "movie_id": self.movie_schedule.movie_id,
            "user_id": self.user_id
        }

