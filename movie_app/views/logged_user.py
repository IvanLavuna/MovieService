import json

from flask import jsonify, request, g
from flask_cors import cross_origin

from movie_app import app
from movie_app.models import User, Reservation, MovieSchedule, Movie
from movie_app.views import session, auth


@app.route('/token')
@auth.login_required
@cross_origin()
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')}), 200


@app.route('/user/logout', methods=['GET'])
@auth.login_required
@cross_origin()
def logout():
    return jsonify(meta={"code": 200, "type": "OK", "message": "Success"}), 200


@app.route('/user/reserve', methods=['POST'])
@auth.login_required
@cross_origin()
def reserve():
    movie_schedule_id = request.json.get('movie_schedule_id', '')
    user_id = request.json.get('user_id', '')
    if user_id != g.user.id:
        return jsonify(meta={"code": 406, "type": "Not Acceptable", "message": "No permission"}), 406
    if not movie_schedule_id or not user_id:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "Missing arguments"}), 400
    if session.query(MovieSchedule).get(movie_schedule_id) is None:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "No such schedule on affiche"}), 400

    reservation = Reservation(movie_schedule_id=movie_schedule_id, user_id=user_id)
    session.add(reservation)
    session.commit()
    return jsonify(reservation.serialize), 201


@app.route('/user/<int:id>', methods=['PUT', 'GET', 'DELETE'])
@auth.login_required
@cross_origin()
def user_handler_by_id(id):
    # if session.query(User).filter_by(id=id).scalar() is None:
    #     return jsonify(meta={"code": 404, "type": "Not Found", "message": "Specified user was not found"}), 404

    user = session.query(User).get(id)

    # if g.user.id != id:
    #     return jsonify(meta={"code": 403, "type": "Forbidden", "message": "No permission"}), 403

    if request.method == 'GET':
        return jsonify(user.serialize), 200

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
        return jsonify(user.serialize), 200

    elif request.method == 'DELETE':
        session.delete(user)
        session.commit()
        return jsonify(user.serialize), 200


@app.route('/user/<int:id>/reservations', methods=['GET'])
@auth.login_required
@cross_origin()
def user_reservations(id):
    res = []
    reservations = {}
    movies = {}
    for item in session.query(Movie):
        movies[item.id] = item
    for item in session.query(Reservation):
        if item.user_id == id:
            reservations[item.movie_schedule_id] = item

    for item in session.query(MovieSchedule):
        if item.id in reservations:
            res.append({"movie_name": movies[item.movie_id].name,
                        "date": item.date,
                        "time": item.time})

    return jsonify([item for item in res]), 200

