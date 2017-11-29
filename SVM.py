import csv,sys
import math,random
import subprocess
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve
from sklearn.svm import OneClassSVM
data = pd.read_csv("DSL-StrongPasswordData.csv")

subjects = data["subject"].unique()

def Calc_equal_err_rate(actual_user_Score,imposter_Score):

  # print len(actual_user_Score),len(imposter_Score)
  classes = [0]*len(actual_user_Score) + [1]*len(imposter_Score)
  fpr, tpr, thresholds = roc_curve(classes, actual_user_Score + imposter_Score)
  false_alarm_rates = fpr
  miss_rate= 1 - tpr
  all_dist = miss_rate - false_alarm_rates
  idx2 = np.argmax(all_dist[all_dist < 0])
  idx1 = np.argmin(all_dist[all_dist >=0 ])
  y = [miss_rate[idx2], false_alarm_rates[idx2]] 
  x = [miss_rate[idx1], false_alarm_rates[idx1]]
 
  m = ( x[0] -x[1] ) / ( y[1] - x[1] - y[0] + x[0] )
  equal_err_rate = x[0] + m * ( y[0] - x[0] )
  return equal_err_rate


def SVM():
    eers = []
    false_negative = 0.0
    false_positive = 0.0

    for subject in subjects:
            
        user_scores = []
        imposter_scores = []
    
        imposter_data = data.loc[data.subject != subject, :]
        train = data.loc[data.subject == subject, "H.period":"H.Return"][:200].values
        test_genuine = data.loc[data.subject == subject, "H.period":"H.Return"][200:].values
        imposter = imposter_data.groupby("subject").head(5).loc[:, "H.period":"H.Return"].values
        clf = OneClassSVM(kernel='rbf',gamma=26)
        clf.fit(train)
        user_scores = -clf.decision_function(test_genuine)
        imposter_scores = -clf.decision_function(imposter)
        user_scores = list(user_scores)
        imposter_scores = list(imposter_scores)

        standard_deviation = np.std(user_scores)
        mean_standard = np.mean(user_scores)

        for score in user_scores :
          if score > mean_standard + standard_deviation or score < mean_standard -standard_deviation :
            false_positive = false_positive + 1 
        # checking for false positives
        for score in imposter_scores :
          if score < mean_standard + standard_deviation and score > mean_standard -standard_deviation :
            false_negative = false_negative + 1

        eers.append(Calc_equal_err_rate(user_scores, imposter_scores))
    #print eers   
    return np.mean(eers) , false_positive / (51*200) , false_negative / (51*250)

equal_err_rate , false_positive ,false_negative = SVM()
print "False Positive   : " , false_positive 
print "False Negative   : " , false_negative 
print "Equal error rate : " , equal_err_rate