import asyncio
import datetime


class DataTrack:
    def __init__(self):

        self.data = {
            'x': [],  
            'y': [],
            'time': [],
            'pressure': [],
            'temperature': [],
            'batteryVoltage': [],
            'accelerometerX': [],
            'accelerometerY': [],
            'accelerometerZ': [], 
        }
        

        #FIX
        self.ignoreDataElements = []

        #persistence tracking
        self.latestElement = -1
        self.currentTime = 0
        self.maprunning  = False #prevents the map from freezing upon a mapping library error

        self.graphDict = {
            2:"Time",
            3:"Pressure",
            4:"Temperature",
            5:"Battery Voltage",
            6:"Acceleration",
            7:"Accelerometer Y",
            8:"Accelerometer Z",
        }

        self.graph_dict_units = {
            2:"Sec",
            3:"Psi",
            4:"C",
            5:"mV",
            6:"M/s^2",
            7:"M/s^2",
            8:"M/s^2",
        }

    def tolerance(self, graphIndex): 
        #print(self.latestElement)
        if (self.latestElement > 0 ):
            return False #can't check previous data if there is none
        
        #previousTime = self.internaldata[2][self.latestElement-1], currentTime = self.internaldata[2][self.latestElement]
        currentLat = self.data['x'][self.latestElement]
        currentLong = self.data['y'][self.latestElement]
        previousLat = self.data['x'][self.latestElement - 1]
        previousLong = self.data['y'][self.latestElement - 1]
        previousTime  = self.data['time'][self.latestElement - 1] 
        currentTime = self.data['time'][self.latestElement]


        deltaDistanceLat = previousLat - currentLat
        deltaDistanceLong = previousLong - currentLong
        deltaTime = previousTime - currentTime


        if (((deltaDistanceLong / deltaTime) > 1) or ((deltaDistanceLat / deltaTime) > 1)):
            return False

        return True
            
        
    def timeSync (self):
        self.currentTime = datetime.datetime.now()


def FileReadSequential(Dataset):
    with open('dateUpdate.txt', "r") as f:
        CoordArrayList = f.readlines()
        lastLine = len(CoordArrayList) - 1

        if lastLine == -1:
            print("Error: File is empty.")
            return False
        
        CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")
        SplitArray = CoordArrayList[lastLine].split(",")
        
        
        
        for x in range(len(SplitArray)):
            if SplitArray[x] == "":
                print("Error: Null value in SplitArray.")
                return False

        if len(Dataset.data['x']) > 2:
            if int(SplitArray[0]) == int(Dataset.data['time'][-2]):
                print("Error: Duplicate time detected.")
                return False

        try:
            Dataset.data['x'].insert(lastLine, float(SplitArray[7]))
            Dataset.data['y'].insert(lastLine, float(SplitArray[8]))
            Dataset.data['pressure'].insert(lastLine, round(float(SplitArray[6])))
            Dataset.data['batteryVoltage'].insert(lastLine, float(SplitArray[1]))
            Dataset.data['temperature'].insert(lastLine, float(SplitArray[5]))
            Dataset.data['accelerometerX'].insert(lastLine, float(SplitArray[2]))
            Dataset.data['accelerometerY'].insert(lastLine, float(SplitArray[3]))
            Dataset.data['accelerometerZ'].insert(lastLine, float(SplitArray[4]))
            Dataset.data['time'].insert(lastLine, float(SplitArray[0]))
        except Exception as e:
            print(f"Error: {e}. Problem input line: {lastLine}")
            return False

        truelength = len(Dataset.data['time'])

        for key in Dataset.data:
            if len(Dataset.data[key]) != truelength:
                print(f"Error: Length mismatch in key '{key}'. Popping extra item.")
                Dataset.data[key].pop()
        
        Dataset.latestElement = len(Dataset.data['time']) - 1
        f.close()

    return Dataset
