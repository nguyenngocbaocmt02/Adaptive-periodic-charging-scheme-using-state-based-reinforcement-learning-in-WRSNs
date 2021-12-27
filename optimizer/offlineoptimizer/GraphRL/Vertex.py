class Vertex:
    def __init__(self, lowerArrivalTime, upperArrivalTime, chargingTime, node=None, endVertex=False, reward=0):
        self.node = node
        self.lowerArrivalTime = lowerArrivalTime
        self.upperArrivalTime = upperArrivalTime
        self.adjacent = []
        self.chargingTime = chargingTime
        self.endVertex = endVertex
        self.reward = reward
        self.value = 0
        self.N = 0
