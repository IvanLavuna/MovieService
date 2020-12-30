from movie_app.models import User


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, firstname, lastname, email, hashed_password,
        and role fields are defined correctly
    """
    assert new_user.username == "Uncle_Stiv"
    assert new_user.firstname == "Stiven"
    assert new_user.lastname == "Black"
    assert new_user.email == 'stiven@gmail.com'
    assert new_user.password_hash != 'password123'
    assert new_user.role == 'user'


def test_new_movie(new_movie):
    """
    GIVEN a Movie model
    WHEN a new movie are created
    THEN check the name, picture, info, actors, duration
    """
    assert new_movie.name == "Sponge Bob"
    assert new_movie.picture == "Sponge-bob.png"
    assert new_movie.info == "Movie about real life under the bottom"
    assert new_movie.actors == "Sponge bob, patrick, squidward"
    assert new_movie.duration == "1:40:50"

