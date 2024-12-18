from flask import Flask, jsonify, request, abort
import psycopg2
import logging
import os

app = Flask(__name__)

POSTGRESQL_USER = "<UserName>"
POSTGRESQL_PASSWORD = "<Password>"
POSTGRESQL_HOST = "<HOST>"
POSTGRESQL_PORT = "<Port>"  # Default Port Number 5432
POSTGRESQL_DBNAME = "<DBName>"

def get_db_connection():
    conn = psycopg2.connect(
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USER,
        password=POSTGRESQL_PASSWORD,
        port=POSTGRESQL_PORT,
        dbname=POSTGRESQL_DBNAME,
    )
    return conn

def setting_db(message, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(message, params)
        else:
            cursor.execute(message)

        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
    except Exception as e:
        logging.error(f"Database error: {e}")
        abort(500)
    finally:
        cursor.close()
        conn.close()

@app.route('/v1/user', methods=['POST'])
def add_user():
    try:
        data = request.json
        name = data.get("name")
        age = data.get("age")
        country = data.get("country")

        if not name or not age or not country:
            return jsonify({"msg": "Missing required fields"}), 400

        message = "INSERT INTO users (name, age, country) VALUES (%s, %s, %s)"
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
            message = "SELECT * FROM users WHERE name = %s"
            users_data = setting_db(message, params=(name,), fetch=True)

            if users_data:
                body = [{"name": user[0], "age": user[1], "country": user[2]} for user in users_data]
                return jsonify(body), 200
            else:
                return jsonify({"msg": "Name not found"}), 404
        else:
            message = "SELECT * FROM users"
            users_data = setting_db(message, fetch=True)

            body = [{"name": user[0], "age": user[1], "country": user[2]} for user in users_data]
            return jsonify(body), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        abort(500)

@app.route('/healthcheck', methods=['GET'])
def get_healthcheck():
    try:
        ret = {'status': 'ok'}
        return jsonify(ret), 200
    except Exception as e:
        logging.error(f"Healthcheck failed: {e}")
        abort(500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
