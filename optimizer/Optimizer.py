from abc import ABC


class Optimizer(ABC):
    def __init__(self, optimizeType):
        """
        An optimizer
        :param optimizeType: the type of this optimizer(OnDemand or Offline)
        """
        ABC.__init__(self)
        self.optimizeType = optimizeType
