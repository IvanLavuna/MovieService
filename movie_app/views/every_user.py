from flask import jsonify, request
from movie_app import app
from movie_app.models import User, Movie, MovieSchedule
from movie_app.views import session


@app.route("/user/register", methods=['POST'])
def register():
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
    return jsonify(User=new_user.serialize, meta={"code": 201, "type": "OK", "message": "Success"}), 201


@app.route('/user/login', methods=['GET', 'POST'])
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
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success"}, User=user.serialize), 200
    return jsonify(meta={"code": 406, "type": "Not Acceptable", "message": "Invalid data supplied"}), 406


@app.route('/movie', methods=['GET'])
def get_movies():
    movies = session.query(Movie).all()
    return jsonify(Movies=[i.serialize for i in movies]), 200


@app.route('/movie/<int:id>', methods=['GET'])
def get_movie_by_id(id):
    if session.query(Movie.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Movie with specified id was not found"}), 404

    movie = session.query(Movie).filter_by(id=id).one()
    return jsonify(meta={"code": 200, "type": "OK", "message": "Success"}, Movie=movie.serialize), 200


@app.route('/schedule', methods=['GET'])
def get_movie_schedules():
    movie_schedules = session.query(MovieSchedule).all()
    return jsonify(MovieSchedules=[i.serialize for i in movie_schedules])


@app.route('/schedule/<int:id>', methods=['GET'])
def get_movie_schedule_by_id(id):
    if session.query(MovieSchedule.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Specified schedule was not found"}), 404

    movie_schedule = session.query(MovieSchedule).get(id)

    return jsonify(meta={"code": 200, "type": "OK", "message": "Success"}, MovieSchedule=movie_schedule.serialize), 200
