from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
custom_salt = "pbkdf2:sha256"


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.secret_key = 'secret-key-goes-here'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


# CREATE TABLE IN DB
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html", fail=False)
    else:
        try:
            hashed_password = generate_password_hash(request.form['password'], salt_length=8)
            new_user = User(email=request.form['email'],
                            password=hashed_password,
                            name=request.form['name'])
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('secrets', user_id=new_user.name, _external=True))
        except IntegrityError:
            flash('Already registered!', 'error')
            return render_template("login.html")

@login_manager.user_loader
def load_user(user_id):
    # Retrieve the user from the database based on the user ID
    user = User.query.get(int(user_id))
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets', user_id=user.name, _external=True))
        else:
            flash('Invalid username or password', 'error')
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    user_name = request.args.get('user_id')
    user = db.session.execute(db.select(User).where(User.name == user_name)).scalar()
    return render_template("secrets.html", user=user, _external=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(
        'static', 'files/cheat_sheet.pdf', as_attachment=True
    )
    pass


if __name__ == "__main__":
    app.run(debug=True)
