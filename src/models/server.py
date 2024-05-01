class Server:
    def __init__(self, nameServer, startTime, ri, exitTime, available:True):
        self.nameServer = nameServer
        self.startTime = startTime
        self.available = available
        self.ri = ri
        self.exitTime = exitTime
        
    def statusActal(self):
        print('SIUUUUU')