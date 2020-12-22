from flask import jsonify, request
from movie_app import app
from movie_app.models import User, Movie, MovieSchedule
from movie_app.views import session, auth, requires_roles


@app.route("/user", methods=["GET"])
@auth.login_required
@requires_roles('admin')
def get_all_user():
    users = session.query(User).all()

    return jsonify(Users=[i.serialize for i in users])


@app.route('/user/<int:id>', methods=['PUT', 'GET', 'DELETE'])
@auth.login_required
@requires_roles('admin')
def user_handler_by_id(id):
    if session.query(User.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Specified user was not found"})

    user = session.query(User).get(id)
    if request.method == 'GET':
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success"}, User=user.serialize)

    if request.method == 'PUT':
        username = request.json.get('username', '')
        firstname = request.json.get('firstname', '')
        lastname = request.json.get('lastname', '')
        email = request.json.get('email', '')
        password = request.json.get('password', '')
        phone_number = request.json.get('phone_number', '')
        photo = request.json.get('photo', '')
        if username:
            user.username = username
        if firstname:
            user.firstname = firstname
        if lastname:
            user.lastname = lastname
        if email:
            user.email = email
        if password:
            user.password_hash = User.hash_password(password)
        if phone_number:
            user.phone_number = phone_number
        if photo:
            user.photo = photo

        session.add(user)
        session.commit()
        return jsonify(meta={"code": 201, "type": "OK", "message": "Success. User is updated"}, User=user.serialize)

    elif request.method == 'DELETE':
        session.delete(user)
        session.commit()
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. User is deleted"}, User=user.serialize)


@app.route('/movie', methods=['POST'])
@auth.login_required
@requires_roles('admin')
def create_movie():
    name = request.json.get('name', '')
    picture = request.json.get('picture', '')
    info = request.json.get('info', '')
    actors = request.json.get('actors', '')
    duration = request.json.get('duration', '')
    if not name or not duration:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "Missing arguments"})

    new_movie = Movie(name=name, picture=picture, info=info, actors=actors, duration=duration)
    session.add(new_movie)
    session.commit()
    return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Movie is created"},
                   Movie=new_movie.serialize)


@app.route('/movie/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required
@requires_roles('admin')
def modify_movie(id):
    if session.query(Movie.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Movie with specified id was not found"})

    movie = session.query(Movie).filter_by(id=id).one()

    if request.method == 'PUT':
        name = request.json.get('name', '')
        picture = request.json.get('picture', '')
        info = request.json.get('info', '')
        actors = request.json.get('actors', '')
        duration = request.json.get('duration', '')
        if name:
            movie.name = name
        if picture:
            movie.picture = picture
        if info:
            movie.info = info
        if actors:
            movie.actors = actors
        if duration:
            movie.duration = duration
        session.add(movie)
        session.commit()
        return jsonify(meta={"code": 201, "type": "OK", "message": "Success. Movie is updated"}, Movie=movie.serialize)

    elif request.method == 'DELETE':
        session.delete(movie)
        session.commit()
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Movie is deleted"}, Movie=movie.serialize)


@app.route('/schedule', methods=['POST'])
@auth.login_required
@requires_roles('admin')
def create_movie_schedule():
    date = request.json.get('date', '')
    time = request.json.get('time', '')
    movie_id = request.json.get('movie_id', '')
    if not date or not time or not movie_id:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "Missing arguments"})
    if session.query(Movie.id).filter_by(id=movie_id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Movie with specified id was not found"})
    if session.query(MovieSchedule).filter_by(date=date, time=time).first() is not None:
        return jsonify(meta={"code": 409, "type": "Conflict", "message": "This date and time is already reserved"})

    movie_schedule = MovieSchedule(movie_id=movie_id, date=date, time=time)
    session.add(movie_schedule)
    session.commit()
    return jsonify(meta={"code": 200, "type": "OK", "message": "Success"},
                   MovieSchedule=movie_schedule.serialize)


@app.route('/schedule/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required
@requires_roles('admin')
def modify_movie_schedule(id):
    if session.query(MovieSchedule.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Specified schedule was not found"})

    movie_schedule = session.query(MovieSchedule).get(id)

    if request.method == 'PUT':
        movie_id = request.json.get('movie_id', '')
        date = request.json.get('date', '')
        time = request.json.get('time', '')
        if movie_id:
            if session.query(Movie).filter_by(id=movie_id).first() is not None:
                movie_schedule.movie_id = movie_id
            else:
                return jsonify(meta={"code": 400, "type": "Bad Request",
                                     "message": "No such movie id"})
        if date:
            movie_schedule.date = date
        if time:
            movie_schedule.time = time
        session.add(movie_schedule)
        session.commit()
        return jsonify(meta={"code": 201, "type": "OK", "message": "Success. Movie schedule is updated"},
                       MovieSchedule=movie_schedule.serialize)

    if request.method == 'DELETE':
        session.delete(movie_schedule)
        session.commit()
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Movie schedule is deleted"},
                       MovieSchedule=movie_schedule.serialize)

