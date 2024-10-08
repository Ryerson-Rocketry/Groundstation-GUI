import asyncio
import datetime

class DataTrack:
    def __init__(self):

        self.InternalData = []

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
        self.InternalData.append(self.x), self.InternalData.append(self.y), self.InternalData.append(self.time), 
        self.InternalData.append(self.pressure), self.InternalData.append(self.temperature), self.InternalData.append(self.batteryVoltage)
        self.InternalData.append(self.accelerometerX), self.InternalData.append(self.accelerometerY), self.InternalData.append(self.accelerometerZ)




    def tolerance(self, graphIndex): 
        #print(self.latestElement)
        if (self.latestElement == 0 or self.latestElement == 1):
            return False #can't check previous data if there is none
        
        #previousTime = self.InternalData[2][self.latestElement-1], currentTime = self.InternalData[2][self.latestElement]
        currentLat = self.InternalData[0][self.latestElement]
        currentLong = self.InternalData[1][self.latestElement]
        previousLat = self.InternalData[0][self.latestElement - 1]
        previousLong = self.InternalData[1][self.latestElement - 1]
        previousTime  = self.InternalData[2][self.latestElement - 1] 
        currentTime = self.InternalData[2][self.latestElement]


        deltaDistanceLat = previousLat - currentLat
        deltaDistanceLong = previousLong - currentLong
        deltaTime = previousTime - currentTime

        #Outlier Detection GPS
        #if ((deltaDistanceLong / deltaTime) > 0.5):
        #    return False

        return False #placeholder
            
        
    def timeSync (self):
        self.currentTime = datetime.datetime.now()


def FileReadSequential(Dataset):

    with open('dateUpdate.txt', "r") as f:

        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list
        lastLine = len(CoordArrayList) - 1

        CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")

        SplitArray = CoordArrayList[lastLine].split(",") #splits each line into the individual x and y components and records it
        #print("Accel" + SplitArray[2] + SplitArray[3] + SplitArray[4])
        
        for x in range(len(SplitArray)):
            if SplitArray[x] == "":
                print("error null")
                return False
            
        if  len(Dataset.InternalData[0]) > 2:
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

        
        for x in range(len(Dataset.InternalData)):
            if (len(Dataset.InternalData[x]) != truelength):
                Dataset.InternalData[x].pop()
        
        print (str(len(Dataset.time)) + ", " + str(len(Dataset.pressure)) + ", " + str(len(Dataset.batteryVoltage)) + ", " + str(len(Dataset.temperature)) + ", " + str(len(Dataset.accelerometerX)) + ", ")

        #if ((len(CoordArrayList) - 1) > (Dataset.latestElement)):
        Dataset.latestElement = len(Dataset.time) - 1

        f.close()

    return Dataset