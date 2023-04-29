from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, SelectField, IntegerField, \
    DateTimeField, BooleanField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional


class DepartForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    chief = SelectField('Шеф', coerce=int, validators=[DataRequired()])
    members = StringField('Список участников', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired()])
    submit = SubmitField('Добавить')

