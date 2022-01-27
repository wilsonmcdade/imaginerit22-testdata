"""
models.py for simulated bl rssi data
Wilson McDade
"""

import randmac
import math
import random

FIELDSIZE = 600

uelist = []

class ESP:
    def __init__(self,name,outputmode,espnum):
        self.name = name
        self.pos = (random.randint(16, FIELDSIZE - 16),random.randint(16, FIELDSIZE - 16))
        self.outputmode = outputmode

        print("Created ESP #{} name: {}, pos: {}".format(name[3:],name,self.pos))

    def sniff(self):
        returnable = []

        for ue in uelist:
            uepos = ue.get_pos()
            uedist = self.get_distance(uepos)

            if uedist < 30:
                uename, uemac = ue.get_identifiers()

                returnable.append({    
                            "uename":   uename,
                            "macaddr":  uemac,
                            "rssi":     round(self.get_RSSI(uedist),3),
                            "dist":     round(self.get_distance(ue.get_pos()),3),
                            "pos":      ue.get_pos()})

        return returnable

    def get_distance(self, uepos):
        return ((uepos[0]-self.pos[0])**2 + (uepos[1]-self.pos[1])**2)**0.5

    def get_RSSI(self,distance):
        if distance < 25:

            """
            distance -> rssi conversion found here:
                https://www.ijcaonline.org/research/volume137/number13/jayakody-2016-ijca-909028.pdf

            -(10n*log(d)+A) where:
                n is path-loss exponent (usually between 1.7-3.0 for indoor spaces
                d is distance
                A is RSSI value at 1 meter reference distance -- estimated to be 50
                    from this experiment:
                    https://github.com/neXenio/BLE-Indoor-Positioning/wiki/RSSI-Measurements
            """

            return -((10*(random.uniform(1.7,2))*math.log(distance,10))+(50))
        else:
            return 80.001

class UE:
    def __init__(self, name):
        self.name = name
        self.macaddr = randmac.RandMac("00:00:00:00:00:00")
        self.pos = (random.randint(0,FIELDSIZE),random.randint(0,FIELDSIZE))
        self.velocity = random.randint(-5,5)
        self.direction = (random.randint(-1,1),random.randint(-1,1))

        uelist.append(self)

    def get_pos(self):
        return self.pos

    def get_name(self):
        return self.name

    def update(self):
        if not self.check_bounds():
            self.velocity += random.randint(-2,2)
            self.direction = (self.direction[0]-random.randint(-1,1),self.direction[1]-random.randint(-1,1))
        self.pos = (self.pos[0] + self.velocity*self.direction[0],self.pos[1]+self.velocity*self.direction[1])

    def get_identifiers(self):
        return self.name, str(self.macaddr)

    def check_bounds(self):
        if (self.pos[0] < 5) or (self.pos[0] > FIELDSIZE-5) or (self.pos[1] < 5) or (self.pos[1] > FIELDSIZE-5):
            self.velocity = 5
            self.direction = (0-self.direction[0],0-self.direction[1])
            return False
        else:
            return True
