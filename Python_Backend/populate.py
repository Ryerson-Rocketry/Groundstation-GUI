import time
import time as t
import serial
#import keyboard 

import DataRead

import threading

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class Populate():

    data_read_obj: DataRead.DataRead = None

    state: bool = False

    port_id: str = "COM5"

    log_path: str = ""

    def __init__(self, data_read):
        super().__init__()
        self.data_read_obj = data_read
 
        if (dir_path.endswith('_internal')): #launching flask from compiled electron exe will have this as the endpoint in the flask exe's directory
            self.log_path = dir_path.removesuffix('_internal')
        else:
            self.log_path = dir_path
        pass

    #for testing with radio
    def radiorun(self):
        port = self.port_id

        baud  = 57600 
        ####    initilization    ####
        i =0 
        count = 0
        #uno = serial.Serial(port,115200)
        flag=True
        radio_connect = True
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

                #MODIFIED SINCE LAST YEAR
                self.state = True

        print("Connected")

        #filedescriptors = termios.tcgetattr(sys.stdin) # retrieves current terminal settings 
        #tty.setcbreak(sys.stdin) # allows for single character commands in terminal ; RAW mode instead of COOKED  mode
        #tty and termios make sure terminal reads the key inputs 

        while (radio_connect == True):
            
            #byteInWait = radio._RadioSerialBuffer.inWaiting()

            data_str= radio.readline().strip().decode("utf-8") #write a string
            
            if (data_str==None):
                print("no data in")
                
            else:
                print (data_str)
                self.populatefileradio(data_str)
                #data_str= data_str.split('\n')
                #print("data is %s " % data_str[0])
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

            
    #for testing WITH the radio
    def populatefileradio(self, data_str):

        with open('dateUpdate.txt', "a") as f:
                
            if (data_str != ""):   
                self.data_read_obj.add_data_points(data_str)
                f.write(data_str + "\n")
                f.flush()

            time.sleep(1)

            self.state = True
        f.close()

        self.radiorun()
    

    #for testing with preset dataset WITHOUT the radio
    def populatefile(self):
        self.state = True


        #with open('dateUpdate.txt', "w") as f, open('data.txt', "r") as f1:
        #with open('D:/Programming/MetRocketry/Groundstation-GUI_Electron/Python Backend/dateUpdate.txt', "w") as f, open('D:/Programming/MetRocketry/Groundstation-GUI_Electron/Python Backend/datainvalids.txt', "r") as f1:
        with open(self.log_path + '/data_log.txt', "w") as f, open(self.log_path + '/simulated_data.txt', "r") as f1: #note this should be temp (if program is built it wouuld read and write to this directory)  
            f.write(self.log_path)
            f.flush()

            arrayList = f1.readlines()

            for i in arrayList:
                self.data_read_obj.add_data_points(i)
                
                #print("writing: " + i)

                f.write(i)
                f.flush()
                
                time.sleep(2)

    def runpopulatefile(self, demo: bool): #this method will run the data retrieval from radio/test file in a separate thread (or else it would be blocking execution from the rest of the backend)
        if (demo == True):
            threading.Thread(target=self.populatefile).start()   
        else:
            threading.Thread(target=self.radiorun).start()  

    
pop = Populate(DataRead.DataRead())

#pop.populatefile()
#pop.populatefileradio()
