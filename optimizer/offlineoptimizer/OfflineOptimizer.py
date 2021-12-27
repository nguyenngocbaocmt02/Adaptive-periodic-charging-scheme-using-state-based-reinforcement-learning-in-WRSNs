from abc import abstractmethod

from optimizer.Optimizer import Optimizer


class OfflineOptimizer(Optimizer):
    def __init__(self, env, checkPoint=0):
        Optimizer.__init__(self, optimizeType='Offline')
        self.checkPoint = checkPoint
        self.env = env

    @abstractmethod
    def schedule(self, net, mcs):
        pass

    def controller(self, mcs, net):
        while True:
            yield self.env.timeout(self.checkPoint - self.env.now)
            self.schedule(mcs, net)
