import simpy

from iostream.Util import Util
from network.MobileCharger import MobileCharger
from network.Network import Network
from optimizer.ondemandoptimizer.RandomOnDemandOptimizer import RandomOnDemandOptimizer

util = Util("../data/ga200_05_simulated.txt")
env = simpy.Environment()
net = Network(env=env, listNodes=util.listNodes, baseStation=util.BaseStation)
mc = MobileCharger(env=env, location=[250, 250])
testedT = 72000
algorithm = RandomOnDemandOptimizer(500)

env.process(mc.operate(net, testedT, algorithm))
env.process(net.runNetwork(testedT))

env.run(until=testedT)
print(net.countDeadNodes())
