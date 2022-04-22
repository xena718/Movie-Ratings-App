from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def create_rating(movie, user, score):
    """ create rating instance and return a new rating"""
    # rate = Rating(movie_id = movie.movie_id, user_id = user.user_id, score=score)
    rate = Rating(movie = movie, user = user, score = score)
    #movie on the left of = is the attribute name, movie on the right of= is movie instance
    return rate


if __name__ == '__main__':
    from server import app
    connect_to_db(app)