

def test_admin(client, admin, default_user):
    """
    1. Get all users without credentials
    """
    response = client.get("/user")
    assert response.status_code == 401

    """
    2. Get all users with default user credentials
    """
    response = client.get("/user", headers=default_user.headers)
    assert response.status_code == 401

    """
    3. Get all users with admin credentials
    """
    response = client.get("/user", headers=admin.headers)
    assert response.status_code == 200
    assert b"DefaultUser" in response.data

    """
    4. Modify default user info with admin credentials
    """
    response = client.put("/user/%s" % default_user.id, json={
        "phone_number": "063",
        "lastname": "Snippetko"
    }, headers=admin.headers)
    assert response.status_code == 403

    """
    5. Create movie
    """
    response = client.post('/movie', json={
        "name": "Once upon time in Hollywood ...",
        "picture": "70-th.png",
        "info": "10-th film by Qwentin Tarantino",
        "actors": "Bred Pitt, Leonardo Di Caprio",
        "duration": "2:45:56"
    }, headers=admin.headers)
    assert response.status_code == 201
    assert b'Once upon time in Hollywood ...' in response.data
    assert b"2:45:56" in response.data

    # movie id ("Once upon time in Hollywood")
    movie_id = response.get_json()['Movie']['id']

    """
    6. Update movie
    """
    response = client.put('/movie/%s' % movie_id, json={
        "actors": "Bred Pitt, Leonardo Di Caprio, Margo Robbie"
    }, headers=admin.headers)
    assert response.status_code == 200
    assert b"Bred Pitt, Leonardo Di Caprio, Margo Robbie" in response.data

    """
    7. Create movie schedule
    """
    response = client.post('/schedule', json={
        "date": "14-09-2019",
        "time": "15:45:00",
        "movie_id": movie_id
    }, headers=admin.headers)
    assert response.status_code == 201
    assert b"14-09-2019" in response.data
    assert b"15:45:00" in response.data

    # movie schedule id
    movie_schedule_id = response.get_json()["MovieSchedule"]['id']

    """
    8. Update movie schedule
    """
    response = client.put('/schedule/%s' % movie_schedule_id, json={
        "time": "18:55:00"
    }, headers=admin.headers)
    assert response.status_code == 200
    assert b"18:55:00" in response.data
    assert b"14-09-2019" in response.data

    """
    9. Delete movie(when there are movie schedule on it)
    """
    response = client.delete('/movie/%s' % movie_id, headers=admin.headers)
    assert response.status_code == 409

    """
    10. Delete movie schedule
    """
    response = client.delete('/schedule/%s' % movie_schedule_id,
                             headers=admin.headers)
    assert response.status_code == 200

    """
    11. Deleting again
    """
    response = client.delete('/schedule/%s' % movie_schedule_id,
                             headers=admin.headers)
    assert response.status_code == 404

    """
    12. Get all movies
    """
    response = client.get('/movie')
    assert response.status_code == 200
    assert b"Bred Pitt, Leonardo Di Caprio, Margo Robbie" in response.data
    assert b"Once upon time in Hollywood ..." in response.data

    """
    13. Delete movie
    """
    response = client.delete('/movie/%s' % movie_id, headers=admin.headers)
    assert response.status_code == 200

    """
    13. Again getting all movies
    """
    response = client.get('/movie')
    assert response.status_code == 200
    assert b"Bred Pitt, Leonardo Di Caprio, Margo Robbie" not in response.data
    assert b"Once upon time in Hollywood ..." not in response.data

