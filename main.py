from datetime import date
from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from ignored.secret import the_secret

app = Flask(__name__)
app.config['SECRET_KEY'] = the_secret()
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configures Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


# Creates the user_callback
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(500), nullable=False)

    # Refers to tablename in User class 'users'.
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Refers to property in User class 'posts'
    author = relationship('User', back_populates='posts')

    # Refers to property in Comment class 'parent_post'.
    comments = relationship('Comment', back_populates='parent_post')


# User class adds a User table to the DB.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    # Refers to property in BlogPost class 'author'
    posts = relationship('BlogPost', back_populates='author')

    # Refers to property in Comment class 'comment_author'.
    comments = relationship('Comment', back_populates='comment_author')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    # Refers to tablename in User class 'users'.
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Refers to property in User class 'comments'.
    comment_author = relationship('User', back_populates='comments')

    # Refers to tablename in BlogPost class 'blog_posts'.
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))

    # Refers to property in BlogPost class 'comments'.
    parent_post = relationship('BlogPost', back_populates='comments')


with app.app_context():
    db.create_all()


gravatar = Gravatar(
    app,
    size=100,
    rating='g',
    default='retro',
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None
)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new User to the Database. Salting and Hashing passwords utilized."""
    form = RegisterForm()
    if form.validate_on_submit():

        # Check to see if the user is already in the Database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash('This email is already registered! Please register a different email address or ')
            return redirect(url_for('register'))

        hash_and_salted_pw = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_pw
        )
        db.session.add(new_user)
        db.session.commit()

        # Authenticates the user with Flask-login.
        login_user(new_user)

        return redirect(url_for('get_all_posts'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in the user by checking the email and hashed password in the Database
    match the input by the user for Authentication
    :return: The login page for GET or redirects to all posts after user login is successful for POST
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user or not check_password_hash(user.password, password):
            flash("Email or Password is incorrect. Please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logs out the current user."""
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    """Renders all the posts on the home page."""
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template('index.html', all_posts=posts)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    """Grabs the post by ID once clicked on and shows the comment section."""
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()

    # Only allow logged-in users to comment on posts
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login to leave comments.")
            return redirect(url_for('login'))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template('post.html', post=requested_post, form=comment_form)


def admin_only(func):
    """Admin Only Decorator."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return func(*args, **kwargs)

    return decorated_function


@app.route('/new-post', methods=['GET', 'POST'])
@admin_only
def add_new_post():
    """Creates a new post by the user once submitted and redirects user to the index page."""
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime('%B %d, %Y')
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form, current_user=current_user)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@admin_only
def edit_post(post_id):
    """Allows the user to edit the post."""
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    return render_template('make-post.html', form=edit_form, is_edit=True, current_user=current_user)


@app.route('/delete/<int:post_id>')
@admin_only
def delete_post(post_id):
    """Allows user to delete the post."""
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# The About Me Page.
@app.route('/about')
def about():
    return render_template('about.html')


# The Contact Me Page.
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, port=5002)
