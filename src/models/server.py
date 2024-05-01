class Server:
    def __init__(self, nameServer, startTime, ri, exitTime, available, exitTimeTotal):
        self.nameServer = nameServer
        self.startTime = startTime
        self.available = available
        self.ri = ri
        self.exitTime = exitTime
        self.exitTimeTotal = exitTimeTotal