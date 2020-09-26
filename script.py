#Testing script just to explore some anomaly searching methods.


import csv
import pickle

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


np.seterr(divide='ignore', invalid='ignore')

pidDict = {}

def openAndDump():
    with open('dataset2.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if int(row[2]) in pidDict.keys():
            	    pidDict[int(row[2])].append([int(row[0])])
                else:
            	    pidDict[int(row[2])] = [ [int(row[0])] ]
            line_count += 1
        print("pidDict:")
        print(pidDict)

    with open('dataset2_dict.pickle', 'wb') as handle:
        pickle.dump(pidDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

#openAndDump()


def isolationForest():
    with open('dataset2_dict.pickle', 'rb') as handle:
        b = pickle.load(handle)

    for key in b.keys():
        print("Working on key {}".format(key))
        model = IsolationForest()
        model.fit(b[key])

        scores = model.decision_function(b[key])
        anomaly = model.predict(b[key])
        #print(model)
        #print(scores)
        #print(anomaly)
