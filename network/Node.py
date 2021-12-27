import numpy as np
import scipy.spatial.distance as distance

import network.Parameter as Para


class Node:
    # identification of a node
    index = 0

    def __init__(self, location=np.zeros(2), energy=Para.NODE_CAPACITY, energyCR=0, threshold=Para.NODE_THRESHOLD,
                 capacity=Para.NODE_CAPACITY):
        self.env = None
        self.location = location
        self.energy = energy
        self.energyCR = energyCR
        self.id = Node.index
        self.energyRR = 0
        Node.index += 1
        self.threshold = threshold
        self.capacity = capacity
        self.status = 1
        self.checkStatus()

    def operate(self, simulateTime, t=1):
        """
        The operation of a node
        :param simulateTime: the time limit of the operation
        :returns yield t(s) to time management system every t(s)
        """
        sumTime = simulateTime
        while sumTime != 0:
            if sumTime < t:
                t = sumTime
            # if self.id == 0:
            # print(str(self.env.now)+" "+str(self.energy)+" "+str(self.energyRR))
            if self.status == 0:
                sumTime -= t
                yield self.env.timeout(t)
                continue
            self.energy = min(max(self.energy - t * self.energyCR + t * self.energyRR, self.threshold), self.capacity)
            self.checkStatus()
            sumTime -= t
            yield self.env.timeout(t)

        return

    def charged(self, mc):
        if self.status == 1:
            self.energyRR += mc.alpha / (distance.euclidean(self.location, mc.location) + mc.beta) ** 2

    def chargingDisconnect(self, mc):
        if self.status == 1:
            self.energyRR -= mc.alpha / (distance.euclidean(self.location, mc.location) + mc.beta) ** 2

    def checkStatus(self):
        if self.energy <= self.threshold:
            self.status = 0
            self.energyRR = 0
            self.energyCR = 0
