from sqlalchemy.exc import IntegrityError

from project.config import DevelopmentConfig
from project.dao.models import genre, director, movie
from project.server import create_app
from project.setup_db import db
from project.utils import read_json

app = create_app(DevelopmentConfig)

DATA_JSON = read_json("fixtures.json")

with app.app_context():
    for genre_item in DATA_JSON["genres"]:
        db.session.add(genre.Genre(id=genre_item["pk"], name=genre_item["name"]))

    for director_item in DATA_JSON["directors"]:
        db.session.add(director.Director(id=director_item["pk"], name=director_item["name"]))

    for movie_item in DATA_JSON["movies"]:
        db.session.add(movie.Movie(
                                    id=movie_item["pk"],
                                    title=movie_item["title"],
                                    description=movie_item["description"],
                                    trailer=movie_item["trailer"],
                                    year=movie_item["year"],
                                    rating=movie_item["rating"],
                                    genre_id=movie_item["genre_id"],
                                    director_id=movie_item["director_id"]
                                    ))

    try:
        db.session.commit()
    except IntegrityError:
        print("Fixtures already loaded")
