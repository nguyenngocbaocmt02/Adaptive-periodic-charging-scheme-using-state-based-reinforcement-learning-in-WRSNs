from abc import abstractmethod

from optimizer.Optimizer import Optimizer


class OnDemandOptimizer(Optimizer):
    def __init__(self):
        Optimizer.__init__(self, optimizeType='On-demand')

    @abstractmethod
    def schedule(self, net, mc):
        pass
