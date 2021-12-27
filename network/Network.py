class Network:
    def __init__(self, env, listNodes, baseStation):
        self.env = env
        self.listNodes = listNodes
        self.baseStation = baseStation
        for node in self.listNodes:
            node.env = self.env
        baseStation.env = self.env

    def runNetwork(self, simulateTime):
        """
        The operation of a network
        :param simulateTime: the time limit of the operation
        """
        for node in self.listNodes:
            self.env.process(node.operate(simulateTime=simulateTime))
        yield self.env.timeout(simulateTime)
        return

    def countDeadNodes(self):
        """
        :return return the number of dead nodes
        """
        count = 0
        for node in self.listNodes:
            if node.status == 0:
                count += 1
        return count
