from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.datetime import DateTimeField, DateField
from wtforms.fields.simple import TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional


class OrganizationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Optional()])
    active_date = DateField('Active Date', validators=[DataRequired()])
    is_active = BooleanField('Is Active', default=True)
    location = StringField('Location', validators=[Optional(), Length(max=256)])
    submit = SubmitField('Create')
