from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util #para transformar los bson de Mongo en json
from bson.objectid import ObjectId

#configurar conexion a bbdd
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pythonmongodb"
mongo = PyMongo(app)

#como ya tenemos la conexion, empezamos con nuestras rutas
#primero ruta para poder crear usuarios
@app.route('/users', methods=['POST'])
def create_user():
    #Receiving data
    #request.json es un objeto
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        #para cifrar la contraseña del  usuario
        hased_password = generate_password_hash(password)
        #de la vble mongo.propiedad db. crea una coleccion users cuando introduzca un  usuario
        id = mongo.db.users.insert(
            {'username': username, 'password': hased_password, 'email':email}
        )
        response = {
            'id': str(id),
            'username': username,
            'password': hased_password,
            'email': email,
        }
        return response
    else: 
        return not_found()

    return {'message': 'received'}

#para listar los elementos:
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)#de la funcion json_util cojo el método dumps() y le paso la variable users en la que se almacenaban los datos tipo bson
    return Response(response, mimetype='aplication/json')

#para mostrar un solo elemento:
@app.route('/users/<id>', methods =['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='aplication/json')

#para eliminar un usuario:
@app.route('/users/<id>', methods =['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User ' + id + ' was Deleted successfully'})
    return response

#para editar o actualizar un dato:
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hased_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set':{
            'username': username,
            'password': password,
            'email': email
        }})
        response = jsonify({'message': 'User ' + id + 'was updated sucessfully'})
        return response

@app.errorhandler(404)
def not_found(error=None):
    #jsonify() es una función
    response = jsonify({
        'message': 'Reasource not found' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response




if __name__ == "__main__":
    app.run(debug=True) #es como un servidor|cada vez que note un cambio reinicie