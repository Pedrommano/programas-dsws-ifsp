from __future__ import print_function
from flask import Flask, request, render_template, session, redirect, url_for, flask
from flask_moment import Moment
# from datetime import datetime, UTC
from datetime import datetime
from forms import NameForm
import sys

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'chave-forte'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
   now = datetime.utcnow()
#    now = datetime.now(UTC)
   form = NameForm()
   ip = None
   host = None
  
   if form.validate_on_submit():
       print(form.subject.data, file=sys.stderr)
       old_name = session.get('name')
       if old_name is not None and old_name != form.name.data:
           flash('Você alterou o seu nome!')
       session['name'] = form.name.data
       session['institution'] = form.institution.data
       session['subject'] = form.subject.data

       form.name.data = ''
       ip = request.remote_addr
       host = request.host
    #    return redirect(url_for('index'))
   return render_template('index.html', current_time=now, form=form, name=session.get('name'), ip=ip, host=host, institution=session.get('institution'), subject=session.get('subject'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_internal_server_error(e):
    return render_template('500.html'), 500
