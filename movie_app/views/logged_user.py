from flask import jsonify, request, g

from movie_app import app
from movie_app.models import User, Reservation, MovieSchedule
from movie_app.views import session, auth


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/user/logout', methods=['GET'])
@auth.login_required
def logout():
    return jsonify(meta={"code": 200, "type": "OK", "message": "Success"})


@app.route('/user/reserve', methods=['POST'])
@auth.login_required
def reserve():
    movie_schedule_id = request.json.get('movie_schedule_id', '')
    user_id = request.json.get('user_id', '')

    if not movie_schedule_id or not user_id:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "Missing arguments"})
    if session.query(MovieSchedule).get(movie_schedule_id) is None:
        return jsonify(meta={"code": 400, "type": "Bad Request", "message": "No such schedule on affiche"})

    reservation = Reservation(movie_schedule_id=movie_schedule_id, user_id=user_id)
    session.add(reservation)
    session.commit()
    return jsonify(meta={"code": 200, "type": "OK", "message": "Success. Place is reserved for %s"
                                                               % session.query(User).get(user_id)})
