from flask import jsonify, request
from flask_cors import cross_origin

from movie_app import app
from movie_app.models import User, Movie, MovieSchedule, Reservation
from movie_app.views import session
import datetime
import calendar


@app.route("/user/register", methods=['POST'])
@cross_origin()
def register():
    print("Request Method:", request.method)
    username = request.json.get('username', '')
    firstname = request.json.get('firstname', '')
    lastname = request.json.get('lastname', '')
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    phone_number = request.json.get('phone_number', '')
    photo = request.json.get('photo', '')

    # checking if all required arguments were passed
    if not username or not firstname or not lastname or not email or not password:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "Missing arguments"}), 400

    # checking if such username or email already exist
    if session.query(User).filter_by(username=username).first() is not None or \
            session.query(User).filter_by(username=email).first() is not None:
        return jsonify(meta={"code": 409, "type": "Conflict", "message": "Such username or email already exist"}), 409

    new_user = User(username=username, firstname=firstname, lastname=lastname, email=email,
                    password_hash=User.hash_password(password), phone_number=phone_number, photo=photo)
    session.add(new_user)
    session.commit()
    return jsonify(new_user.serialize), 201


@app.route('/user/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    username = request.json.get('username', '')
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    user = None
    if username:
        user = session.query(User).filter_by(username=username).first()
    elif email:
        user = session.query(User).filter_by(email=email).first()

    if user is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Try again"}), 404
    if user.verify_password(password):
        return jsonify(user.serialize), 200
    return jsonify(meta={"code": 406, "type": "Not Acceptable", "message": "Invalid data supplied"}), 406


@app.route('/movies', methods=['GET'])
@cross_origin()
def get_movies():
    movies = session.query(Movie).all()
    return jsonify([i.serialize for i in movies]), 200


@app.route('/movie/<int:id>', methods=['GET'])
@cross_origin()
def get_movie_by_id(id):
    if session.query(Movie.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Movie with specified id was not found"}), 404

    movie = session.query(Movie).filter_by(id=id).one()
    return jsonify(movie.serialize), 200


@app.route('/schedules', methods=['GET'])
@cross_origin()
def get_movie_schedules():
    movie_schedules = session.query(MovieSchedule).all()
    return jsonify([i.serialize for i in movie_schedules])


@app.route('/schedule/<int:id>', methods=['GET'])
@cross_origin()
def get_movie_schedule_by_id(id):
    if session.query(MovieSchedule.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Specified schedule was not found"}), 404

    movie_schedule = session.query(MovieSchedule).get(id)

    return jsonify(movie_schedule.serialize), 200


@app.route('/schedule/movie/<int:id>', methods=['GET'])
@cross_origin()
def get_schedule_by_movie(id):
    movie_schedules = session.query(MovieSchedule).all()
    proper_movie_schedule = []
    for item in movie_schedules:
        if item.movie_id == id:
            proper_movie_schedule.append(item)
    return jsonify([i.serialize for i in proper_movie_schedule]), 200


# date format: 'year-month-day' 1999-12-25
@app.route('/schedule-days', methods=['GET'])
@cross_origin()
def get_schedule_days():

    full_response = []
    for i in range(7):
        cur_response = {}
        movie_sessions = []
        cur_date = datetime.datetime.today() + datetime.timedelta(days=i)
        date = f"{cur_date:%Y-%m-%d}"
        cur_response['date'] = date
        cur_response['day'] = calendar.day_name[cur_date.weekday()]

        for movie_schedule in session.query(MovieSchedule).filter_by(date=date):
            reservation_num = session.query(Reservation).filter_by(movie_schedule_id=movie_schedule.id).count()
            movie_sessions.append({"time": movie_schedule.time,
                                   "movie": movie_schedule.movie.serialize,
                                   "reservation_num": reservation_num})
        movie_sessions.sort(key=lambda x: x["time"])
        cur_response["movie_sessions"] = movie_sessions
        full_response.append(cur_response)

    return jsonify(full_response), 200



