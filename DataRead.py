import asyncio
import datetime
import sys
# this is where python stores modules, yours could be different
sys.path.insert(1, r"D:\Programming\Library-RRC-encoder\src")

#import tty,termios

import time as t
import serial
import keyboard 


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
    #-------------------------------

"""  
def FileReadSequential(Dataset):
   

    port = "COM3"

    baud  = 115200 
    ####    initilization    ####
    i =0 
    count = 0
    #uno = serial.Serial(port,115200)
    flag=True
    radio_connect = False
    radio_connect2 = False

    rx_command = False
    while True:

        try:
            radio =serial.Serial(port=port,baudrate=baud)

            radio_connect = True
            break
        except Exception as e:
            print(e)
            radio_connect = False
            exit(-1)

    print("Connected")

    #filedescriptors = termios.tcgetattr(sys.stdin) # retrieves current terminal settings 
    #tty.setcbreak(sys.stdin) # allows for single character commands in terminal ; RAW mode instead of COOKED  mode
    #tty and termios make sure terminal reads the key inputs 

    while (radio_connect == True):
        
        #byteInWait = radio._RadioSerialBuffer.inWaiting()
        
        data_str= radio.readline().strip("null").decode("utf-8")    # write a string
        if (data_str==None):
            print("stufdhfskbj\n")
            continue
        else:
            data_str= data_str.split('\n')
            print("data is %s " % data_str[0])
            #print("# bytes in wait: %d \n" % byteInWait)
            t.sleep(1)
            print('...\n')
            '''
            if (data_str[0] == 'idle'):
                start=t.time()
                while True:
                    end=t.time()
                    timer=end-start
                    if keyboard.is_pressed('space'):
                        rx_command = True
                        print("sending launch command \n") 
                        t.sleep(1)
                        flag=False
                        break
                    elif (timer>2):
                        rx_command= False
                        break
            if flag==False:
                break
            
            else:
                #t.sleep(0.5)
                print("data command is: %s\n"% data_str[0]) 
                radio.sendCommand("launch\n")
                print("launch command sent\n")
                t.sleep(1)
                if keyboard.is_pressed('D'):
                    t.sleep(1)
                    print("exitting connect loop \n")
                    break
            '''

        #CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list

        #SplitArray = data_str.split() #splits each line into the individual x and y components and records it
        
        
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
        
        
        try:
            Dataset.x.insert(0,float((data_str[0]))) 
            Dataset.y.insert(0,float(data_str[1]))
            Dataset.time.insert(0,float(data_str[2])) 


            Dataset.pressure.insert(0,float(data_str[3]))
            Dataset.signalStrength.insert(0,float(data_str[4]))
            Dataset.batteryVoltage.insert(0,float(data_str[5]))
            Dataset.temperature.insert(0,float(data_str[6]))
        except:
            print("is null")
            
            Dataset.latestElement = 0
        

    return Dataset        

"""
    
  


def FileReadSequential(Dataset):
   
    with open('dateUpdate.txt', "r") as f:


        CoordArrayList = f.readlines() #reads each line of the data file and splits it into a array list
        lastLine = len(CoordArrayList) - 1
        #CoordArrayList[lastLine] = CoordArrayList[lastLine].strip("\n")

        SplitArray = CoordArrayList[lastLine].split(", ") #splits each line into the individual x and y components and records it

        SplitFirstLine = CoordArrayList[0].split(", ")

        
        #print (len(Dataset.x))
        if (len(Dataset.x) == 1): # len == 0 is a buffer

            print ("test")
            Dataset.x.insert(1,float(SplitFirstLine[4])) 
            Dataset.y.insert(1,float(SplitFirstLine[5]))
        

        #for i in SplitArray:
        #    print (SplitArray[i])
        
        """
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
        """

        #print (SplitArray)

        Dataset.x.insert(lastLine,float(SplitArray[4])) 
        Dataset.y.insert(lastLine,float(SplitArray[5]))
        Dataset.time.insert(lastLine,(float(SplitArray[0]) - float(SplitFirstLine[0]))) 

        Dataset.pressure.insert(lastLine,float(SplitArray[6]))
        Dataset.signalStrength.insert(lastLine,float(SplitArray[6]))
        Dataset.batteryVoltage.insert(lastLine,float(SplitArray[5]))
        Dataset.temperature.insert(lastLine,float(SplitArray[5]))

        if ((len(CoordArrayList) - 1) > (Dataset.latestElement)):
            Dataset.latestElement += 1

            

        f.close()
        

    return Dataset
