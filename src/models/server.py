class Server:
    def __init__(self, nameServer, ):
        self.nameServer = nameServer
        self.times = []
        self.available = True
    
    def addTime(self, startTime, ri, exitTime, exitTimeTotal):
        timeServer = TimeServer(startTime, ri, exitTime, exitTimeTotal)
        self.times.append(timeServer)
    
    def setAvailable(self):
        self.available = False if self.available else True
        
class TimeServer:
    def __init__(self, startTime, ri, exitTime, exitTimeTotal):
        self.startTime = startTime
        self.ri = ri
        self.exitTime = exitTime
        self.exitTimeTotal = exitTimeTotal