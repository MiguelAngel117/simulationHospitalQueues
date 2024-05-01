class Patient:
    def __init__(self, name, arrivalTime, ri, intervalArrivalTime, leftService = False ,priority=0):
        self.name = name
        self.arrivalTime = arrivalTime
        self.ri = ri
        self.intervalArrivalTime = intervalArrivalTime
        self.leftService = leftService
        self.priority = priority