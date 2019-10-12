from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Optional, URL, EqualTo


class ProfileForm(FlaskForm):
    nickname = StringField("Nickname",validators=[DataRequired(), Length(1,16)])
    github = StringField("Github", validators=[Optional(), URL(), Length(1, 120)])
    website = StringField("Website", validators=[Optional(),URL(), Length(1, 120)])
    bio = TextAreaField("About yourself", validators=[Optional(), Length(1,120)])


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("remember me")
    submit = SubmitField("Log me in")


class RegisterForm(FlaskForm):
    nickname = StringField("Nickname", validators=[DataRequired(), Length(1,16)])
    email = StringField('email', validators=[DataRequired(), Length(1,12), Email()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Register")