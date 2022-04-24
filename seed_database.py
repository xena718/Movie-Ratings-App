"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later

movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title = movie['title']
    overview = movie['overview']    
    poster_path = movie['poster_path']
    release_date = datetime.strptime(movie['release_date'], "%Y-%m-%d")
    new_movie = crud.create_movie(title = title, overview = overview, release_date = release_date, poster_path = poster_path)
    movies_in_db.append(new_movie)

    # TODO: create a movie here and append it to movies_in_db

model.db.session.add_all(movies_in_db)
model.db.session.commit()

users_in_db = []
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'
    new_user = crud.create_user(email=email, password=password)
    users_in_db.append(new_user)
    
    user_ratings = []
    for i in range(10):
        
        new_rating = crud.create_rating(user = new_user, movie = choice(movies_in_db), score=randint(1, 5))
        user_ratings.append(new_rating)
    
    model.db.session.add_all(user_ratings)
    # model.db.session.commit()
        
model.db.session.add_all(users_in_db)
model.db.session.commit()   


