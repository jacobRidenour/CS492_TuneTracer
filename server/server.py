from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="../Application/client/src")

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)