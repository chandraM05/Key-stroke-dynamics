import numpy as np
import pandas as pd
from statsmodels import robust
from sklearn import metrics

data1 = pd.read_csv("DSL-StrongPasswordData.csv")
subjects = data1["subject"].unique()
# print (subjects)

data={}


def Calc_equal_err_rate(actual_user_Score,imposter_Score):

	# print len(actual_user_Score),len(imposter_Score)
	classes = [0]*len(actual_user_Score) + [1]*len(imposter_Score)
	fpr, tpr, thresholds = metrics.roc_curve(classes, actual_user_Score + imposter_Score)
	false_alarm_rates = fpr
	miss_rate= 1 - tpr
	all_dist = miss_rate - false_alarm_rates
	idx1 = np.argmin(all_dist[all_dist >=0 ])
	idx2 = np.argmax(all_dist[all_dist < 0])
	x = [miss_rate[idx1], false_alarm_rates[idx1]]
	y = [miss_rate[idx2], false_alarm_rates[idx2]]
	m = ( x[0] -x[1] ) / ( y[1] - x[1] - y[0] + x[0] )
	equal_err_rate = x[0] + m * ( y[0] - x[0] )
	return equal_err_rate

total_genuine_samples = 0
total_imposter_samples = 0

# collecting all the required information
for subject in subjects:
	user_scores = []
	imposter_scores = []
	subj_data = {}
	genuine_user = data1.loc[data1.subject == subject, "H.period":"H.Return"]

	train_subj = genuine_user[:200]
	test_subj = genuine_user[200:]
	mean_vector = train_subj.mean().values
	subj_data["train"]=train_subj.values.tolist()
	subj_data["test_user"] = test_subj.values.tolist()
	subj_data["mean"] = mean_vector.tolist()
	data[subject]=subj_data
	total_genuine_samples =total_genuine_samples + 200

# for keys in data :
# 	print (len(data[keys]["train"]),keys,len(data[keys]["test_user"]))
# 	print (data[keys]["mean"])
	# print data[keys]["mean"]

# collectings all imposter data for each subject
for subj1 in subjects :
	imposter_test=[]
	for subj2 in subjects :
		if subj1 != subj2 :
			temp = data[subj2]["train"][:5]
			total_imposter_samples = total_imposter_samples + 5
			for i in temp :
				imposter_test.append(i)

	arr = np.matrix(data[subj1]["train"])
	array = robust.mad(arr,axis=0)

	subj_data=data[subj1]
	subj_data["imposter_test"] = imposter_test
	subj_data["sd"] = array.tolist()
	data[subj1]=subj_data

# for keys in data :
	# print len(data[keys]["train"]),keys,len(data[keys]["test_user"]),len(data[keys]["sd"]),len(data[keys]["mean"])
	# print type(data[keys]["imposter_test"]),len(data[keys]["imposter_test"]),data[keys]["imposter_test"][0]

# Calculating user score and imposter score 
equal_err_rates=[]

false_negative = 0.0
false_positive = 0.0


# Manhattan model

for key in data :
	user_score = []
	imposter_score = []
	mean = data[key]["mean"]
	sd = data[key]["sd"]
	user_test_data = data[key]["test_user"]
	imposter_test_data = data[key]["imposter_test"]

	for sample in user_test_data :
		sample_score = 0.0
		for i in range(0,len(mean)) :
			sample_score = sample_score + abs(mean[i]-sample[i])/sd[i]
		user_score.append(sample_score)

	for sample in imposter_test_data :
		sample_score = 0.0
		for i in range(0,len(mean)) :
			sample_score = sample_score + abs(mean[i]-sample[i])/sd[i]
		imposter_score.append(sample_score)

	standard_deviation = np.std(user_score)
	mean_standard = np.mean(user_score)
	# print key , standard_deviation,mean_standard

	# checking for false negatives ,if score is within range then its treated as outlier
	for score in user_score :
		if score > mean_standard + standard_deviation or score < mean_standard -standard_deviation :
			false_positive = false_positive + 1 
	# checking for false positives
	for score in imposter_score :
		if score < mean_standard + standard_deviation and score > mean_standard -standard_deviation :
			false_negative = false_negative + 1


	error=Calc_equal_err_rate(user_score,imposter_score)
	equal_err_rates.append(error)
# print equal_err_rates,len(equal_err_rates)

print "False Positive   : " , false_positive / total_imposter_samples
print "False Negative   : " , false_negative / total_genuine_samples
print "Equal error rate : " , np.mean(equal_err_rates)
# print false_positive / total_imposter_samples + false_negative / total_genuine_samples