from flask import Flask, abort, request, jsonify
from pymongo import MongoClient
from bson import json_util
import requests
import logging
import json
import os

app = Flask(__name__)

# DB Setting
MONGODB_USERNAME = "<UserName>"
MONGODB_PASSWORD = "<Password>"
MONGODB_HOST = "<HOST>"
MONGODB_PORT = "<Port>" # Default Port Number : 27017
CERT_FILE = "global-bundle.pem"

def db_connection():
    download_global_pem()

    client = MongoClient(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")
    return client

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

    client = db_connection()
    db = client["demo"]
    col = db["user"]

    result = col.insert_one(body)
    client.close()

    return {"msg": "User added successfully"}, 200
  except Exception as e:
    logging.error(e)
    abort(500)

@app.route('/user', methods=["GET"])
def get_user():
  try:
    name = request.args.get('name')  

    body = {"name": name}

    client = db_connection()
    db = client["demo"]
    
    col = db["user"]

    result = col.find(body)
    result = [json.loads(json_util.dumps(doc)) for doc in result]

    return jsonify(list(result)), 200
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