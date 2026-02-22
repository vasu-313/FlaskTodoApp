from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField , DecimalField, BooleanField,TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

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




class TimesheetForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    project = SelectField("Project", coerce=int)
    taskType = RadioField(
        "Task Type",
        choices=[
            ("General Tasks", "General Tasks"),
            ("MPP Tasks", "MPP Tasks"),
            ("Assigned Tasks", "Assigned Tasks"),
            ("Issues Assigned", "Issues Assigned")
        ],
        validators=[DataRequired()]
    )

    task = SelectField("Task", coerce=int)
    activity = SelectField("Activity", coerce=int)

    time = DecimalField("Actual Work (hrs)",
                        validators=[DataRequired(), NumberRange(min=0)])

    overtime = DecimalField("OverTime (hrs)",
                            validators=[NumberRange(min=0)])

    holiday = BooleanField("Holiday")

    description = TextAreaField("Description")


    submit = SubmitField("Save")

