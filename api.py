import re
from bson import json_util
from bson.objectid import ObjectId
from decouple import config
from flask import request, Blueprint
from google import protobuf
from pymongo import MongoClient, ASCENDING

from application import create_app
import executor_client


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



@api.route('/scenes', methods=['GET'])
def home():
    docs = scenes.find().sort([("index", ASCENDING)])
    return json_util.dumps(docs)


@api.route('/off', methods=['GET'])
def off():
    msg = Message()
    executor_client.send_grpc(msg.__dict__)
    return 'Turned off.'

@api.route('/scene/<string:scene_id>', methods=['GET'])
def applyScene(scene_id):
    print("Hit function")
    toApply = scenes.find_one({"_id": ObjectId(scene_id)})
    future = executor_client.send_grpc(toApply)
    print (future)
    print("applied")
    return "applied"


@api.route('/scene/name/<string:scene_name>', methods=['GET'])
def applySceneByName(scene_name):
    splitName = scene_name.replace('_', ' ')
    toApply = scenes.find_one({"name": re.compile(splitName, re.IGNORECASE)})
    future = executor_client.send_grpc(toApply)
    print (future.__dict__)
    print('applied')
    return 'applied'


@api.route('/ambilight/on', methods=['GET'])
def applyAmbiLight():
    print('applying ambilight')
    future = executor_client.send_stream()
    print('future: \n{}\n\n'.format(future))
    return 'applied'


@api.route('/ambilight/off', methods=['GET'])
def removeAmbiLight():
    executor_client.ambi.on = False
    msg = Message()
    executor_client.send_grpc(msg.__dict__)
    return 'Turned off.'


@api.route('/scene/create', methods=['POST', 'OPTIONS'])
def createScene():
    if request.method == 'OPTIONS':
        return "ok"

    jsonDoc = request.get_json()
    newId = scenes.insert_one(jsonDoc).inserted_id
    return str(newId)


@api.route('/scene/<string:scene_id>', methods=['DELETE', 'OPTIONS'])
def deleteScene(scene_id):
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
    response = executor_client.send_grpc(msg.__dict__)
    print('Response to updated brightness: {}'.format(response))
    return "done"


app.register_blueprint(api, url_prefix="/api")
app.run(host='0.0.0.0', port=5001)