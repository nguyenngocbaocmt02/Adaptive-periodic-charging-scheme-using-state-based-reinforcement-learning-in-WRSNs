from abc import ABC

from optimizer.offlineoptimizer.GraphRL.StatusGraph import StatusGraph
from optimizer.offlineoptimizer.OfflineOptimizer import OfflineOptimizer


class GraphRlOptimizer(OfflineOptimizer, ABC):
    def __init__(self, env, T, testedT):
        OfflineOptimizer.__init__(self, env=env)
        self.checkPoint = 0
        self.T = T
        self.testedT = testedT
        self.fuzzy = None
        self.Esafe = 8000
        self.linearDF = (self.Esafe - 800) / int(self.testedT / self.T)

    def schedule(self, mcs, net):
        mc = mcs[0]
        T = min(self.T, self.testedT - self.env.now)
        Esafe = []
        for node in net.listNodes:
            if node.status == 0:
                Esafe.append(0)
            else:
                Esafe.append(self.Esafe)
        self.Esafe -= self.linearDF
        self.checkPoint += self.T
        graph = StatusGraph(net=net, mc=mc, delta=100, T=T, Esafe=Esafe)
        graph.initialize()
        # schedule MC
        for ver in graph.path:
            mc.schedule.append([ver.node.location, ver.chargingTime, [ver.node]])
        mc.schedule.append([net.baseStation.location, 0, []])
        del graph
        print('Time: ' + str(self.env.now) + ' The number of dead node:' + str(net.countDeadNodes()))
