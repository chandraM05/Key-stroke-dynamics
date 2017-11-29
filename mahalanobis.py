import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve
def equal_error_rate(user_scores,imposter_scores):
	labels = len(user_scores)*[0]
	labels = labels + len(imposter_scores)*[1]
	fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
	FalseAlarmRates = fpr    
	miss_rate= 1 - tpr
	ad = miss_rate - fpr
	index2 = np.argmax(ad[ad < 0])
	index1 = np.argmin(ad[ad >=0 ])	    
	y = [miss_rate[index2], fpr[index2]]
	x = [miss_rate[index1], fpr[index1]]
	m = ( x[0] -x[1] ) / ( y[1] - x[1] - y[0] + x[0] )
	eer = x[0] + m * ( y[0] - x[0] )
    
	return eer

data = pd.read_csv("DSL-StrongPasswordData.csv")
subjects = data["subject"].unique()
# print subjects
equal_err_rates=[]
fprs=[]
for subject in subjects:

			user_scores = []
			imposter_scores = []
			# take one subject as genuine user
			genuine_user = data.loc[data.subject == subject, "H.period":"H.Return"]
			#take every 5 records of all other users as imposter data
			imposter = data.loc[data.subject != subject,"H.period":"H.Return"][:5]
			#take first 200 records of genuine user as training data
			train = genuine_user[:200]
			# take remainib 200 records of genuine user as testing data
			test_genuine = genuine_user[200:]
            # print test_genuine
            #calculate meane vector
			mean_vector = train.mean().values
            # print mean_vector
            #calculate covariance matrix
			coviance=np.cov(train.T)
            # print coviance

            # for genuine user calculate test score
			for i in range(test_genuine.shape[0]):
				# difference bet mean vector and user vector (x-y)
				diff = mean_vector - test_genuine.iloc[i].values
				# mahalanobis formula
				score = np.dot(np.dot(diff.T,np.linalg.inv(coviance)), diff)
				user_scores.append(score)
	            # print score
	        # for imposter calculate imposter score
			for i in range(imposter.shape[0]):
				# difference bet mean vector and imposter vector (x-y)
				diff = mean_vector - imposter.iloc[i].values
				# mahalanobis formula
				score = np.dot(np.dot(diff.T,np.linalg.inv(coviance)), diff)
				imposter_scores.append(score)
			# calculate equal error rate
			eer=equal_error_rate(user_scores,imposter_scores)
			equal_err_rates.append(eer)
			# fprs.append(fpr)
			# print fpr
print np.mean(equal_err_rates)
            