from flask import Flask, jsonify, request, current_app
from flask_cors import CORS


import populate
import DataRead
import os

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
        current_app.data_read.gui_state = False
        return jsonify(current_app.data_read.gui_state)
    
@app.route('/radio/start', methods=['GET'])
def radiostart():
    with app.app_context(): 
        current_app.data_read.gui_state = True
        return jsonify(current_app.data_read.gui_state)
    
@app.route('/radio/status', methods=['GET'])
def radiostatus():
    with app.app_context(): 
        return jsonify(current_app.data_read.gui_state)

@app.route('/read/last/<int:index>', methods=['GET'])
def readlast(index):
    with app.app_context(): #we can access session data through app.app_context()
        if (index == 0): #return all store data in a list (http://127.0.0.1:5000/read/last/0)
            change = current_app.data_read.has_changed()
            data = current_app.data_read.get_latest_points()
            return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)
        else:
            #todo
            return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)
    
@app.route('/read/gps', methods=['GET'])
def readgps(): 
    #TO DO
    return "null"

@app.route('/read/graph/<int:index>', methods=['GET'])
def readgraphdata(index): #return full data set of graph data
    with app.app_context(): #we can access session data through app.app_context()
        data = current_app.data_read.get_points(index)
        return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)


@app.route('/initialize/graph/<int:index>', methods=['GET'])
def initialgraphdata():
    data = [{'graph_title': "placeholder", 'graph_x_unit': "placeholder", 'graph_y_unit': "placeholder" }]
    return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)


@app.route('/start', methods=['GET'])
def start():
    create_app()
   
    dir_path = os.path.dirname(os.path.realpath(__file__))
    msg = "current working directory is" + dir_path 
    return msg

def create_app(): #persistant object handling
    with app.app_context(): #define new objects here stored in current server session
        current_app.data_read = DataRead.DataRead() 
        current_app.radio_read = populate.Populate(current_app.data_read) 
        current_app.radio_read.runpopulatefile() #run the radio data retrieval / test file
        
        
        current_app.config['start_time'] = (datetime.datetime.now())
        



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    
    
    