import asyncio
import datetime

class DataRead():

    data_point_list = []
    has_changed_since_last_request = False

    def __init__(self):
        super().__init__()
        pass
     
    def add_data_point(self, data_point: str):
        self.has_changed_since_last_request = True
        self.data_point_list.append(data_point)

    def get_latest_point(self):
        self.has_changed_since_last_request = False
        return self.data_point_list[len(self.data_point_list)-1]
    
    def get_point(self, index):
        self.has_changed_since_last_request = False
        return self.data_point_list[index]

    def has_changed(self):
        return self.has_changed_since_last_request
