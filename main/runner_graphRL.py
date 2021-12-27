import simpy

from iostream.Util import Util
from network.MobileCharger import MobileCharger
from network.Network import Network
from optimizer.offlineoptimizer.GraphRL.GraphRLOptimizer import GraphRlOptimizer

util = Util("../data/ga200_05_simulated.txt")
env = simpy.Environment()
net = Network(env=env, listNodes=util.listNodes, baseStation=util.BaseStation)
mc = MobileCharger(env=env, location=[250, 250])
testedT = 32000
algorithm = GraphRlOptimizer(env=env, T=20000, testedT=testedT)

env.process(mc.operate(net, testedT, algorithm))
env.process(algorithm.controller(mcs=[mc], net=net))
env.process(net.runNetwork(testedT))

env.run(until=testedT)
print('Time: ' + str(env.now) + ' The number of dead node:' + str(net.countDeadNodes()))
