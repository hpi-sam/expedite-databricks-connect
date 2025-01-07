from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS  # Import CORS
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Restricting CORS

@app.route("/")
def serve_react_app():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/api/migrate', methods=['POST'])
def migrate_code():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    code = data.get('code', '')
    print(f"Received code: {code}")  # Log the received code
    return jsonify({'result': 'testasfadfassd'})

if __name__ == "__main__":
    app.run(debug=True)
