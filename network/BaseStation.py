import scipy.spatial.distance as distance


class BaseStation:
    def __init__(self, location):
        """
        The initialization for basestation
        :param location: the coordinate of a basestation
        """
        self.env = None
        self.location = location

    def chargeMC(self, mc, t=0):
        """
        MC is replenished at the base station. It takes 0(s) to replace the battery
        :param mc: the mc needs charging
        :param t: the time to replenish
        :return: yield t(s) to time management system (in this case, t = 0)
        """
        if distance.euclidean(mc.location, self.location) == 0:
            mc.energy = mc.capacity
        yield self.env.timeout(t)
