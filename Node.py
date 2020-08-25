import random
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import recall_score

label_category = [1,0]
prevalance = 0.5

class Node:
    def __init__(self,node_id,pred_auc,prevalance):
        self.id = node_id
        self.__spammer_score = 0
        self.pred_auc = pred_auc
        self.__recall = 0
        self.__fallout = 0
        self.__auc = 0
        self.pred_history = []
        self.__prevalance = prevalance
    
    def get_info(self,pred_history = False):
        print(f"id : {self.id}, spammer score : {self.__spammer_score:.2f}, pred_auc : {self.pred_auc:.2f}, recall : {self.__recall:.2f}, fallout : {self.__fallout:.2f}, auc : {self.__auc:.2f}")
        if pred_history:
            print(self.pred_history)

    def make_label(self,label_category):
        return random.choices(label_category, weights=[self.pred_auc] + [(1-self.pred_auc)/(len(label_category) -1) for i in range(len(label_category)-1)],k=1)
    
    def calculate_matrix(self,recall,fallout):
        self.__recall = recall
        self.__fallout = fallout
        self.__auc = recall*self.__prevalance + (1-fallout)*(1-self.__prevalance)
        self.__spammer_score = (recall-fallout)**2

    @property
    def auc(self):
        return self.__auc

    @property
    def spammer_score(self):
        return self.__spammer_score



node = Node(1,0,0.46)

# test_size = 100000
# y = random.choices([1,0],weights=[prevalance,1-prevalance],k=test_size) 


# for i in range(test_size):
#     if random.choices([1,0],weights=[node.pred_auc,1-node.pred_auc],k=1) == [1]:
#         node.pred_history.append(y[i])
#     else :
#         node.pred_history.append(abs(y[i]-1))

# tn, fp, fn, tp = confusion_matrix(y,node.pred_history).ravel()

# recall = tp/(tp+fn) # recall
# fallout = fp/(fp+tn) # fallout

# node.calculate_matrix(recall,fallout)

# node.get_info()

