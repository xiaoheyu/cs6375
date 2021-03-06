
# coding: utf-8

# In[2]:


# This example has been taken from SciKit documentation and has been
# modifified to suit this assignment. You are free to make changes, but you
# need to perform the task asked in the lab assignment


from __future__ import print_function

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
import pandas as pd
import requests
import io


# In[3]:


print(__doc__)

# Loading the Digits dataset
#digits = datasets.load_digits()


# In[5]:


source =requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data").content 
df = pd.read_csv(io.StringIO(source.decode('utf-8')), header=None)
X = df.iloc[:,1:13]
y = df.iloc[:,0]


# In[6]:


# Split the dataset in two equal parts into 80:20 ratio for train:test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)


# In[7]:


# This is a key step where you define the parameters and their possible values
# that you would like to check.
tuned_parameters = [{'hidden_layer_sizes':[(100,),(50,50),(50,50,50)],'activation': ['logistic','tanh','relu'], 'alpha': [0.0001,0.001,0.005],
                     'learning_rate': ['constant', 'invscaling', 'adaptive']}
                    ]

# We are going to limit ourselves to accuracy score, other options can be
# seen here:
# http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
# Some other values used are the predcision_macro, recall_macro
scores = ['accuracy']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(MLPClassifier(), tuned_parameters, cv=5,
                       scoring='%s' % score)
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print("Detailed confusion matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("Accuracy Score: \n")
    print(accuracy_score(y_true, y_pred))

    print()

# Note the problem is too easy: the hyperparameter plateau is too flat and the
# output model is the same for precision and recall with ties in quality.

