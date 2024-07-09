from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(80), unique=True, nullable=False)
#     author = db.Column(db.String(80), nullable=False)
#     rating = db.Column(db.Float, nullable=False)


@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books, book_length=len(books))


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST' and request.form['name'].strip():
        with app.app_context():
            new_book = Book(title=request.form['name'], author=request.form['author'], rating=request.form['rating'])
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id):
    with app.app_context():
        book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        if request.method == 'POST':
            book_to_update.rating = request.form['rating']
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('edit.html', book=book_to_update)


@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
    with app.app_context():
        book_to_delete = return_entry(id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))



def return_entry(id):
    return db.session.execute(db.select(Book).where(Book.id == id)).scalar()

if __name__ == "__main__":
    app.run(debug=True)
