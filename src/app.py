from urllib import response
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import os

app = Flask(__name__)
mongo_uri = os.environ.get('MONGO_URI')
if mongo_uri is None:
    raise Exception('MONGO_URI is not set')
app.config['MONGO_URI']=mongo_uri
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
    name = request.json['name']
    lastname = request.json['lastname']
    email = request.json['email']
    birthdate = request.json['birthdate']
    phone_number = request.json['phone_number']
    address = request.json['address']
    historials = request.json['historials']

    if user_id and name and lastname and email and birthdate and phone_number and address:
        id = mongo.db.Profiles.insert_one(
            {
                'user_id': user_id,
                'name': name,
                'lastname': lastname,
                'email': email,
                'birthdate': birthdate,
                'phone_number': phone_number,
                'address': address,
                'historials': historials
            }
        )
        response = {
            'MESSAGE': 'Usuario INSERTADO con éxito.',
            'user_id': user_id,
            'name': name,
            'lastname': lastname,
            'email': email,
            'birthdate': birthdate,
            'phone_number': phone_number,
            'address': address,
            'historials': historials,
        }

        return response
    else:
        return not_found()

# --GET--: ALL PROFILES
@app.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = mongo.db.Profiles.find()
    response = json_util.dumps(profiles)
    return Response(response, mimetype='application/json')

# --GET--: PROFILE
@app.route('/profiles/<user_id>', methods=['GET'])
def get_profile(user_id):
    profile = mongo.db.Profiles.find_one({'_id': ObjectId(user_id)})
    response = json_util.dumps(profile)
    return Response(response, mimetype='application/json')

# --DELETE--: PROFILE
@app.route('/profiles/<user_id>', methods=['DELETE'])
def delete_profile(user_id):
    profile = mongo.db.Profiles.find_one({'_id': ObjectId(user_id)})
    mongo.db.Profiles.delete_one({'_id': ObjectId(user_id)})
    response = jsonify({'message': 'Usuario ' + user_id + ' (' + str(profile['name']) + ' ' + str(profile['lastname']) + ')' + ' ELIMINADO con éxito.'})
    return response

# --PUT--: PROFILE
@app.route('/profiles/<user_id>', methods=['PUT'])
def update_profile(user_id):
    phone_number = request.json['phone_number']
    address = request.json['address']
    historials = request.json['historials']

    if phone_number or address or historials:
        mongo.db.Profiles.update_one({'_id': ObjectId(user_id)}, {'$set': {
            'phone_number': phone_number,
            'address': address,
            'historials': historials
        }})

        response = jsonify({'message': 'Usuario ' + user_id + ' ACTUALIZADO con éxito.'})
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

