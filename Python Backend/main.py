from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)