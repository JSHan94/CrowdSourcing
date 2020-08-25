import random
import numpy as np

class PoB:

    def __init__(self):
        self.node_num = 1000
        self.active_threshold = 0.8
        self.node_list = []
        for i in range(self.node_num):
            auc = round(random.random(),2)
            if auc >= 0.8:
                self.node_list.append(dict(id=i, auc=auc, servi=1,active=True))
            else : 
                self.node_list.append(dict(id=i, auc=auc, servi=1,active=False))
            
            
