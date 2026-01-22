from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(),
        Length(min=3, message="Name must be at least 3 characters")
    ])

    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Invalid email address")
    ])

    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters")
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match")
    ])

    submit = SubmitField("Sign Up")



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Enter a valid email")
    ])

    password = PasswordField("Password", validators=[
        DataRequired()
    ])

    submit = SubmitField("Login")