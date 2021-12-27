import random

from optimizer.offlineoptimizer.OfflineOptimizer import OfflineOptimizer


class RandomOfflineOptimizer(OfflineOptimizer):
    def __init__(self, env, chargingTime=500):
        OfflineOptimizer.__init__(self, env=env)
        self.chargingTime = chargingTime
        self.checkPoint = 0

    def schedule(self, mcs, net):
        self.checkPoint += 20000
        for mc in mcs:
            mc.schedule.clear()
            for i in range(0, 10):
                action = []
                index = random.randint(0, len(net.listNodes) - 1)
                destination = net.listNodes[index].location
                chargingTime = self.chargingTime
                nodes = [net.listNodes[index]]
                action.append(destination)
                action.append(chargingTime)
                action.append(nodes)
                mc.schedule.append(action)
            action = [net.baseStation.location, 0, []]
            mc.schedule.append(action)
