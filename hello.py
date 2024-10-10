from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Avaliação contínua: Aula 030</h1><ul><li><a href="/">Home</a></li><li><a href="/user/Fabio%20Teixeira/PT23820X/IFSP">Identificação</a></li><li><a href="/contextorequisicao">Contexto da requisição</a></li></ul>'

@app.route('/user/<name>/<register>/<institution>')
def user(name, register, institution):
    return '<h1>Avaliação Contínua: Aula 030</h1><h1>Aluno: {n}</h1><h1>Prontuário: {r}</h1><h1>Instituição: {i}</h1> <a href="/">Voltar</a>'.format(n = name, r=register, i=institution)
 

@app.route('/contextorequisicao')
def contexto_requisicao():
  browser = request.headers.get('User-Agent')
  ip = request.remote_addr
  host = request.headers.get('Host')
  return '<h1>Avaliação Contínua: Aula 030</h1><h1>Seu navegador é: {}</h1><h1>O IP do computador remoto é: {}</h1><h1>O host da aplicação é: {}</h1><a href="/">Voltar</a>'.format(browser, ip, host)
