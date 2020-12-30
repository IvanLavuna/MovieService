from flask import jsonify, request, g

from movie_app import app
from movie_app.models import User, Reservation, MovieSchedule
from movie_app.views import session, auth


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')}), 200


@app.route('/user/logout', methods=['GET'])
@auth.login_required
def logout():
    return jsonify(meta={"code": 200, "type": "OK", "message": "Success"}), 200


@app.route('/user/reserve', methods=['POST'])
@auth.login_required
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
    return jsonify(meta={"code": 201, "type": "Created", "message": "Success. Reservation is created for %s"
                                                               % session.query(User).get(user_id)}), 201


@app.route('/user/<int:id>', methods=['PUT', 'GET', 'DELETE'])
@auth.login_required
def user_handler_by_id(id):
    if session.query(User.id).filter_by(id=id).scalar() is None:
        return jsonify(meta={"code": 404, "type": "Not Found", "message": "Specified user was not found"}), 400

    user = session.query(User).get(id)

    if g.user.id != id:
        return jsonify(meta={"code": 403, "type": "Forbidden", "message": "No permission"}), 403

    if request.method == 'GET':
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success"}, User=user.serialize), 200

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
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. User is updated"}, User=user.serialize), \
               200

    elif request.method == 'DELETE':
        session.delete(user)
        session.commit()
        return jsonify(meta={"code": 200, "type": "OK", "message": "Success. User is deleted"}, User=user.serialize),\
               200