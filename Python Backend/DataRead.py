import asyncio
import datetime

class DataRead():

    data_point_list = []

    def __init__(self):
        super().__init__()
        pass
     
    def add_data_point(self, data_point: str):
        self.data_point_list.append(data_point)

    def get_latest_point(self):
        return self.data_point_list[len(self.data_point_list)-1]
