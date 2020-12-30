from flask import jsonify, request
from movie_app import app
from movie_app.models import User, Movie, MovieSchedule
from movie_app.views import session, auth, requires_roles


@app.route("/user", methods=["GET"])
@auth.login_required
@requires_roles('admin')
def get_all_user():
    users = session.query(User).all()
    return jsonify(Users=[i.serialize for i in users],
                   meta={"code": 200, "type": "OK", "message": "Success"}), 200


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
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "Missing arguments"}), 400

    new_movie = Movie(name=name, picture=picture, info=info, actors=actors, duration=duration)
    session.add(new_movie)
    session.commit()
    return jsonify(meta={"code": 201, "type": "OK", "message": "Success. Movie is created"},
                   Movie=new_movie.serialize), 201


@app.route('/movie/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required
@requires_roles('admin')
def modify_movie(id):
    if session.query(Movie.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Movie with specified id was not found"}), 404

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
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Movie is updated"},
                       Movie=movie.serialize), 200

    elif request.method == 'DELETE':
        movie_schedule = session.query(MovieSchedule).filter_by(movie_id=id).first()
        if movie_schedule is not None:
            return jsonify(meta={"code": 409, "type": "Conflict", "message": "There are some schedules on this movie."
                                                                             "Delete them in order to delete this movie"},
                           Movie=movie.serialize), 409
        session.delete(movie)
        session.commit()
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Movie is deleted"},
                       Movie=movie.serialize), 200


@app.route('/schedule', methods=['POST'])
@auth.login_required
@requires_roles('admin')
def create_movie_schedule():
    date = request.json.get('date', '')
    time = request.json.get('time', '')
    movie_id = request.json.get('movie_id', '')
    if not date or not time or not movie_id:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "Missing arguments"}), 400
    if session.query(Movie.id).filter_by(id=movie_id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Movie with specified id was not found"}), 404
    if session.query(MovieSchedule).filter_by(date=date, time=time).first() is not None:
        return jsonify(meta={"code": 409, "type": "Conflict", "message": "This date and time is already reserved"}), 409

    movie_schedule = MovieSchedule(movie_id=movie_id, date=date, time=time)
    session.add(movie_schedule)
    session.commit()
    return jsonify(meta={"code": 201, "type": "Created", "message": "Movie schedule is created!"},
                   MovieSchedule=movie_schedule.serialize), 201


@app.route('/schedule/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required
@requires_roles('admin')
def modify_movie_schedule(id):
    if session.query(MovieSchedule.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Specified schedule was not found"}), 404

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
                                     "message": "No such movie id"}), 400
        if date:
            movie_schedule.date = date
        if time:
            movie_schedule.time = time
        session.add(movie_schedule)
        session.commit()
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Movie schedule is `updated"},
                       MovieSchedule=movie_schedule.serialize), 200

    if request.method == 'DELETE':
        session.delete(movie_schedule)
        session.commit()
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Movie schedule is deleted"},
                       MovieSchedule=movie_schedule.serialize), 200
