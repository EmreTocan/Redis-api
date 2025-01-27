from flask import Flask, request, jsonify
import redis
import os 

app = Flask(__name__)


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis.redis.svc.cluster.local"),
    port=int(os.getenv("REDIS_PORT", 6379)), 
    password=os.getenv("REDIS_PASSWORD"),  
    db=0
)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Redis API! Use /add to add a key, /delete to delete a key, and /keys to list all keys."}), 200


@app.route('/add', methods=['POST'])
def add_key():
    data = request.json
    key = data.get('key')
    value = data.get('value')

    if not key or not value:
        return jsonify({"error": "Key and value are required"}), 400

    try:
        redis_client.set(key, value)
        return jsonify({"message": f"Key '{key}' added successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to connect to Redis: {str(e)}"}), 500


@app.route('/delete', methods=['DELETE'])
def delete_key():
    data = request.json
    key = data.get('key')

    if not key:
        return jsonify({"error": "Key is required"}), 400

    try:
        if not redis_client.exists(key):
            return jsonify({"error": f"Key '{key}' does not exist"}), 404

        redis_client.delete(key)
        return jsonify({"message": f"Key '{key}' deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to connect to Redis: {str(e)}"}), 500
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200
@app.route('/keys', methods=['GET'])
def list_keys():
    try:
        keys = []
        cursor = 0
        while True:
            cursor, partial_keys = redis_client.scan(cursor, count=100) 
            keys.extend(partial_keys)
            if cursor == 0: 
                break
        key_value_pairs = []
        for key in keys:
            value = redis_client.get(key)
            key_value_pairs.append({
                "key": key.decode('utf-8'),
                "value": value.decode('utf-8') if value else None
            })
        return jsonify({"keys": key_value_pairs}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to connect to Redis: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)