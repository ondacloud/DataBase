from flask import Flask, abort, request, jsonify
import logging
import json
import redis

app = Flask(__name__)

# DB Setting
DB_HOST = "<HOST>"
DB_PORT = "<PORT>" # Default Port Number : 6379

def db_connection():
    global DB_HOST, DB_PORT
    
    client = redis.Redis(host=DB_HOST, port=DB_PORT, db=0)
    return client

@app.route('/user', methods=["POST"])
def add_user():
    try:
        data = request.json
        name = data.get("name")
        age = data.get("age")

        client = db_connection()

        result = client.set(name, age)
        
        return {"msg": "User added successfully"}
    except Exception as e:
        logging.error(e)
        abort(500)

@app.route('/user', methods=['GET'])
def get_user():
    try:
        name = request.args.get('name')  

        client = db_connection()

        result = client.get(name)
        result = result.decode('utf-8')
        body = {"name": name, "age": result}

        return jsonify(body), 200
    except Exception as e:
        logging.error(e)
        abort(500)

@app.route('/healthz', methods=['GET'])
def get_healthz():
  try:
    ret = {'status': 'ok'}

    return jsonify(ret), 200
  except Exception as e:
    logging.error(e)
    abort(500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)