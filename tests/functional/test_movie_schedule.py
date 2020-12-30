def test_movie_schedule(client, admin, default_movie):
    """
    1. Creating one movie
    """
    response = client.post('/movie', json={
        "name": "Star Wars",
        "picture": "star.png",
        "info": "About wars in space",
        "actors": "Joda, Jedai",
        "duration": "2:49:32",
    }, headers=admin.headers)

    assert response.status_code == 201
    assert b"Star Wars" in response.data
    assert b"2:49:32" in response.data

    # movie id
    star_wars_id = response.get_json()['Movie']['id']

    """
    2. Creating  movie schedule with no credentials
    """
    response = client.post("/schedule", json={
        "date": "15-01-2021",
        "time": "14:23:23",
        "movie_id": star_wars_id
    })
    assert response.status_code == 401

    """
    2. Creating 2 movie schedules with correct credentials
    """
    response = client.post("/schedule", json={
        "date": "15-01-2021",
        "time": "14:23:23",
        "movie_id": star_wars_id
    }, headers=admin.headers)
    assert response.status_code == 201

    response = client.post("/schedule", json={
        "date": "15-01-2021",
        "time": "18:23:23",
        "movie_id": star_wars_id
    }, headers=admin.headers)
    assert response.status_code == 201

    """
    3. Creating third movie schedule with data and time of first movie
    """
    response = client.post("/schedule", json={
        "date": "15-01-2021",
        "time": "14:23:23",
        "movie_id": default_movie.id
    }, headers=admin.headers)
    assert response.status_code == 409
    assert b'Conflict' in response.data

    """
    4. Get all movie schedules
    """
    response = client.get('/schedule')
    assert response.status_code == 200

    """
    5. Get movie schedule with specified id
    """
    schedule_id = response.get_json()['MovieSchedules'][0]['id']
    response = client.get('/schedule/%s' % schedule_id)
    assert response.status_code == 200

    """
    6. PUT movie schedule with specified id and correct credentials
    """
    response = client.put('/schedule/%s' % schedule_id, json={
        "time": "21:23:00"
    }, headers=admin.headers)

    assert response.status_code == 200
    assert b"21:23:00" in response.data

    """
    7. DELETE movie schedule with specified id and correct credentials
    """
    response = client.delete('/schedule/%s' % schedule_id, headers=admin.headers)
    assert response.status_code == 200
