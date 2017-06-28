from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_httpauth import HTTPBasicAuth
from Model import Process
auth = HTTPBasicAuth()

app = Flask(__name__)

global processo
global entrada
global recomendation_points

recomendation_points = {}
processo = None
entrada = []

@app.route('/')
@auth.login_required
def index():
    return ("Bem vindo ao web service do SEEC %s" % auth.username())


#curl -i -H "Content-Type: application/json" -X POST -d "{"""dominio""":"""d(a,b,c,d,e)""", """regras""":"""o(d;e)"""}" http://localhost:5000/tarefas/add
@app.route('/tarefas/add', methods=['POST'])
def adicionar_entrada():
    global processo
    global entrada
    global recomendation_points

    req = None
    try:
        req = request.get_json(force=True)
    except:
        abort(400)

    if not 'dominio' in req:
        abort(400)

    dominio = req['dominio']
    regras = req['regras']
    regras = regras.split("|")
    print(regras)
    entrada = []
    entrada.append(dominio)
    for reg in regras:
        entrada.append(reg)

    processo = Process.Process(entrada)
    processo.carregar()

    return jsonify({'status': 'ok'}), 201


#curl -i http://localhost:5000/tarefas/ultima_recomendacao
@app.route('/tarefas/ultima_recomendacao', methods=['GET'])
def get_ultima_recomendacao():
    global processo
    global entrada
    global recomendation_points
    if processo == None:
        abort(410)
    if len(recomendation_points) == 0:
        recomendation_points['rp1'] = processo.step_2()

    return jsonify({'recomendacao': recomendation_points})


# Sistema de Login
@auth.get_password
def get_password(username):
    if username == 'padrao':
        return 'padrao'
    return False

#
# Erros
#
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
@app.errorhandler(410)
def not_found(error):
    return make_response(jsonify({'error': 'Process not started'}), 410)



if __name__ == '__main__':
    app.run(debug=True)