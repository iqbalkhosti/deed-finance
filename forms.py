from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import (DataRequired, Email, Length, EqualTo)

class SignupForm(FlaskForm):



    first_name = StringField(
        
        "First Name",
        validators=[DataRequired(), Length(min=2, max=100, message="Please enter a valid first name, between 2 and 100 characters.")]
    )
    surname = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=2, max=100, message="A valid last name is required, between 2 and 100 characters.")]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Please enter a valid email address.")]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=256, message="Password must be more than 8 characters.")]
    )

    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )

    submit = SubmitField(
        "Sign Up")
    
class LoginForm(FlaskForm):
        email = StringField(
            "Email",
            validators=[DataRequired(), Email(message="Please enter a valid email address.")]
        )
        password = PasswordField(
            "Password",
            validators=[DataRequired(), Length(min=8, max=256, message="Password must be more than 8 characters.")]
        )
        submit = SubmitField("Login")


class VerificationForm(FlaskForm):
    """Form for entering email verification code."""
    code = StringField(
        "Verification Code",
        validators=[DataRequired(), Length(min=6, max=6, message="Please enter the 6-digit code.")]
    )
    submit = SubmitField("Verify Email")