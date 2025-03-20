from flask import Flask, jsonify, request, current_app
from flask_cors import CORS

import populate
import DataRead

import datetime

app = Flask(__name__)
cors = CORS(app)

@app.route('/test')
def hello():
    return "Hello World!"

@app.route('/serverstatus', methods=['GET'])
def status():
    with app.app_context(): 
        deltatime = ((datetime.datetime.now()) - current_app.config['start_time'] ).seconds
        
        status = [{'running': True, 'runTime': deltatime}]
        return jsonify(status)
    
@app.route('/radio/restart', methods=['GET'])
def radiorestart():
    with app.app_context(): 
        #TO DO
        return "null"
    
@app.route('/radio/stop', methods=['GET'])
def radiostop():
    with app.app_context(): 
        #TO DO
        return "null"
    
@app.route('/radio/start', methods=['GET'])
def radiostart():
    with app.app_context(): 
        #TO DO
        return "null"

@app.route('/read/last/<int:index>', methods=['GET'])
def readlast(index):
    with app.app_context(): #we can access session data through app.app_context()
        if (index == 0): #return all store data in a list (http://127.0.0.1:5000/read/last/0)
            change = current_app.data_read.has_changed()
            data = [{'latest_data_points': current_app.data_read.get_latest_point(), 'has_changed_since_last_request': change }]
            return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)
        else:
            change = current_app.data_read.has_changed()
            data = [{'latest_data_points': current_app.data_read.get_point(index), 'has_changed_since_last_request': change }]
            return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)
    
@app.route('/read/gps', methods=['GET'])
def readgps():
    #TO DO
    return "null"

@app.route('/read/graph', methods=['GET'])
def readgraphdata():
    #TO DO
    return "null"

def create_app(): #persistant object handling
    with app.app_context(): #define new objects here stored in current server session
        current_app.data_read = DataRead.DataRead() 
        current_app.radio_read = populate.Populate(current_app.data_read) 
        current_app.radio_read.runpopulatefile() #run the radio data retrieval / test file
        
        current_app.config['start_time'] = (datetime.datetime.now())



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    