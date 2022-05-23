from datetime import datetime as dt

class Preprocessing:


    def __init__(self, data, whatis=None):

        self.raw_data = data
        #self.__transform_data__()
        print(self.raw_data)
    

    def __transform_data__(self):
        self.data = None

        self.data = dt.utcfromtimestamp(float(self.raw_data)).strftime("%H:%M:%S %m/%d/%Y")






    #def get_data(self):
    #    if self.data != None:
    #        return self.data

    
