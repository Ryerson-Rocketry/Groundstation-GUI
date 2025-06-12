import asyncio
import datetime
import time


class DataRead():
    
    uid = 0

    raw_data_lists = []

    data_lists = []

    writing = False;
    
    """
    graphDict = {
        0:"Time",
        1:"Pressure",
        2:"Temperature",
        3:"Battery Voltage",
        7:"x coord",
        8:"y coord",
        4:"Acceleration X",
        5:"Accelerometer Y",
        6:"Accelerometer Z",

    }
    """
    graphDict = {
        "Time": 0,
        "Pressure": 1,
        "Temperature":2,
        "Battery Voltage":3,
        "Acceleration X":4,
        "Accelerometer Y":5,
        "Accelerometer Z":6,
        "x coord":7,
        "y coord":8,
    }

    has_changed_since_last_request = False
    gui_state = False

    def __init__(self):
        super().__init__()
        for i in range (9):
            self.data_lists.append([])
        pass
     

    def add_data_points(self, data_point: str):
        """
        used by radio populate class to add more rows of data points
        """
        self.has_changed_since_last_request = True
        self.raw_data_lists.append(data_point)

        self.data_parse(data_point)

    def get_latest_points(self):
        while (self.writing == True):
            time.sleep(1)
        """
        return entire latest row of data points
        """
        self.has_changed_since_last_request = False
        return self.raw_data_lists[len(self.raw_data_lists)-1]
    
    #only method that should be sent through the api
    def get_points(self, index):
        while (self.writing == True):
            time.sleep(1)

        """
        return the latest data point of [x: n, y: m], where n = time of the current row, m = selected data from row
        """
        self.has_changed_since_last_request = False

        self.writing = True
        specific_list = []
        for i in range (len(self.data_lists[0])-1):
            specific_list.append({'x': self.data_lists[0][i], 'y': self.data_lists[index][i], 'id' : self.uid})
            self.uid = self.uid + 1
        self.uid = 0
        self.writing = False

        return specific_list
    
    def get_coordinates(self, all: bool):
        while (self.writing == True):
            time.sleep(1)
    
        if (all == False):
            
            specific_list = []
            specific_list.append({'x': self.data_lists[7][len(self.data_lists[0])-1], 'y': self.data_lists[8][len(self.data_lists[0])-1]})
            return specific_list
        
        else:
    
            specific_list = []
            for i in range (len(self.data_lists[0])-1):
                specific_list.append({'x': self.data_lists[7][i], 'y': self.data_lists[8][i]})
            
            return specific_list
    
    def get_latest_points(self):
        """
        return the latest data point of [x: n, y: m], where n = time of the current row, m = selected data from row
        """
        self.has_changed_since_last_request = False

        while (self.writing == True):
            time.sleep(1)
        
        
        specific_list = []
        specific_list.append(self.data_lists[1][len(self.data_lists[0])-1])
        specific_list.append(self.data_lists[2][len(self.data_lists[0])-1])
        specific_list.append(self.data_lists[3][len(self.data_lists[0])-1])
        specific_list.append(self.data_lists[4][len(self.data_lists[0])-1])
        specific_list.append(self.data_lists[5][len(self.data_lists[0])-1])
        specific_list.append(self.data_lists[6][len(self.data_lists[0])-1])
        specific_list.append(self.data_lists[7][len(self.data_lists[0])-1])
        specific_list.append(self.data_lists[8][len(self.data_lists[0])-1])




        return specific_list

    def has_changed(self):
        return self.has_changed_since_last_request
    
    def data_parse(self, string):
        self.writing = True

        raw_data = string.strip("\n")
        raw_data = raw_data.split(",")
       # print(len(self.data_lists), flush=True)
        #for i in range (9):
        #    self.data_lists[i].append(float(raw_data[i])) 

        #retarded way of doing things
        try:
            for i in range(9):
                float(raw_data[i]) #dont save data if it cannot be parsed into a number
        except:
            return


        try:
            self.data_lists[0].append(round(float(raw_data[0]),2))
            self.data_lists[1].append(round(float(raw_data[6]),2))
            self.data_lists[2].append(round(float(raw_data[5]),2))
            self.data_lists[3].append(round(float(raw_data[1]),2))
            self.data_lists[4].append(round(float(raw_data[2]),2))
            self.data_lists[5].append(round(float(raw_data[3]),2))
            self.data_lists[6].append(round(float(raw_data[4]),2))
            self.data_lists[7].append(float(raw_data[7])) #dont round coordinates
            self.data_lists[8].append(float(raw_data[8]))
        except:
            print("error")

        self.writing = False
        
            
