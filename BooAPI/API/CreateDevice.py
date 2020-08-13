from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length

class Create_Device(FlaskForm):
	name = StringField('Device name', validators=[DataRequired()])
	value = StringField('Value', validators=[DataRequired()])
	#value_type = StringField('Value type', validators=[DataRequired()])
	value_type = SelectField('Value Type',choices=["string","integer","boolean","floating point","image"], validators=[DataRequired()])
	description = TextAreaField('Description')

	submit = SubmitField('submit')