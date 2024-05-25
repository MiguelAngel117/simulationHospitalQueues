from helpers.generateNames import generateNames

class Patient:
    def __init__(self, arrival_time, interarrival_time):
        self.name = generateNames()
        self.interarrival_time = interarrival_time
        self.arrival_time = arrival_time
        self.start_time = None
        self.end_time = None
        self.waiting_time = 0
        self.total_time = 0
