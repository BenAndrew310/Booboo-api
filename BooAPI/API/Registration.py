from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError
from API.models import User

class Signup(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),Length(min=4,max=20)])
	email    = StringField('Email',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
			validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That username is already taken.")

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That email is already taken.")

class Login(FlaskForm):
	auth = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember me')

	submit = SubmitField('Login')

class ChangeUserInformation(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),Length(min=4,max=20)])
	email    = StringField('Email',validators=[DataRequired()])

	submit = SubmitField('Submit')