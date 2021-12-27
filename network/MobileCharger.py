import scipy.spatial.distance as distance

import network.Parameter as Para


class MobileCharger:
    index = 0

    def __init__(self, env, location, capacity=Para.MC_CAPACITY, threshold=Para.MC_THRESHOLD,
                 alpha=Para.MC_ALPHA, beta=Para.MC_BETA,
                 velocity=Para.MC_VELOCITY, pm=Para.MC_PM):
        """
        The initialization for a MC. The default value of these params are in the Parameter.py
        :param env: the time management system of this MC
        :param location: the initial coordinate of this MC, usually at the base station
        :param capacity: the capacity of this MC
        :param threshold: the threshold of this MC
        :param alpha: the charging rate regarding the Friss's function
        :param beta: another charging rate regarding the Friss's function
        :param velocity: the velocity of this MC
        :param pm: the moving rate of this MC
        """
        self.env = env
        self.location = location
        self.energy = capacity
        self.capacity = capacity
        self.alpha = alpha
        self.beta = beta
        self.threshold = threshold
        self.velocity = velocity
        self.pm = pm

        self.id = MobileCharger.index
        MobileCharger.index += 1

        self.chargingRate = 0

        self.schedule = []

        self.status = 1
        self.checkStatus()

    def move(self, destination, simulateTime, t=1):
        """
        The movement within simulateTime to a destination :param destination: the final destination of this movement
        :param simulateTime: the time limit of movement. The MC may not reach the destination if the simulateTime is
        run out
        :param t: the status of MC is updated every t(s)
        :return yield t(s) to time management system every t(s) and terminate when MC reaches the destination
        """
        sumTime = simulateTime
        while distance.euclidean(self.location, destination) > Para.epsilon:
            if sumTime < t:
                t = sumTime
            if self.status == 0:
                print("MC run out of energy while moving from !" + str(self.location))
                yield self.env.timeout(sumTime)
                sumTime = 0
                continue
            else:
                energyConsume = distance.euclidean(self.location, destination) / self.velocity * self.pm
                movingVector = [destination[i] - self.location[i] for i in range(0, len(self.location))]
                movingTime = distance.euclidean(self.location, destination) / self.velocity
                if movingTime > t:
                    energyConsume = energyConsume / movingTime * t
                    movingVector = [i / movingTime * t for i in movingVector]
                    movingTime = t
                else:
                    t = movingTime
                if self.energy - energyConsume <= self.threshold:
                    movingVector = [i / ((self.energy - self.threshold) / energyConsume) for i in movingVector]
                    energyConsume = self.energy - self.threshold
                self.location = [self.location[i] + movingVector[i] for i in range(0, len(self.location))]
                self.energy = self.energy - energyConsume
                self.checkStatus()
                sumTime -= t
                yield self.env.timeout(t)

    def chargeNodes(self, chargingTime, simulateTime, nodes, t=1):
        """
        The charging process to nodes in 'nodes' within simulateTime
        :param nodes: the set of charging nodes
        :param t: the status of MC is updated every t(s)
        :param chargingTime: the charging time
        :param simulateTime: the time limit
        """
        sumTime = min(chargingTime, simulateTime)
        while sumTime > Para.epsilon:
            if sumTime < t:
                t = sumTime
            if self.status == 0:
                print("MC run out of energy while charging at !" + str(self.location))
                yield self.env.timeout(sumTime)
                sumTime = 0
                continue
            self.setChargingRate(nodes)
            if self.status == 0:
                sumTime -= t
                yield self.env.timeout(t)
                continue
            self.energy = max(self.threshold, self.energy - self.chargingRate * t)
            self.checkStatus()
            sumTime -= t
            yield self.env.timeout(t)
            self.chargingDisconnect(nodes)

    def setChargingRate(self, nodes):
        """
        Set up the charging rate when charging nodes
        :param nodes: the set of charging nodes
        """
        tmp = 0
        for node in nodes:
            if node.status == 0:
                continue
            d = distance.euclidean(self.location, node.location)
            tmp += self.alpha / (d + self.beta) ** 2
            node.charged(mc=self)
        self.chargingRate = tmp

    def chargingDisconnect(self, nodes):
        """
        Disconnect the charging process
        :param nodes: the set of charging nodes
        """
        for node in nodes:
            if node.status == 0:
                continue
            node.chargingDisconnect(mc=self)
        self.chargingRate = 0

    def operate(self, net, simulateTime, optimizer=None):
        """
        The operation of MC
        :param net: the network
        :param simulateTime: the simulate time
        :param optimizer: if the  schedule list of MC is empty, the on-demand algorithm will provide the next action
        instantly , the offline algorithm will wait until the checkpoint
        :returns return time of charging and moving to time management system
        """
        while True:
            if len(self.schedule) == 0:
                if optimizer is None:
                    break
                elif optimizer.optimizeType == "On-demand":
                    self.schedule.append(optimizer.schedule(net=net, mc=self))
                elif optimizer.optimizeType == "Offline":
                    yield self.env.timeout(optimizer.checkPoint - self.env.now)
            else:
                action = self.schedule[0]
                destination = action[0]
                chargingTime = action[1]
                nodes = action[2]
                yield self.env.process(
                    self.move(destination=destination, simulateTime=simulateTime))
                print('Time: ' + str(self.env.now) + ", MC " + str(self.id) + ' is at ' + str(self.location))
                if self.location != net.baseStation.location and len(nodes) != 0:
                    yield self.env.process(
                        self.chargeNodes(chargingTime=chargingTime, simulateTime=simulateTime,
                                         nodes=nodes))
                else:
                    yield self.env.process(net.baseStation.chargeMC(self, chargingTime))
                del self.schedule[0]

        return

    def checkStatus(self):
        """
        check the status of MC
        """
        if self.energy <= self.threshold:
            self.status = 0
