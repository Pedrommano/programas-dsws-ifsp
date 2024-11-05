from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    last_name = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua instituição de ensino:', validators=[DataRequired()])
    subject = SelectField('Informe a sua disciplina:', choices=["DSWA5", "DWBA4", "Gestão de Projetos"], validators=[DataRequired()])
    submit = SubmitField('Submit')
