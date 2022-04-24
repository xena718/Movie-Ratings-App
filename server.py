"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template('homepage.html')

# Replace this with routes and view functions!

@app.route('/movies')
def all_movies():
    """get all movies"""
    movies = crud.get_movies()
    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def movie_detail(movie_id):

    return render_template('movie_details.html', movie=crud.get_movie_by_id(movie_id))


@app.route('/users')
def all_users():
    """get all users"""
    users = crud.get_users()
    return render_template('all_users.html', users=users)
@app.route('/users', methods=['POST'])
def creat_user():
    """ create new user """

    email_input = request.form.get('email')
    
    if crud.get_user_by_email(email_input) is None:
        password_input = request.form.get('password')
        new_user = crud.create_user(email_input, password_input)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully')
    else:
        flash('User already exists. Try again')

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    """user log in"""

    login_email = request.form.get('email')
    login_password = request.form.get('password')
    match_user = crud.get_user_by_email(login_email)

    if match_user and match_user.password == login_password:
        user_id = match_user.user_id
        session['user_id'] = user_id
        flash(f'login success as {login_email}!')
    else:
        flash('email or password does not match, try again or create an account')
    
    return render_template('rate_a_movie.html', movies = crud.get_movies())
    # return render_template('homepage.html', user_id=user_id)
    

@app.route('/rate-movie', methods=['POST'])
def rate_movie():
    """ get movie name and score"""
    movie_title = request.form.get("movie")
    score = request.form.get("score")
    movie = crud.get_movie_by_title(movie_title)
    user = crud.get_user_by_id(session['user_id'])

    new_rating = crud.create_rating(movie, user, score)
    db.session.add(new_rating)
    db.session.commit()
    flash('rating successfully added')
    return render_template('rate_a_movie.html', movies = crud.get_movies())

@app.route('/users/<user_id>')
def user_detail(user_id):

    return render_template('user_details.html', user=crud.get_user_by_id(user_id))

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=5002)
