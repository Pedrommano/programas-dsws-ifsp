import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))
    
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for, flash, request
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chave forte'

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    sobrenome = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    instituicao = StringField('Informe a sua Instituição de ensino:', validators=[DataRequired()])
    disciplina = SelectField('Informe a sua disciplina:', choices=[('DSWA5', 'DSWA5')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Parece que você alterou seu nome!')
        
        # Salvando dados no session
        session['name'] = form.name.data
        session['sobrenome'] = form.sobrenome.data
        session['instituicao'] = form.instituicao.data
        session['disciplina'] = form.disciplina.data
        
        return redirect(url_for('index'))

    # Captura o IP e o host
    ip_remoto = request.remote_addr
    host_app = request.host

    # Define o start_time na sessão caso ainda não esteja definido
    if 'start_time' not in session:
        session['start_time'] = datetime.now().isoformat()
    
    # Carrega o start_time e calcula a diferença de tempo
    start_time = datetime.fromisoformat(session['start_time'])
    now = datetime.now()
    time_elapsed = now - start_time

    # Passa 'now', 'start_time' e 'time_elapsed' para o template
    return render_template(
        'index.html', 
        form=form, 
        name=session.get('name'), 
        sobrenome=session.get('sobrenome'),
        instituicao=session.get('instituicao'), 
        disciplina=session.get('disciplina'), 
        ip_remoto=ip_remoto, 
        host_app=host_app, 
        now=now,
        start_time=start_time,
        time_elapsed=time_elapsed
    )

if __name__ == '__main__':
    app.run(debug=True)
