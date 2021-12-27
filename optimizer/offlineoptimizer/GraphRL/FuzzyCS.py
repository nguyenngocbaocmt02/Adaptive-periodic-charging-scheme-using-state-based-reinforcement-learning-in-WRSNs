from simpful import *


class FuzzyCS:
    def __init__(self):
        self.FS = FuzzySystem()
        self.initialize()

    def initialize(self):
        RS_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=0.05), term='low')
        RS_2 = FuzzySet(function=Trapezoidal_MF(a=0, b=0.05, c=0.05, d=0.15), term='moderate')
        RS_3 = FuzzySet(function=Trapezoidal_MF(a=0.05, b=0.15, c=0.15, d=0.2), term='high')
        RS_4 = FuzzySet(function=Trapezoidal_MF(a=0.15, b=0.2, c=1, d=1), term='veryhigh')
        LV1 = LinguisticVariable([RS_1, RS_2, RS_3, RS_4], concept='RS', universe_of_discourse=[0, 1])
        self.FS.add_linguistic_variable('RS', LV1)

        ESR_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=0.1, d=0.25), term='low')
        ESR_2 = FuzzySet(function=Trapezoidal_MF(a=0.1, b=0.3, c=0.4, d=0.6), term='moderate')
        ESR_3 = FuzzySet(function=Trapezoidal_MF(a=0.4, b=0.6, c=0.65, d=0.85), term='high')
        ESR_4 = FuzzySet(function=Trapezoidal_MF(a=0.65, b=0.85, c=1, d=1), term='veryhigh')
        LV2 = LinguisticVariable([ESR_1, ESR_2, ESR_3, ESR_4], concept='ESR', universe_of_discourse=[0, 1])
        self.FS.add_linguistic_variable('ESR', LV2)

        SAFE_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=0.05, d=0.1), term='verylow')
        SAFE_2 = FuzzySet(function=Trapezoidal_MF(a=0.05, b=0.1, c=0.2, d=0.35), term='low')
        SAFE_3 = FuzzySet(function=Trapezoidal_MF(a=0.2, b=0.35, c=0.40, d=0.55), term='moderate')
        SAFE_4 = FuzzySet(function=Trapezoidal_MF(a=0.4, b=0.55, c=0.6, d=0.75), term='high')
        SAFE_5 = FuzzySet(function=Trapezoidal_MF(a=0.6, b=0.75, c=1, d=1), term='veryhigh')
        LV3 = LinguisticVariable([SAFE_1, SAFE_2, SAFE_3, SAFE_4, SAFE_5], concept='SAFE', universe_of_discourse=[0, 1])
        self.FS.add_linguistic_variable('SAFE', LV3)

        # Define fuzzy rules
        R1 = 'IF (RS IS veryhigh) AND (ESR IS low) THEN (SAFE IS low)'
        R2 = 'IF (RS IS veryhigh) AND (ESR IS moderate) THEN (SAFE IS low)'
        R3 = 'IF (RS IS veryhigh) AND (ESR IS high) THEN (SAFE IS high)'
        R4 = 'IF (RS IS veryhigh) AND (ESR IS veryhigh) THEN (SAFE IS high)'

        R5 = 'IF (RS IS high) AND (ESR IS low) THEN (SAFE IS moderate)'
        R6 = 'IF (RS IS high) AND (ESR IS moderate) THEN (SAFE IS moderate)'
        R7 = 'IF (RS IS high) AND (ESR IS high) THEN (SAFE IS high)'
        R8 = 'IF (RS IS high) AND (ESR IS veryhigh) THEN (SAFE IS high)'

        R9 = 'IF (RS IS moderate) AND (ESR IS low) THEN (SAFE IS moderate)'
        R10 = 'IF (RS IS moderate) AND (ESR IS moderate) THEN (SAFE IS moderate)'
        R11 = 'IF (RS IS moderate) AND (ESR IS high) THEN (SAFE IS high)'
        R12 = 'IF (RS IS moderate) AND (ESR IS veryhigh) THEN (SAFE IS veryhigh)'

        R13 = 'IF (RS IS low) AND (ESR IS low) THEN (SAFE IS moderate)'
        R14 = 'IF (RS IS low) AND (ESR IS moderate) THEN (SAFE IS moderate)'
        R15 = 'IF (RS IS low) AND (ESR IS high) THEN (SAFE IS veryhigh)'
        R16 = 'IF (RS IS low) AND (ESR IS veryhigh) THEN (SAFE IS veryhigh)'

        self.FS.add_rules([R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16])

    def operate(self, net, T):
        safeEnergy = []
        maxESR = 0.0001
        RS = 0
        num = 0
        for node in net.listNodes:
            if node.status == 0:
                continue
            maxESR = max(maxESR, node.energyCR)
            if node.energy - T * node.energyCR <= node.threshold:
                RS += 1
            num += 1
        print(str(RS) + ' ' + str(num))
        if num == 0:
            num = 1
        RS = RS / num
        for node in net.listNodes:
            if node.status == 0:
                safeEnergy.append(0)
            else:
                self.FS.set_variable('RS', RS)
                self.FS.set_variable('ESR', node.energyCR / maxESR)
                # Perform Madman inference and print output
                safeEnergy.append(
                    (self.FS.Mamdani_inference(['SAFE'])['SAFE']) * (node.capacity - node.threshold) + node.threshold)
            # print(str(RS) + " " + str(node.energyCR / maxESR)+" "+str(safeEnergy[-1]))
        return safeEnergy
