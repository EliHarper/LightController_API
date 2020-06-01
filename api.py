from bson import json_util, BSON
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, request, Blueprint
from kafka import KafkaProducer
from decouple import config

from actions import apply
from application import create_app


app = create_app()
api = Blueprint("api", __name__)
app.register_blueprint(api, url_prefix="/api")

producer = KafkaProducer(bootstrap_servers=[config('KAFKA_URL')],
                         value_serializer=lambda x:
                         json_util.dumps(x).encode('utf-8'))

mongoClient = MongoClient([config('DB_URL')])
db = mongoClient.lightdb
scenes = db.scenes


@api.route('/scenes', methods=['GET'])
def home():
    docs = scenes.find()
    return json_util.dumps(docs)


@api.route('/scene/create', methods=['POST', 'OPTIONS'])
def createScene():
    if request.method == 'OPTIONS':
        return "ok"

    jsonDoc = request.get_json()
    newId = scenes.insert_one(jsonDoc).inserted_id
    return str(newId)


@api.route('/scene/<string:scene_id>', methods=['GET'])
def applyScene(scene_id):
    print("Hit function")
    toApply = scenes.find_one({"_id": ObjectId(scene_id)})
    producer.send('applyScene', toApply)
    print("applied")
    return "applied"

@api.route('/scene/<string:scene_id>', methods=['DELETE', 'OPTIONS'])
def deleteScene(scene_id):
    # import pdb; pdb.set_trace()
    if request.method == 'OPTIONS':
        return "ok"

    scenes.delete_one({'_id': ObjectId(scene_id)})
    return "done"


app.register_blueprint(api, url_prefix="/api")
app.run(host='0.0.0.0')
