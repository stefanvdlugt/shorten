from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class SetupForm(FlaskForm):
    username = StringField('Admin username', validators=[DataRequired()])
    password = PasswordField('Admin password', validators=[DataRequired()])
    password2 = PasswordField('Repeat admin password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
