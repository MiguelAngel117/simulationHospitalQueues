class Patient:
    def __init__(self, name, arrivalTime:0, ri:0, intervalArrivalTime:0, leftService:False, priority:0):
        self.name = name
        self.arrivalTime = arrivalTime
        self.ri = ri
        self.intervalArrivalTime = intervalArrivalTime
        self.leftService = leftService
        self.priority = priority