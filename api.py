import json

from bson import json_util, BSON
from bson.objectid import ObjectId
from pymongo import MongoClient, ASCENDING
from flask import Flask, request, Blueprint
from kafka import KafkaProducer
from decouple import config

from application import create_app


class Message:
    def __init__(self, functionCall = 'off', value=''):
        self.functionCall = functionCall
        self.value = value



app = create_app()
api = Blueprint("api", __name__)
app.register_blueprint(api, url_prefix="/api")

mongoClient = MongoClient([config('DB_URL')])
mongoClient.server_info()
db = mongoClient.lightdb
scenes = db.scenes

producer = KafkaProducer(bootstrap_servers=[config('KAFKA_URL')],
                         value_serializer=lambda x:
                         json_util.dumps(x).encode('utf-8'))


@api.route('/scenes', methods=['GET'])
def home():
    docs = scenes.find().sort([("index", ASCENDING)])
    return json_util.dumps(docs)


@api.route('/off', methods=['GET'])
def off():
    msg = Message()
    producer.send('applyScene', msg.__dict__)
    return 'Turned off.'

@api.route('/scene/<string:scene_id>', methods=['GET'])
def applyScene(scene_id):
    print("Hit function")
    toApply = scenes.find_one({"_id": ObjectId(scene_id)})
    future = producer.send('applyScene', toApply)
    print (future.__dict__)
    print("applied")
    return "applied"


@api.route('/scene/create', methods=['POST', 'OPTIONS'])
def createScene():
    if request.method == 'OPTIONS':
        return "ok"

    jsonDoc = request.get_json()
    newId = scenes.insert_one(jsonDoc).inserted_id
    return str(newId)


@api.route('/scene/<string:scene_id>', methods=['DELETE', 'OPTIONS'])
def deleteScene(scene_id):
    # import pdb; pdb.set_trace()
    if request.method == 'OPTIONS':
        return "ok"

    scenes.delete_one({'_id': ObjectId(scene_id)})
    return "done"


@api.route('/indices/edit', methods=['PUT', 'OPTIONS'])
def putIndices():
    if request.method == 'OPTIONS':
        return "ok"

    updatedScenes = request.get_json()
    scene_ids_and_indices = dict()
    try:
        for scene in updatedScenes:
            oid = scene.pop("_id", None)
            id = oid.pop("$oid", None)
            if id is None:
                raise Exception("No _id value found in object {}".format(scene))
            else:
                index = scene.pop("index", None)
                if index is None:
                    raise Exception("No index value found in object {}".format(scene))
                print('scene_id: {}'.format(id))
                scene_ids_and_indices[id] = index
                print('index: {}'.format(index))
    except Exception as e:
        print('caught exception: {}'.format(e))

    print('past except')
    for scene_id, scene_index in scene_ids_and_indices.items():
        # query = {'_id': ObjectId(scene_id)}
        # setIndex = {"$set": {"index": scene_index}}
        result = scenes.update_one({'_id': ObjectId(scene_id)}, {"$set": {"index": int(scene_index)}})
        print('result of updating scene with id {} to have index {}: \n{}'.format(scene_id, scene_index, result.raw_result))

    return "done"


@api.route('/scene/edit', methods=['PUT', 'OPTIONS'])
def updateScene():
    if request.method == 'OPTIONS':
        return "ok"

    updated = request.get_json()
    try:
        id = updated.pop("_id", None)
        if id is None:
            raise Exception("No _id value found in updated object")
    except Exception as e:
        print(e.args)
    query = {'_id': ObjectId(id['$oid'])}
    newVal = {"$set": updated}
    scenes.update_one(query, newVal)
    return "done"

@api.route('/brightness/<string:brightness>', methods=['GET'])
def updateBrightness(brightness):
    msg = Message(functionCall='update_brightness', value=brightness)
    producer.send('applyScene', msg.__dict__)
    return "done"


app.register_blueprint(api, url_prefix="/api")
app.run(host='0.0.0.0', port=5001)