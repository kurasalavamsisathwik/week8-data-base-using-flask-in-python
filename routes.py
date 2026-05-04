from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import User, Post
from app.forms import RegisterForm, LoginForm, PostForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Create Blueprint
main = Blueprint('main', __name__)


# ------------------ HOME ------------------
@main.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)


# ------------------ REGISTER ------------------
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


# ------------------ LOGIN ------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


# ------------------ LOGOUT ------------------
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('main.home'))


# ------------------ CREATE POST ------------------
@main.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )

        db.session.add(post)
        db.session.commit()

        flash('Post created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', form=form)