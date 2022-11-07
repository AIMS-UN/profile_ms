import mimetypes
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import os

from models.profile import profileModel
from models.historial import historialModelforUser

app = Flask(__name__)
mongo_uri = os.environ.get('MONGO_URI')
if mongo_uri is None:
    raise Exception('MONGO_URI is not set')
app.config['MONGO_URI'] = mongo_uri
mongo = PyMongo(app)

# ---- PROFILES ROUTES ----

# DEFAULT GET


@app.route('/', methods=['GET'])
def default():
    return jsonify({'message': 'Bienvenido al microservicio aims_profile_ms!!!'})

# --POST--: PROFILE

@app.route('/profiles', methods=['POST'])
def create_profile():
    user_id = request.json['user_id']
    doc_id = request.json['doc_id']
    name = request.json['name']
    lastname = request.json['lastname']
    email = request.json['email']
    birthdate = request.json['birthdate']
    phone_number = request.json['phone_number']
    address = request.json['address']
    historials = request.json['historials']

    if user_id is not None and doc_id is not None and name is not None and lastname is not None and email is not None and birthdate is not None:
        mongo.db.Profiles.insert_one(
            profileModel(user_id, doc_id, name, lastname, email, birthdate,
                         phone_number, address, historials)
        )
        response = profileModel(
            user_id, doc_id, name, lastname, email, birthdate, phone_number, address, historials)

        return Response(response, status=201, mimetype='application/json')
    else:
        return not_found()

# --GET--: ALL PROFILES


@app.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = mongo.db.Profiles.find()
    if profiles == None:
        response = json_util.dumps({"message": "No hay usuarios registrados."})
        result = Response(response, status=204, mimetype='application/json')
    else:
        response = json_util.dumps(profiles)
        result = Response(response, status=200, mimetype='application/json')
    return result
# --GET--: PROFILE


@app.route('/profiles/<user_id>', methods=['GET'])
def get_profile(user_id):
    profile = mongo.db.Profiles.find_one({'user_id': user_id})
    if profile == None:
        response = json_util.dumps({"message": "Usuario no encontrado."})
        result = Response(response, status=200, mimetype='application/json')
    else:
        response = json_util.dumps(profile)
        result = Response(response, status=200, mimetype='application/json')
    return result

# --GET--: PROFILE/HISTORIAL


@app.route('/profiles/<user_id>/historial', methods=['GET'])
def get_profile_historial(user_id):
    profile = mongo.db.Profiles.find_one({'user_id': user_id})
    if profile == None:
        response = json_util.dumps({"message": "Usuario no encontrado."})
        result = Response(response, status=204, mimetype='application/json')
    else:
        historial = profile['historials'][0]
        response = json_util.dumps(historialModelforUser(
            profile["user_id"], historial['career'], historial['GPA'], historial['coursed_credits'], historial['approved_credits'], historial['reprobed_credits']))
        result = Response(response, status=200, mimetype='application/json')
    return result

# --DELETE--: PROFILE


@app.route('/profiles/<user_id>', methods=['DELETE'])
def delete_profile(user_id):
    profile = mongo.db.Profiles.find_one({'user_id': user_id})
    mongo.db.Profiles.delete_one({'user_id': user_id})
    response = jsonify({'message': 'Usuario ' + user_id + ' (' + str(
        profile['name']) + ' ' + str(profile['lastname']) + ')' + ' ELIMINADO con éxito.'})
    return response

# --PUT--: PROFILE


@app.route('/profiles/<user_id>', methods=['PUT'])
def update_profile(user_id):
    phone_number = request.json['phone_number']
    address = request.json['address']
    historials = request.json['historials']

    if phone_number or address or historials:
        mongo.db.Profiles.update_one({'user_id': user_id}, {'$set': {
            'phone_number': phone_number,
            'address': address,
            'historials': historials
        }})

        response = jsonify(
            {'message': 'Usuario ' + user_id + ' ACTUALIZADO con éxito.'})
        return response

# ERROR HANDLING


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'One or multiple resources Not Found: ' + request.url,
        'status': 404
    })

    response.status_code = 404

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
