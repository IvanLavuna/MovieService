from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/cinema_db'
app.secret_key = b's8a9012mksdfnkj$@()($erjw09rjwef'


from movie_app.views import every_user, logged_user, admin
