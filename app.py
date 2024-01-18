from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb+srv://angeldaw1:Pal0meras@concesionario.aoppurt.mongodb.net/concesionario'

mongo = PyMongo(app)

@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    usuario = mongo.db.users.find_one({'_id': ObjectId(id)})
    
    if usuario:
        response = {
            'id': str(usuario['_id']),
            'nomusuario': usuario['nomusuario'],
            'passw': usuario['passw'],
            'email': usuario['email']
        }
        return jsonify(response)
    else:
        return not_found()


@app.route('/users', methods=['POST'])
def create_user():

    request_data = request.get_json()

    if 'nomusuario' in request_data:
        nomusuario = request.json['nomusuario']
    else:
        return datos_incompletos()
    
    if 'email' in request_data:
        email = request.json['email']
    else:
        return datos_incompletos()
    
    if 'passw' in request_data:
        passw = request.json['passw']
        hashed_password = generate_password_hash(passw)
    else:
        return datos_incompletos()
    
    id = mongo.db.users.insert_one({'nomusuario': nomusuario, 'email': email, 'passw': hashed_password})

    response = {
        'id': str(id.inserted_id),
        'nomusuario': nomusuario,
        'passw': hashed_password,
        'email': email
    }
    return response


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    usuario = mongo.db.users.find_one({'_id': ObjectId(id)})
    
    if usuario:
        usuarioborrar = mongo.db.users.delete_one({'_id': ObjectId(id)})
        response = jsonify({'mensaje': 'Usuario ' + id + ' fue eliminado satisfactoriamente'})
        return response
    else:
        return not_found()
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'mensaje': 'Recurso no encontrado: ' + request.url,
        'status': 404
    })
    response.status_code = 404

    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):

    request_data = request.get_json()

    if 'nomusuario' in request_data:
        nomusuario = request.json['nomusuario']
    else:
        return datos_incompletos()
    
    if 'email' in request_data:
        email = request.json['email']
    else:
        return datos_incompletos()
    
    if 'passw' in request.json:
        passw = request.json['passw']
        hashed_password = generate_password_hash(passw)
    else:
        return datos_incompletos()
    
    usuario = mongo.db.users.find_one({'_id': ObjectId(id)})

    if usuario:
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set':
                                                          {
                                                              'nomusuario': nomusuario,
                                                              'passw': hashed_password,
                                                              'email': email
                                                          }})
    else:
        return not_found()
    
    response = jsonify({'mensaje': 'Usuario' + id + ' fue actualizado satisfactoriamente.'})

    return response


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'mensaje': 'Recurso no encontrado: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

@app.errorhandler(400)
def datos_incompletos(error=None):
    response = jsonify({
        'mensaje': 'Datos incompletos: nomusuario, email y/o passw',
        'satus': 400
    })
    response.status_code = 400
    return response

if __name__ == "__main__":
    app.run(debug=True)