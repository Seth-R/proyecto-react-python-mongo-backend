import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo, ObjectId
#
app = Flask(__name__)

app.config['MONGO_URI']='mongodb://localhost/pythonreactdb'#si la db no existe al hacer referencia a ella se creara una db
mongo = PyMongo(app)

CORS(app)
#"CORS se usa para no tener problemas con el servidor de react le pasamos la app con CORS(app)"

db = mongo.db.users

@app.route("/", methods=["GET"])
def index():
    return "Holis"

@app.route("/users", methods=["POST"])
def createUser():
    user = {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }
    try:
        usuario = db.insert_one(user)
    except Exception as e:
        print ("unexeptede error", type(e), e)
    #print(id)

    return jsonify(str(usuario.inserted_id))#, usuario.acknowledged
    #return "recived"

@app.route("/users", methods=["GET"])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route("/user/<id>", methods = ["GET"])
def getUser(id):
    user = db.find_one({"_id":ObjectId(id)})
    #print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })#jsonify(str(user))

@app.route("/user/<id>", methods=['DELETE'])
def deleteUser(id):
    if db.find_one({"_id": ObjectId(id)}) != None:
        db.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg":"usuario eliminado"})
    else:
        return "no existe usuario con ese id"


@app.route("/user/<id>", methods=["PUT"])
def updateUser(id):
    if db.find_one({"_id":ObjectId(id)}) != None:
        
        db.update_one({"_id": ObjectId(id)},{'$set':{
            'name': request.json['name'],
            'email':request.json['email'],
            'password':request.json['password']
        }})
        print (id)
        return jsonify({"msg":"usuario modificado"})
    else:
        return jsonify({"msg": "no se encontro el usuario con ese id"})


if __name__=="__main__":
    app.run(debug=True) #cáda vez que se haga un cambio en el codigo se reinicie por si solo         