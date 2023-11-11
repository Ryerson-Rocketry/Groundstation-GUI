import os
import os.path

def fileRead():
    with open('data.txt', "r") as f:

        Coordinates = []
        x = []
        y = []

        #appends the 1D arrays for the individual components for the coordinates to the 2D array that encompasses both
        Coordinates.append(x)
        Coordinates.append(y)

        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list
    

        for i in range(len(CoordArrayList)):
            CoordArrayList[i] = CoordArrayList[i].strip("\n")
            SplitArray = CoordArrayList[i].split() #splits each line into the individual x and y components and records it
            x.insert(i,SplitArray[0]) 
            y.insert(i,SplitArray[1])

        f.close()

    return Coordinates

