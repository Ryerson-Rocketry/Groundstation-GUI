from flask import Flask, jsonify, request, current_app
from flask_cors import CORS

import populate
import DataRead

app = Flask(__name__)
CORS(app)

@app.route('/test')
def hello():
    return "Hello World!"

@app.route('/readLast')
def read():
    return "Hello World!"

def create_app(): #persistant object handling
    app = Flask(__name__)
    with app.app_context():
        current_app.data_read = DataRead.DataRead()
        current_app.radio_read = populate.Populate() 
        current_app.config['test'] = 'test' 

    with app.app_context():
        #here to use current_app to get what you want.
        print("placeholder")


if __name__ == '__main__':
    create_app()
    app.run(host='127.0.0.1', port=5000)
    