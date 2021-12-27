from network.BaseStation import BaseStation
from network.Network import Network
from network.Node import Node


class Util:
    def __init__(self, filePath):
        self.filePath = filePath
        self.listNodes = []
        f = open(self.filePath, 'r')
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                tmp = tuple(map(float, line.split(" ")[:2]))
                self.BaseStation = BaseStation([tmp[0], tmp[1]])
                continue
            tmp = tuple(map(float, line.split(" ")[:4]))
            self.listNodes.append(Node(energy=tmp[3], energyCR=tmp[2], location=[tmp[0], tmp[1]]))

    def setUpNetwork(self, enviroment):
        network = Network(env=enviroment, listNodes=self.listNodes, listMCs=self.listMCs,
                          listChargingLocations=self.listChargingLocations,
                          baseStation=self.BaseStation)
        return network
