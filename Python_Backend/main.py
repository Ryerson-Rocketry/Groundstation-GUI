from flask import Flask, jsonify, request, current_app, has_request_context, has_app_context
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
        #deltatime = ((datetime.datetime.now()) - current_app.config['start_time'] ).seconds

        status = [{'state': True, 'runTime': 0, "radio_state": current_app.radio_read.state, "radio_port_id": current_app.radio_read.port_id, "flask_path": current_app.radio_read.log_path}]
        return jsonify(status)


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
    
@app.route('/read/graph/<int:index>', methods=['GET'])
def readgraphdata(index): #return full data set of graph data
    with app.app_context(): #we can access session data through app.app_context()
        data = current_app.data_read.get_points(index)
        return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)
    
@app.route('/read/graph/all', methods=['GET'])
def readgraphall(): #return full data set of graph data
    with app.app_context(): #we can access session data through app.app_context()
        data = []
        for i in range(7):
            data.append(current_app.data_read.get_points(i))
        return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)

@app.route('/read/gps/all', methods=['GET'])
def readgpsall(): #return full data set of graph data
    with app.app_context(): #we can access session data through app.app_context()
        data = []
        data.append(current_app.data_read.get_coordinates(True))
        return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)
    
@app.route('/read/gps/latest', methods=['GET'])
def readgpslatest(): #return full data set of graph data
    with app.app_context(): #we can access session data through app.app_context()
        return jsonify(current_app.data_read.get_coordinates(False)) #jsonify returns data formatted into json (good for parsing it from the frontend)

@app.route('/initialize/graph/<int:index>', methods=['GET'])
def initialgraphdata():
    data = [{'graph_title': "placeholder", 'graph_x_unit': "placeholder", 'graph_y_unit': "placeholder" }]
    return jsonify(data) #jsonify returns data formatted into json (good for parsing it from the frontend)


@app.route('/radio/demo', methods=['GET'])
def radio_demo():
    current_app.radio_read.runpopulatefile(True) #run the radio data retrieval / test file
    
    return jsonify(True)

@app.route('/radio/start', methods=['GET'])
def radio_start():
    current_app.radio_read.runpopulatefile(False) #run the radio data retrieval / test file
    
    return jsonify(True)

@app.route('/radio/port/<int:index>', methods=['GET'])
def radio_port(index):
    current_app.radio_read.port_id = index
    
    return jsonify(True)

def create_app(): #persistant object handling
    with app.app_context(): #define new objects here stored in current server session
        
        current_app.data_read = DataRead.DataRead() 
        current_app.radio_read = populate.Populate(current_app.data_read) 
        current_app.config['start_time'] = (datetime.datetime.now())

    return app
        



if __name__ == '__main__':
    app = create_app()

    app.run(host='127.0.0.1', port=5000)
    
    
    