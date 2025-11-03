from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired, Length(min=3, max=30)])
    email = StringField("Email", validators=[DataRequired, Email])
    password = PasswordField("Password", validators=[DataRequired, Length(min=12)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired, EqualTo("password", message="Must match original password")])
    bio = TextAreaField("Enter something about yourself")


