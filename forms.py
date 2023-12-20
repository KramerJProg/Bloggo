from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


# WTForm for creating a Blog Post.
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# WTForm for Registering a User.
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[Email("Must be a valid email address, i.e. your_email@email.com"), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Up!")


# WTForm for Logging in a User.
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email("Must be a valid email address, i.e. your_email@email.com"), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In!")


# WTForm for Commenting on Posts.
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comments", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")



