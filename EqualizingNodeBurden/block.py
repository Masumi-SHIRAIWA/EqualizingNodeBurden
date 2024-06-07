#Block
class block:
    
    def __init__(self, prevHash, height, time, tx_list):
        self.type = "block"
        self.header = {"prevHash" : prevHash, "height" : height, "TimeStamp" : time}
        # body = hash values of tx in the list.
        self.body = tx_list
        self.popLevel = 1.0