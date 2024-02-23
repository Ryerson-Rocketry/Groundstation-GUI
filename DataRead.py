import asyncio
import datetime

class DataTrack:
    def __init__(self):

        self.InternalData = []

        #Data
        self.x = [0]
        self.y = [0]
        self.time = [0]

        self.pressure = [0]
        self.temperature = [0]
        self.signalStrength = [0]
        self.batteryVoltage = [0]

        #FIX
        self.ignoreDataElements = []

        #persistence tracking
        self.latestElement = 0
        self.currentGraphTab = 3
        self.currentTime = 0
        self.maprunning  = False #prevents the map from freezing upon a mapping library error

        self.graphDict = {
            2:"Time",
            3:"Pressure",
            4:"Temperature",
            5:"Signal Strength",
            6:"Battery Voltage"
        }

        #appends the 1D arrays for the individual components for the coordinates to the 2D array that encompasses both
        self.InternalData.append(self.x), self.InternalData.append(self.y), self.InternalData.append(self.time), 
        self.InternalData.append(self.pressure), self.InternalData.append(self.signalStrength), self.InternalData.append(self.temperature), self.InternalData.append(self.batteryVoltage)


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
        
        for i in SplitArray: #null and valid character detection

            if (i == ""):
                return False
            
            tempCheck = list(i)
            for j in tempCheck:
                if (((ord(j) < 48) or (ord(j) > 57))):
                    if (ord(j) == 45) or (ord(j) == 32) or (ord(j) == 46):
                        pass
                    else:
                        #print (str(ord(j)) + " failed")
                        return False
                
        Dataset.x.insert(lastLine,float(SplitArray[0])) 
        Dataset.y.insert(lastLine,float(SplitArray[1]))
        Dataset.time.insert(lastLine,float(SplitArray[2])) 


        Dataset.pressure.insert(lastLine,float(SplitArray[3]))
        Dataset.signalStrength.insert(lastLine,float(SplitArray[4]))
        Dataset.batteryVoltage.insert(lastLine,float(SplitArray[5]))
        Dataset.temperature.insert(lastLine,float(SplitArray[6]))

        if ((len(CoordArrayList) - 1) > (Dataset.latestElement)):
            Dataset.latestElement += 1

        f.close()

    return Dataset




