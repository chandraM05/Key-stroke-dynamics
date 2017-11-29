--> Comparing Anomaly-Detection Algorithms for Keystroke Dynamics

- study of whether people can be distinguished by their typing rhythms.

--> Applications

- acting as an electronic fingerprint
- access-control and authentication mechanism
- detecting computer-based crimes

-->Data :
	Data consists of 20401 rows and 34 columns .
	NO of rows = # subject * # sessions * #50
	Each row of data corresponds to the timing information for a single repetition of the password by a single subject.
	columns = 34 ,	
	col[0] = subject_id , is a unique identifier for each subject (e.g., s002 or s057) 
	col[1] = sessionIndex,is the session in which the password was typed (ranging from 1 - 8). 
	col[2] = rep, is the repetition of the password within the session (ranging from 1 to 50).
	The remaining 31 columns present the timing information for the password. The name of the column encodes the type of timing information.

	Column names H.key : hold time for the named key (i.e., the time from when key was pressed to when it was released).

	Column names DD.key1.key2 : keydown-keydown time for the named digraph (i.e., the time from when key1 was pressed to when key2 was pressed).

	Column names UD.key1.key2 : keyup-keydown time for the named digraph (i.e., the time from when key1 was released to when key2 was pressed).

	Based on the password lenghth column size varies.

	Each row consists of subject_id,session,repition and the timing information
Timing information is used for training

--> Detectors implemented 
	Manhattan (Scaled) 
		False Positive   :  0.129882352941
		False Negative   :  0.163725490196
		Equal error rate :  0.108286340595
	Mahalanobis 
		Equal error rate :  0.189917805965
	Svm(one class) 
		False Positive   :  0.147647058824
		False Negative   :  0.258901960784
		Equal error rate :  0.120650799483

--> Observation 
	Manhattan performed better than the other two models in terms of false rates and equal error rates .

--> References
Comparing Anomaly-Detection Algorithms for Keystroke Dynamics
- http://www.cs.cmu.edu/~maxion/pubs/KillourhyMaxion09.pdf
- http://www.cs.cmu.edu/~keystroke/