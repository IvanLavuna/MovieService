"""
For now some test are dependant from each other
"""


def test_user(client):
    """
    1. Post not existing user
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
    assert response.status_code == 201
    assert b"LaVuna" in response.data
    assert b"lavuna2002" not in response.data

    """
    2. Post existing user
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
    3. Post user with not specified all info
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
    TODO : bug are here
    """
    response = client.get('/user/login', json={
        "username": "LaVuna",
        "password": "lavuna2002",
    })
    assert response.status_code == 200
    assert b"Success" in response.data

    """
    5. login existing user with email and password
    """
    response = client.get('/user/login', json={
        "email": "LaVuna@gmail.com",
        "password": "lavuna2002"
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
    },)

    assert response.status_code == 201
    assert b"Matrix: Reboot" in response.data
    assert b"2:33:23" in response.data
    #
    # """
    # 2. Creating movie by admin with wrong data supplied
    # """
    # response = client.post('/movie', json={
    #     "name": "Matrix: Reboot",
    #     "picture": "Matrix.png",
    #     "info": "Very cool psychological movie about reality",
    #     "actors": "Kiany and company",
    #     "duration": "2:33:23",
    # }, password="admin2", username=admin.username)
    # assert response.status_code == 401
    #
    # """
    # 3. Getting all movies
    # """
    # response = client.get('/movie',
    #                       password="admin", username=admin.username)
    #
    # assert response.status_code == 200
    #
    #
    #
    #
    #
    #
    #




