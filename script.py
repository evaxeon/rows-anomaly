#Testing script just to explore some anomaly searching methods.


import csv
import pickle
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

np.seterr(divide='ignore', invalid='ignore')

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

def largeOpenAndDump(filename, chunksize, fields):
    pidDict = {}
    r = pd.read_csv(filename, chunksize=chunksize, usecols=fields)
    chunkCounter = 0
    for chunk in r:
        print("Working on chunk #{}".format(chunkCounter))
        chunkCounter += 1
        for index, row in chunk.iterrows():
            if int(row[fields[1]]) in pidDict.keys():
                pidDict[int(row[fields[1]])].append([int(row[fields[0]])])
            else:
                pidDict[int(row[fields[1]])] = [ [int(row[fields[0]])] ]
            #print(row[fields[0]], row[fields[1]])
    with open('{}_dict_n.pickle'.format(filename), 'wb') as handle:
        pickle.dump(pidDict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def isolationForestProc():
    print("Applying IsolationForest algorithm...")
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

def oneClassSvmProc():
    print("Applying OneClassSVM algorithm...")
    with open('dataset2_dict.pickle', 'rb') as handle:
        b = pickle.load(handle)

    for key in b.keys():
        print("Working on key {}".format(key))
        model = OneClassSVM()
        model.fit(b[key])
        anomaly = model.predict(b[key])
        for an in anomaly:
            if an == 1:
                print('Not anomaly!')
            else:
                print('Anomaly!')


#oneClassSvmProc()
chunksize = 1000000
fields = ['REQTIME', 'PID']
filename = 'dataset2.csv'
largeOpenAndDump(filename, chunksize, fields)