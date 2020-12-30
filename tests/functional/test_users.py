"""
For now some test are dependant from each other
"""
from sqlalchemy.util import b64encode
from movie_app.models import User


def test_user_auth(client, session, default_user):
    """
    1. Create not existing 3 users
    """
    response = client.post('/user/register', json={
        "username": "LaVuna",
        "firstname": "Ivan",
        "lastname": "Manchur",
        "email": "LaVuna@gmail.com",
        "password": "lavuna",
        "phone_number": "0632804617",
        "photo": "my_photo.png"
    })
    assert response.status_code == 201
    assert b"LaVuna" in response.data
    assert b"lavuna" not in response.data

    response = client.post('/user/register', json={
        "username": "Fedora",
        "firstname": "Byanka",
        "lastname": "KillWereWolf",
        "email": "Killer666@gmail.com",
        "password": "qwerty",
        "phone_number": "0632804632",
        "photo": "my_photo.png"
    })
    assert response.status_code == 201
    assert b"Fedora" in response.data
    assert b"qwerty" not in response.data

    response = client.post('/user/register', json={
        "username": "Volodya",
        "firstname": "Volodya",
        "lastname": "Remembersky",
        "email": "RememberMe@gmail.com",
        "password": "password123",
        "phone_number": "0632804689",
        "photo": "my_photo.png"
    })
    assert response.status_code == 201
    assert b"Volodya" in response.data
    assert b"password123" not in response.data

    """
    2. Create existing user
    """
    response = client.post('/user/register', json={
        "username": "LaVuna",
        "firstname": "Ivan",
        "lastname": "Manchur",
        "email": "LaVuna@gmail.com",
        "password": "lavuna2002",
        "phone_number": "0632804617",
        "photo": "my_photo.png"
    })
    assert response.status_code == 409
    assert b"Conflict" in response.data

    """
    3. Create user with not specified all required info
    """
    response = client.post('/user/register', json={
        "firstname": "Ivan",
        "lastname": "Manchur",
        "email": "LaVuna@gmail.com",
        "password": "lavuna2002",
        "phone_number": "0632804617",
        "photo": "my_photo.png"
    })
    assert response.status_code == 400
    assert b"Bad Request" in response.data

    """
    4. login existing user with username and password
    """
    response = client.get('/user/login', json={
        "username": "LaVuna",
        "password": "lavuna",
    })
    assert response.status_code == 200
    assert b"Success" in response.data

    """
    5. login existing user with email and password
    """
    response = client.get('/user/login', json={
        "email": default_user.email,
        "password": default_user.password
    })
    assert response.status_code == 200
    assert b"Success" in response.data

    """
    6. login user without redundant data
    """
    response = client.get('/user/login', json={
        "email": "LaVuna@gmail.com",
    })
    assert response.status_code == 406
    assert b"Not Acceptable" in response.data

    """
    7. login user with wrong email
    """
    response = client.get('/user/login', json={
        "email": "LaVuna@gmail.com1",
        "password": "lavuna20024"
    })
    assert response.status_code == 404
    assert b"Not Found" in response.data

    """
    8. Logout user
    """
    response = client.get('user/logout', headers=default_user.headers)
    assert response.status_code == 200

    """
    9. Update user with invalid credentials
    """
    response = client.put('user/%s' % default_user.id, json={
        "lastname": "Gourge",
        "firstname": "De Mouchhi"
    }, headers=default_user.wrong_credentials_headers)
    assert response.status_code == 401

    """
    10. Update user with valid credentials
    """
    response = client.put('user/%s' % default_user.id, json={
        "lastname": "Gourge",
        "firstname": "De Mouchhi"
    }, headers=default_user.headers)
    assert response.status_code == 200
    assert b"Gourge" in response.data
    assert b"De Mouchhi" in response.data

    """
    11. GET user with invalid credentials
    """
    response = client.get("/user/%s" % default_user.id,
                          headers=default_user.wrong_credentials_headers)
    assert response.status_code == 401

    """
    12. GET user with valid credentials
    """
    response = client.get("/user/%s" % default_user.id, headers=default_user.headers)
    assert response.status_code == 200
    assert b"DefaultUser" in response.data
    assert b"DefUser@gmail.com" in response.data

    """
    13. DELETE default user with  token of second user
    """
    credentials = b64encode(b'Fedora:qwerty')
    headers = {"Authorization": "Basic {}".format(credentials)}
    token2 = bytes(client.get("/token", headers=headers).get_json()["token"] + ":JO", 'utf-8')
    credentials = b64encode(token2)
    headers = {"Authorization": "Basic {}".format(credentials)}
    response = client.delete("/user/%s" % default_user.id, headers=headers)

    assert response.status_code == 403

    """
    14. DELETE third user with valid credentials (token)
    """
    credentials = b64encode(b'Volodya:password123')
    headers = {"Authorization": "Basic {}".format(credentials)}
    token = bytes(client.get("/token", headers=headers).get_json()["token"] + ":JO", 'utf-8')
    user_id = session.query(User).filter_by(username="Volodya").first().id
    credentials = b64encode(token)
    headers = {"Authorization": "Basic {}".format(credentials)}
    response = client.delete("/user/%s" % user_id, headers=headers)

    assert response.status_code == 200


def test_user_reservation(client, admin, default_movie, default_user):
    """
    1. Creating 2 movie schedules by admin
    """
    response = client.post('/schedule', json={
        "date": "04-07-2004",
        "time": "14:35:00",
        "movie_id": default_movie.id
    }, headers=admin.headers)
    assert response.status_code == 201

    # movie schedule id 1
    movie_schedule_id1 = response.get_json()['MovieSchedule']['id']

    response = client.post('/schedule', json={
        "date": "04-07-2004",
        "time": "18:35:00",
        "movie_id": default_movie.id
    }, headers=admin.headers)
    assert response.status_code == 201

    # movie schedule id 2
    movie_schedule_id2 = response.get_json()['MovieSchedule']['id']

    """
    2. Reserving first movie schedule by user DefUser with Fedora credentials
    """
    fedora_credentials = b64encode(b'Fedora:qwerty')
    fedora_headers = {"Authorization": "Basic {}".format(fedora_credentials)}
    response = client.post('/user/reserve', json={
        "movie_schedule_id": movie_schedule_id1,
        "user_id": default_user.id
    }, headers=fedora_headers)
    assert response.status_code == 406

    """
    3. Reserving second movie schedule by defUser user with defUser user
        credentials
    """
    response = client.post('/user/reserve', json={
        "movie_schedule_id": movie_schedule_id2,
        "user_id": default_user.id
    }, headers=default_user.headers)
    assert response.status_code == 201


def test_user_actions(client, default_movie, default_user):
    """
    1. Get All movies
    """
    response = client.get('/movie')
    assert response.status_code == 200
    assert b"DefaultMovie" in response.data

    """
    2. Get Movie by id
    """
    response = client.get('/movie/%s' % default_movie.id)
    assert response.status_code == 200
    assert b"DefaultMovie" in response.data

    """
    3. Create Movie
    """
    response = client.post('/movie', json={
        "name": "Sponge Bob",
        "picture": "Sponge-bob.png",
        "info": "Movie about real life under the bottom",
        "actors": "Sponge bob, patrick, squidward",
        "duration": "1:40:50"
    }, headers=default_user.headers)
    assert response.status_code == 401

    """
    4. Update Movie
    """
    response = client.put('/movie/%s' % default_movie.id, json={
        "actors": "Sponge bob, patrick, squidward, plankton",
        "duration": "1:41:50"
    }, headers=default_user.headers)
    assert response.status_code == 401

    """
    5. Delete movie
    """
    response = client.delete('/movie/%s' % default_movie.id,
                             headers=default_user.headers)
    assert response.status_code == 401






