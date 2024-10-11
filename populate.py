import time
import time as t
import serial
#import keyboard 


class Populate():
    def __init__(self):
        super().__init__()
        pass

    #for testing with radio
    def radiorun(self):
        port = "COM5"

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

        with open('dateUpdate.txt', "a") as f, open('data.txt', "r") as f1:
                
                if (data_str != ""):   
                    f.write(data_str + "\n")
                    f.flush()

                time.sleep(1)
        f.close()

        self.radiorun()
    

    #for testing with preset dataset WITHOUT the radio
    def populatefile(self):

        #with open('dateUpdate.txt', "w") as f, open('data.txt', "r") as f1:
        with open('dateUpdate.txt', "w") as f, open('datainvalids.txt', "r") as f1:
            

            arrayList = f1.readlines()

            for i in arrayList:
                f.write(i)
                f.flush()

                time.sleep(1)
    
"""
pop = Populate()

pop.populatefile()
#pop.populatefileradio()
"""