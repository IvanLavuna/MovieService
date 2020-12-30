def test_movie(client, admin):
    """
    1. Creating movie by admin
    """
    response = client.post('/movie', json={
        "name": "Matrix: Reboot",
        "picture": "Matrix.png",
        "info": "Very cool psychological movie about reality",
        "actors": "Kiany and company",
        "duration": "2:33:23",
    }, headers=admin.headers)

    assert response.status_code == 201
    assert b"Matrix: Reboot" in response.data
    assert b"2:33:23" in response.data

    # movie_id
    movie_id = response.get_json()["Movie"]['id']

    """
    2. Creating movie by admin with wrong data supplied
    """
    response = client.post('/movie', json={
        "picture": "Matrix.png",
        "info": "Very cool psychological movie about reality",
        "actors": "Kiany and company",
        "duration": "2:33:23",
    }, headers=admin.wrong_credentials_headers)
    assert response.status_code == 401

    """
    3. Getting all movies
    """
    response = client.get('/movie')
    assert response.status_code == 200
    assert b"Matrix: Reboot" in response.data
    assert b"2:33:23" in response.data

    """
    4. Changing movie 'Matrix: Reboot' with specified id
    """
    response = client.put('/movie/%s' % movie_id, json={
        "name": "Matrix: REBOOT",
        "duration": "2:11:11"
    }, headers=admin.headers)

    assert response.status_code == 200
    assert b"Matrix: REBOOT" in response.data
    assert b"2:11:11" in response.data

    """
    5. Changing movie 'Matrix: Reboot' without admin credentials
    """
    response = client.put('/movie/%s' % movie_id, json={
        "name": "Matrix: REBOOT",
        "duration": "2:11:11"
    })
    assert response.status_code == 401

    """
    6. deleting movie
    """
    response = client.delete('/movie/%s' % movie_id, headers=admin.headers)
    assert response.status_code == 200

