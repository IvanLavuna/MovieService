from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)
app.config.from_pyfile('./../instance/flask.cfg')

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
engine.connect()
db_session = scoped_session(sessionmaker(bind=engine))


from movie_app.views import every_user, logged_user, admin
