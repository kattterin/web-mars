from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, SelectField, IntegerField, \
    DateTimeField, BooleanField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional


class JobForm(FlaskForm):
    team_leader = SelectField("Руководитель", coerce=int, validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы в часах', validators=[DataRequired()])

    collaborators = StringField('Список d участников')
    start_date = DateTimeLocalField("Дата начала", format="%Y-%m-%dT%H:%M", validators=[Optional()])
    end_date = DateTimeLocalField("Дата конца", format="%Y-%m-%dT%H:%M", validators=[Optional()])
    is_finished = BooleanField('Признак завершения')

    submit = SubmitField('Создать')
