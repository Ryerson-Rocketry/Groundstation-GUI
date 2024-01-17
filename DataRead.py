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

        #persistence tracking
        self.latestElement = 0
        self.currentGraphTab = 3
        self.changedState = False

        self.graphDict = {
            2:"Time",
            3:"Pressure",
            4:"Temperature",
            5:"Signal Strength",
            6:"Battery Voltage"
        }


        #appends the 1D arrays for the individual components for the coordinates to the 2D array that encompasses both
        self.InternalData.append(self.x)
        self.InternalData.append(self.y)
        self.InternalData.append(self.time)
        self.InternalData.append(self.pressure)
        self.InternalData.append(self.signalStrength)
        self.InternalData.append(self.temperature)
        self.InternalData.append(self.batteryVoltage)




def FileReadSequential(Dataset):
    with open('data.txt', "r") as f:


        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list

        lastLine = Dataset.latestElement

        CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")
        SplitArray = CoordArrayList[lastLine].split() #splits each line into the individual x and y components and records it
        Dataset.x.insert(lastLine,SplitArray[0]) 
        Dataset.y.insert(lastLine,SplitArray[1])
        Dataset.time.insert(lastLine,SplitArray[2]) 

        Dataset.pressure.insert(lastLine,SplitArray[3])
        Dataset.signalStrength.insert(lastLine,SplitArray[4])
        Dataset.batteryVoltage.insert(lastLine,SplitArray[5])
        Dataset.temperature.insert(lastLine,SplitArray[6])

        if ((len(CoordArrayList) - 1) > (Dataset.latestElement)):
            Dataset.latestElement += 1


        f.close()

    return Dataset



def fileRead():
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




