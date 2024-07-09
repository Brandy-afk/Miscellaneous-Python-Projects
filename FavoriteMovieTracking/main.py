from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

bootstrap = Bootstrap5(app)


# CREATE DB
class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired(),
                                              NumberRange(min=0, max=10, message='Rating must be between 0 and 10')])
    review = StringField('Review', validators=[DataRequired()])
    img_url = URLField('Movie Image', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


class UpdateForm(FlaskForm):
    rating = FloatField('New Rating')
    img_url = URLField('New Image')
    submit = SubmitField('Update Movie')


class Movie(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(db.String, nullable=False)
    year: Mapped[int] = mapped_column(db.Integer, nullable=False)
    description: Mapped[str] = mapped_column(db.String, nullable=False)
    rating: Mapped[float] = mapped_column(db.Float, nullable=False)
    ranking: Mapped[int] = mapped_column(db.Integer, nullable=False)
    review: Mapped[str] = mapped_column(db.String, nullable=False)
    img_url: Mapped[str] = mapped_column(db.String, nullable=False)


@app.route("/")
def home():
    with app.app_context():
        movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars()
        return render_template("index.html", movies=movies)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = MovieForm()
    if form.validate_on_submit():
        with app.app_context():
            movie = Movie(title=form.title.data, year=form.year.data, description=form.description.data,
                          rating=form.rating.data, review=form.review.data, img_url=form.img_url.data)
            db.session.add(movie)
            db.session.commit()
            organize_rankings()
            return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/movies/<ranking>', methods=['GET', 'POST'])
def edit(ranking):
    form = UpdateForm()
    with app.app_context():
        edited_movie = return_movie(ranking)
        if form.validate_on_submit():
            if form.img_url.data:
                edited_movie.img_url = form.img_url.data
            if form.rating.data:
                edited_movie.rating = form.rating.data

            db.session.commit()
            organize_rankings()

            return redirect(url_for('home'))
        return render_template('edit.html', movie=edited_movie, form=form)


@app.route('/delete/<ranking>', methods=['GET', 'POST'])
def delete(ranking):
    with app.app_context():
        movie = return_movie(ranking)
        delete_entry(movie)
        organize_rankings()
        return redirect(url_for('home'))


def delete_entry(movie):
    db.session.delete(movie)
    db.session.commit()


def organize_rankings():
    with app.app_context():
        movies = db.session.execute(db.select(Movie).order_by(desc(Movie.rating))).scalars()
        i = 0
        for movie in movies:
            i += 1
            if i > 10:
                delete_entry(movie)
                continue
            elif movie.ranking is not i:
                movie.ranking = i

        db.session.commit()

def return_movie(ranking):
    return db.session.execute(db.select(Movie).where(Movie.ranking == ranking)).scalar()


if __name__ == '__main__':
    app.run(debug=True)
