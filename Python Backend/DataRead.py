
import asyncio
import datetime

class DataTrack:
    def __init__(self):

        self.internaldata = []

        #Data
        self.x = []
        self.y = []
        self.time = []

        self.pressure = []
        self.temperature = []
        self.batteryVoltage = []
        self.accelerometerX = []
        self.accelerometerY = []
        self.accelerometerZ = []

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

        #appends the 1D arrays for the individual components for the coordinates to the 2D array that encompasses both
        self.internaldata.append(self.x), self.internaldata.append(self.y), self.internaldata.append(self.time), 
        self.internaldata.append(self.pressure), self.internaldata.append(self.temperature), self.internaldata.append(self.batteryVoltage)
        self.internaldata.append(self.accelerometerX), self.internaldata.append(self.accelerometerY), self.internaldata.append(self.accelerometerZ)

    def tolerance(self, graphIndex): 
        #print(self.latestElement)
        if (self.latestElement > 0 ):
            return False #can't check previous data if there is none
        
        #previousTime = self.internaldata[2][self.latestElement-1], currentTime = self.internaldata[2][self.latestElement]
        currentLat = self.internaldata[0][self.latestElement]
        currentLong = self.internaldata[1][self.latestElement]
        previousLat = self.internaldata[0][self.latestElement - 1]
        previousLong = self.internaldata[1][self.latestElement - 1]
        previousTime  = self.internaldata[2][self.latestElement - 1] 
        currentTime = self.internaldata[2][self.latestElement]


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

        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list
        lastLine = len(CoordArrayList) - 1

        if lastLine == -1:
            return False
        
        CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")

        SplitArray = CoordArrayList[lastLine].split(",") #splits each line into the individual x and y components and records it
        #print("Accel" + SplitArray[2] + SplitArray[3] + SplitArray[4])
        
        for x in range(len(SplitArray)):
            if SplitArray[x] == "":
                print("error null")
                return False
            
        if  len(Dataset.internaldata[0]) > 2:
            #print(str(SplitArray[0]) + ", " + str(Dataset.time[-2]))
            if int(SplitArray[0]) == int(Dataset.time[-2]):
                #print(str(SplitArray[0]) + ", " + str(Dataset.time[-2]))
                return False;

        try:
            Dataset.x.insert(lastLine,float(SplitArray[7])) 
            Dataset.y.insert(lastLine,float(SplitArray[8]))
 
            Dataset.pressure.insert(lastLine,round(float(SplitArray[6])))
            Dataset.batteryVoltage.insert(lastLine,float(SplitArray[1]))
            Dataset.temperature.insert(lastLine,float(SplitArray[5]))
            Dataset.accelerometerX.insert(lastLine, float(SplitArray[2]))
            Dataset.accelerometerY.insert(lastLine, float(SplitArray[3]))
            Dataset.accelerometerZ.insert(lastLine, float(SplitArray[4]))
            Dataset.time.insert(lastLine,float(SplitArray[0]))
        except:
            print("error" + "Problem inputline:" + str(lastLine))

        #error checking
        truelength = len(Dataset.time)

        
        for x in range(len(Dataset.internaldata)):
            if (len(Dataset.internaldata[x]) != truelength):
                Dataset.internaldata[x].pop()
        
        #print (str(len(Dataset.time)) + ", " + str(len(Dataset.pressure)) + ", " + str(len(Dataset.batteryVoltage)) + ", " + str(len(Dataset.temperature)) + ", " + str(len(Dataset.accelerometerX)) + ", ")

        #if ((len(CoordArrayList) - 1) > (Dataset.latestElement)):
        Dataset.latestElement = len(Dataset.time) - 1

        f.close()

    return Dataset


"""
import asyncio
import datetime

class DataTrack:
    def __init__(self):

        #self.internaldata = []

        #Data
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
        '''
        self.x = []
        self.y = []
        self.time = []

        self.pressure = []
        self.temperature = []
        self.batteryVoltage = []
        self.accelerometerX = []
        self.accelerometerY = []
        self.accelerometerZ = []
        '''
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

        #appends the 1D arrays for the individual components for the coordinates to the 2D array that encompasses both
        '''
        self.internaldata.append(self.x), self.internaldata.append(self.y), self.internaldata.append(self.time), 
        self.internaldata.append(self.pressure), self.internaldata.append(self.temperature), self.internaldata.append(self.batteryVoltage)
        self.internaldata.append(self.accelerometerX), self.internaldata.append(self.accelerometerY), self.internaldata.append(self.accelerometerZ)
'''
    def tolerance(self, graphIndex): 
        #print(self.latestElement)
        if (self.latestElement > 0 ):
            return False #can't check previous data if there is none
        
        #previousTime = self.internaldata[2][self.latestElement-1], currentTime = self.internaldata[2][self.latestElement]
        currentLat = self.data['x'][self.latestElement]
        currentLong = self.data['y'][self.latestElement]
        currentTime = self.data['time'][self.latestElement]
        previousLat = self.data['x'][self.latestElement - 1]
        previousLong = self.data['y'][self.latestElement - 1]
        previousTime = self.data['time'][self.latestElement - 1]
        
        '''
        currentLat = self.internaldata[0][self.latestElement]
        currentLong = self.internaldata[1][self.latestElement]
        previousLat = self.internaldata[0][self.latestElement - 1]
        previousLong = self.internaldata[1][self.latestElement - 1]
        previousTime  = self.internaldata[2][self.latestElement - 1] 
        currentTime = self.internaldata[2][self.latestElement]
''' 

        deltaDistanceLat = previousLat - currentLat
        deltaDistanceLong = previousLong - currentLong
        deltaTime = previousTime - currentTime


        if (((deltaDistanceLong / deltaTime) > 1) or ((deltaDistanceLat / deltaTime) > 1)):
            return False

        return True
            
        
    def timeSync (self):
        self.currentTime = datetime.datetime.now()
"""

def FileReadSequential(Dataset):

    with open('dateUpdate.txt', "r") as f:

        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list
        lastLine = len(CoordArrayList) - 1

        if lastLine == -1:
            return False
        
        CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")

        SplitArray = CoordArrayList[lastLine].split(",") #splits each line into the individual x and y components and records it
        #print("Accel" + SplitArray[2] + SplitArray[3] + SplitArray[4])
        
        for x in range(len(SplitArray)):
            if SplitArray[x] == "":
                print("error null")
                return False
           
        if  len(Dataset.internaldata[0]) > 2:
            #print(str(SplitArray[0]) + ", " + str(Dataset.time[-2]))
            if int(SplitArray[0]) == int(Dataset.time[-2]):
                #print(str(SplitArray[0]) + ", " + str(Dataset.time[-2]))
                print("Error: Duplicate time detected.")
                return False
        
    
        try:

            
            Dataset.x.insert(lastLine,float(SplitArray[7])) 
            Dataset.y.insert(lastLine,float(SplitArray[8]))
 
            Dataset.pressure.insert(lastLine,round(float(SplitArray[6])))
            Dataset.batteryVoltage.insert(lastLine,float(SplitArray[1]))
            Dataset.temperature.insert(lastLine,float(SplitArray[5]))
            Dataset.accelerometerX.insert(lastLine, float(SplitArray[2]))
            Dataset.accelerometerY.insert(lastLine, float(SplitArray[3]))
            Dataset.accelerometerZ.insert(lastLine, float(SplitArray[4]))
            Dataset.time.insert(lastLine,float(SplitArray[0]))
        except:
            print("error" + "Problem inputline:" + str(lastLine))

        #error checking
        truelength = len(Dataset.time)

        for x in range(len(Dataset.internaldata)):
            if (len(Dataset.internaldata[x]) != truelength):
                Dataset.internaldata[x].pop()

        #print (str(len(Dataset.time)) + ", " + str(len(Dataset.pressure)) + ", " + str(len(Dataset.batteryVoltage)) + ", " + str(len(Dataset.temperature)) + ", " + str(len(Dataset.accelerometerX)) + ", ")

        #if ((len(CoordArrayList) - 1) > (Dataset.latestElement)):
        Dataset.latestElement = len(Dataset.time) - 1

        f.close()

    return Dataset