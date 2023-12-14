from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate(pred,type):
    actual = [True] * len(pred)
    if type == 'precision':
        precision = precision_score(actual, pred)
        return precision
    elif type == 'recall':
        recall = recall_score(actual, pred)
        return recall
    elif type == 'f1':
        f1 = f1_score(actual,pred)
        return f1
    else:
        print("Insert from following choices['precision', 'recall', 'f1']")        