from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re

reserved_usernames = {"admin", "root", "superuser"}
common_password = {"password123", "admin", "123456", "qwerty", "letmein", "welcome", "iloveyou", "abc123", "monkey", "football"}

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=12)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Must match original password")])
    bio = TextAreaField("Enter something about yourself")
    submit = SubmitField("Submit")

    def validate_username(self, username):
        if not re.match(r"^[A-Za-z_]+$", username.data):
            raise ValidationError("Username must only contain letters and underscores")
        if username.data.lower() in reserved_usernames:
            raise ValidationError("Username is reserved")

    def validate_email(self, email):
        lower = email.data.lower()
        if not re.match(r'.+@.+\.(edu|ac\.uk|org)$', lower):
            raise ValidationError('Only .edu, .ac.uk, or .org emails are allowed.')

    def validate_password(self, password):
        password = password.data
        username = self.username.data.lower()
        email = self.email.data.lower()

        if len(password) < 12:
            raise ValidationError("Password must be at least 12 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain a capital letter")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain a lowercase letter")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain a number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain a special character")
        if re.search(r'\s', password):
            raise ValidationError("Password cannot contain whitespace")
        if username in password.lower():
            raise ValidationError("Password cannot contain your username")
        if email in password.lower():
            raise ValidationError("Password cannot contain your email")
        if password.lower() in common_password:
            raise ValidationError("Password cannot be in list of common passwords")
