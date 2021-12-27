import random

from optimizer.ondemandoptimizer.OnDemandOptimizer import OnDemandOptimizer


class RandomOnDemandOptimizer(OnDemandOptimizer):
    def __init__(self, chargingTime):
        OnDemandOptimizer.__init__(self)
        self.chargingTime = chargingTime

    def schedule(self, net, mc):
        action = []
        if mc.energy < 8000:
            action.append(net.baseStation.location)
            action.append(0)
            action.append([])
        index = random.randint(0, len(net.listNodes) - 1)
        if random.random() < 0.8:
            index = 0
        destination = net.listNodes[index].location
        chargingTime = self.chargingTime
        nodes = [net.listNodes[index]]
        action.append(destination)
        action.append(chargingTime)
        action.append(nodes)
        return action
