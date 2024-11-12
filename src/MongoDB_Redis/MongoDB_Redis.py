from flask import Flask, abort, request, jsonify
from pymongo import MongoClient
from bson import json_util
from bson import ObjectId
import requests
import logging
import redis
import json
import os

app = Flask(__name__)

# MongoDB Setting
MongoDB_USERNAME = "<UserName>"
MongoDB_PASSWORD = "<Password>"
MongoDB_HOST = "<HOST>"
MongoDB_PORT = "<Port>" # Default Port Number : 27017
CERT_FILE = "global-bundle.pem"

# Redis Setting
Redis_HOST = "<HOST>"
Redis_PORT = "<Port>" # Default Port Number : 6379

def mongodb_connection():
    global MongoDB_USERNAME, MongoDB_PASSWORD, MongoDB_HOST, MongoDB_PORT
    download_global_pem()

    mongodb_client = MongoClient(f"mongodb://{MongoDB_USERNAME}:{MongoDB_PASSWORD}@{MongoDB_HOST}:{MongoDB_PORT}/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")
    return mongodb_client

def redis_connection():
    global Redis_HOST, Redis_PORT
    
    redis_client = redis.Redis(host=Redis_HOST, port=Redis_PORT, db=0)
    return redis_client

def download_global_pem():
    url = "https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem"
    req = requests.get(url)
    with open(CERT_FILE, 'wb') as f:
        f.write(req.content)

@app.route('/user', methods=["POST"])
def add_user():
  try:
    data = request.json
    name = data.get("name")
    age = data.get("age")
    country = data.get("country")
      
    body = {"name": name, "age": age, "country": country}

    mongodb_client = mongodb_connection()
    db = mongodb_client["demo"]
    col = db["user"]

    mongodb_result = col.insert_one(body)
    mongodb_client.close()

    return {"msg": "User added successfully"}, 200
  except Exception as e:
    logging.error(e)
    abort(500)

@app.route('/user', methods=["GET"])
def get_user():
    try:
        name = request.args.get('name')

        redis_client = redis_connection()
        mongodb_client = mongodb_connection()
        db = mongodb_client["demo"]
        col = db["user"]

        body = {"name": name}
        mongodb_result = col.find_one(body)

        redis_result = redis_client.get(name)
        if redis_result:
            return jsonify(json.loads(redis_result))

        if mongodb_result:
            mongodb_result['_id'] = str(mongodb_result['_id'])
            redis_client.set(name, json.dumps(mongodb_result))
            return jsonify(mongodb_result)

    except Exception as e:
        logging.error(e)
        abort(500)

@app.route('/healthcheck', methods=['GET'])
def get_healthcheck():
  try:
    ret = {'status': 'ok'}

    return jsonify(ret), 200
  except Exception as e:
    logging.error(e)
    abort(500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)