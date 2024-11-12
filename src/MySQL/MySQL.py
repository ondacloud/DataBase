from flask import Flask, jsonify, request, abort
import pymysql
import logging
import os

app = Flask(__name__)

MYSQL_USER = "<UserName>"
MYSQL_PASSWORD = "<Password>"
MYSQL_HOST = "<HOST>"
MYSQL_PORT = "Port" # Default Port Number : 3306
MYSQL_DBNAME = "<DBName>"

def get_db_connection():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        database=MYSQL_DBNAME,
        charset='utf8'
    )
    return conn

def setting_db(message, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(message, params)
    else:
        cursor.execute(message)
    
    if fetch:
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    else:
        conn.commit()
        cursor.close()
        conn.close()

@app.route('/v1/user', methods=['POST'])
def add_user():
    try:
        data = request.json
        name = data.get("name")
        age = data.get("age")
        country = data.get("country")

        message = f"INSERT INTO {MYSQL_DBNAME}.users (name, age, country) VALUES (s, %s, %s)"
        setting_db(message, params=(name, age, country))
        
        return jsonify({"msg": "User added successfully"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        abort(500)

@app.route('/v1/user', methods=['GET'])
def users():
    try:
        name = request.args.get('name')
        if name:
            message = f"SELECT * FROM {MYSQL_DBNAME}.users WHERE name = %s"
            users_data = setting_db(message, params=(name,), fetch=True)

            if users_data:
                body = [{"name": user[0], "age": user[1], "country": user[2]} for user in users_data]
                return jsonify(body), 200
            else:
                return jsonify({"msg": "Name Not Found"}), 404
        else:
            return jsonify({"msg": "Name parameter is required"}), 400

    except Exception as e:
        logging.error(f"Error occurred: {e}")
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
