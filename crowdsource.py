import random
from matplotlib import pyplot as plt
import numpy as np

class CrowdSource():

    def __init__(self):
        self.test_size = 10000
        self.true_label=[1 for i in range(self.test_size)]
        
    def make_label(self,auc_percent):    
        return random.choices([1,0],weights=(auc_percent, 1-auc_percent),k=self.test_size)
    
    def double_check(self,worker_auc,validator_auc,validator_num = 1):
        # double check method  

        worker_label = self.make_label(worker_auc)
        validator_label = [self.make_label(validator_auc) for i in range(validator_num)]

        auc_label = 0
        for i in range(self.test_size):
            if worker_label[i] == 1 :
                validator = True
                for idx in range(validator_num):
                    if validator_label[idx][i] == 0:
                        validator = False
                if validator:
                    auc_label += 1
        
        res = round(auc_label/self.test_size,4)*100

        return res



    def consensus(self,node_num,node_auc,mal_num = 0):
        
        node_label = [self.make_label(node_auc) for i in range(node_num)]
        node_num += mal_num

        if mal_num>0:
            for i in range(mal_num):
                node_label.append([0 for i in range(self.test_size)])
    
        final_label = []
        
        for test_idx in range(self.test_size):
            consensus = 0
            for node_idx in range(node_num):
                if node_label[node_idx][test_idx] == 1:
                    consensus +=1
            
            if consensus > node_num/2:
                final_label.append(1)
            else :
                final_label.append(0)
        
        auc_label =0
        for i in range(self.test_size):
            if final_label[i] == 1:
                auc_label+=1

        res = round(auc_label/self.test_size,4)*100
        return res

def main():
    crowd = CrowdSource()
    
    # plt.plot([i/100 for i in range(50,100)],[crowd.double_check(i/100,0.99) for i in range(50,100)])
    # plt.plot([i/100 for i in range(50,100)],[crowd.double_check(i/100,0.99,4) for i in range(50,100)])
    # plt.plot([i/100 for i in range(50,100)],[crowd.consensus(3,i/100) for i in range(50,100)])
    # plt.plot([i/100 for i in range(50,100)],[crowd.consensus(5,i/100) for i in range(50,100)])
    #`` plt.plot([i/100 for i in range(50,100)],[crowd.consensus(10,i/100) for i in range(50,100)])
    # plt.plot([i/100 for i in range(50,100)],[crowd.consensus(20,i/100) for i in range(50,100)])
    # plt.xlabel('Annotator Auc')
    # plt.ylabel('Label Auc')
    # plt.title('Experiment Result')
    # plt.legend(['Doublecheck validator_num=1','Doublecheck validator_num=4','Consensus node_num=3','Consensus node_num=5','Consensus node_num=10','Consensus node_num=20'])

    # plt.show()

    node_num = 20
    mal_num = 5
    plt.plot([i/100 for i in range(50,100)],[crowd.consensus(node_num,i/100) for i in range(50,100)]) 
    plt.plot([i/100 for i in range(50,100)],[crowd.consensus(node_num-mal_num,i/100,mal_num) for i in range(50,100)])

    plt.xlabel('Annotator Auc')
    plt.ylabel('Label Auc')
    plt.title('Experiment Result')
    plt.legend([f'consensus node_num={node_num}',f'consensus node_num={node_num},mal_node={mal_num}'])
    #plt.legend()
    plt.show()

    return


if __name__=="__main__":
    main()