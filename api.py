from actions import apply
from bson import json_util, BSON
from flask import Flask
from flask import request
from flask_cors import CORS
from kafka import KafkaProducer
from pymongo import MongoClient

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

mongoClient = MongoClient()
db = mongoClient.lightdb
scenes = db.scenes


@app.route('/', methods=['GET'])
def home():
    docs = scenes.find()
    return json_util.dumps(docs)


@app.route('/scene/create', methods=['POST', 'OPTIONS'])
def createScene():
    # import pdb; pdb.set_trace()
    jsonDoc = request.json.get('scene')
    print('jsonDoc: %', jsonDoc)
    bsonDoc = BSON.encode(jsonDoc)
    print('bsonDoc: %', bsonDoc)
    newId = scenes.insert_one(bsonDoc).inserted_id
    return newId
    # scene_id = scenes.insert_one()


@app.route('/scene/<int:scene_id>')
def applyScene(scene_id):
    toApply = scenes.find_one({"_id": scene_id})
    toApply = BSON.decode(toApply)
    apply(toApply)


app.run(host='0.0.0.0')
