"""
Testing logistic regression on nuclear scattering data.
"""

import scipy as sp
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

p_data = sp.sparse.load_npz('/home/taylor/Documents/independent-research/data/pDisc_40000.npz')
C_data = sp.sparse.load_npz('/home/taylor/Documents/independent-research/data/pDisc_40000.npz')
p_labels = np.zeros((p_data.shape[0],))
C_labels = np.ones((C_data.shape[0],))

#print(p_data.shape)
#print(p_labels.shape)
#print(C_data.shape)
#print(C_labels.shape)

full_data = sp.sparse.vstack([p_data, C_data], format='csr')
#print(full_data.shape)
full_labels = np.hstack((p_labels, C_labels))
#print(full_labels.shape)


X_train, X_test, y_train, y_test = train_test_split(full_data, full_labels, test_size=0.25, random_state=0)

#print(X_train.shape)
#print(X_test.shape)

reg = 1e10

lr = LogisticRegression(C=reg)

y_pred = lr.fit(X_train, y_train).predict(X_test)

print("With regularization C=" + str(reg) + " precision: " + str(metrics.precision_score(y_test, y_pred)))
print("With regularization C=" + str(reg) + " accuracy: " + str(metrics.accuracy_score(y_test, y_pred)))
print(metrics.classification_report(y_test, y_pred))
