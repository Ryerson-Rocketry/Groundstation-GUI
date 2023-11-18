class Data:
    def __init__(self):
        self.InternalData = []
        self.x = []
        self.y = []

        self.graphx = []
        self.graphy = []

        self.LatestElement = 0

        #appends the 1D arrays for the individual components for the coordinates to the 2D array that encompasses both
        self.InternalData.append(self.x)
        self.InternalData.append(self.y)
        self.InternalData.append(self.graphx)
        self.InternalData.append(self.graphy)

        


def FileReadSequential(Dataset):
    with open('data.txt', "r") as f:


        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list

        lastLine = Dataset.LatestElement

        CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")
        SplitArray = CoordArrayList[lastLine].split() #splits each line into the individual x and y components and records it
        Dataset.x.insert(lastLine,SplitArray[0]) 
        Dataset.y.insert(lastLine,SplitArray[1])
        Dataset.graphx.insert(lastLine,SplitArray[2]) 
        Dataset.graphy.insert(lastLine,SplitArray[3])

        

        if ((len(CoordArrayList) - 1) > (Dataset.LatestElement)):
            Dataset.LatestElement += 1


        
        

        f.close()

    return Dataset



def fileRead():
    with open('data.txt', "r") as f:

        Dataset = []
        x = []
        y = []

        graphx = []
        graphy = []

        


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




