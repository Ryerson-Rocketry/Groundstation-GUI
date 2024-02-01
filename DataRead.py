class DataTrack:
    def __init__(self):
        self.InternalData = []

        #Coordinates
        self.x = []
        self.y = []

        self.time = []
        
        #Data
        self.pressure = []
        self.temperature = []
        self.signalStrength = []
        self.batteryVoltage = []

        #Checks for 
        self.ignoreDataElements = []

        #persistence tracking
        self.latestElement = 0
        self.currentGraphTab = 3

        self.maprunning  = False#test

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

        #Using previous data points and 
    def toleranceAndCorruption(self, graphIndex): 
        #print(self.latestElement)
        if (self.latestElement == 0 or self.latestElement == 1):
            return False #can't check previous data if there is none
        
        #previousTime = self.InternalData[2][self.latestElement-1], currentTime = self.InternalData[2][self.latestElement]
        currentLat = self.InternalData[0][self.latestElement - 1]
        currentLong = self.InternalData[1][self.latestElement - 1]
        previousLat = self.InternalData[0][self.latestElement - 2]
        previousLong = self.InternalData[1][self.latestElement - 2]
        latLongTolerance = 5

        #Outlier Detection GPS (placeholder)
        if (((currentLat - previousLat) > latLongTolerance) or ((currentLong - previousLong) > latLongTolerance)):
            self.ignoreDataElements.append(self.latestElement)
            return True
        
        #Outlier Detection Data (placeholder)
        if ((self.InternalData[graphIndex][self.latestElement - 2] - self.InternalData[graphIndex][self.latestElement - 1]) > 5):
            return True
        else:
            return False



def FileReadSequential(Dataset):
    with open('datainvalids.txt', "r") as f:


        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list

        lastLine = Dataset.latestElement

        CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")
        SplitArray = CoordArrayList[lastLine].split() #splits each line into the individual x and y components and records it
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


def fileRead(): #obsolete
    with open('data.txt', "r") as f:

        Dataset = []
        x = []
        y = []

        graphx = []
        graphy = []

        graph2y = []

        


        #appends the 1D arrays for the individual components for the coordinates to the 2D array that encompasses both
        Dataset.append(x)
        Dataset.append(y)
        Dataset.append(graphx)
        Dataset.append(graphy)

        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list
    
        
        for i in range(len(CoordArrayList)):
            CoordArrayList[i] = CoordArrayList[i].strip("\n")
            SplitArray = CoordArrayList[i].split() #splits each line into the individual x and y components and records it
            x.insert(i,SplitArray[0]) 
            y.insert(i,SplitArray[1])
            graphx.insert(i,SplitArray[2]) 
            graphy.insert(i,SplitArray[3])
        

        f.close()

    return Dataset




