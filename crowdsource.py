import Node
import random
from sklearn.metrics import confusion_matrix 


class CrowdSource:
    def __init__(self,task_size=1000, prevalance=0.5, good_threshold = 0.8, label_category = [1,0]):
        self.good_threshold = good_threshold
        self.label_category = label_category
        self.prevalance = prevalance
        self.task_size = task_size

        self.good_annotators = []
        self.malicious_annotators = []
        self.spammers = []
        self.annotators = []
        self.y = random.choices(label_category,weights=[self.prevalance] + [(1-self.prevalance)/(len(label_category)-1) for i in range(len(label_category)-1)],k=task_size) 

    def generate_annotators(self,good_num,mal_num,spammer_num):
        node_id = 0
        for i in range(good_num):
            node = Node.Node(node_id, self.good_threshold+random.uniform(-0.1,0.1), self.prevalance)
            self.good_annotators.append(node)
            node_id += 1
        
        for i in range(mal_num):
            node = Node.Node(node_id, abs(random.uniform(-0.1,0.1)), self.prevalance)
            self.malicious_annotators.append(node)
            node_id +=1

        for i in range(spammer_num):
            node = Node.Node(node_id, 0.5+random.uniform(-0.1,0.1), self.prevalance)
            self.spammers.append(node)
            node_id +=1 

        self.annotators = self.good_annotators + self.malicious_annotators + self.spammers


    def nodes_info(self,pred_history=False):
        for node in self.annotators:
            node.get_info(pred_history)
    
    def calculate_matrix(self,annotator):
        tn, fp, fn, tp = confusion_matrix(self.y, annotator.pred_history).ravel()

        recall = tp/(tp+fn)
        fallout = fp/(fp+tn)

        annotator.calculate_matrix(recall,fallout)


    def do_task(self):
        for annotator in self.annotators:
            for idx in range(self.task_size):
                if random.random() < annotator.pred_auc:
                    annotator.pred_history.append(self.y[idx])
                else :
                    annotator.pred_history.append(random.choice([ item for item in self.label_category if item != self.y[idx]]))
            self.calculate_matrix(annotator)

crowd = CrowdSource(1000)

crowd.generate_annotators(10,10,10)
#crowd.nodes_info()

crowd.do_task()
crowd.nodes_info()