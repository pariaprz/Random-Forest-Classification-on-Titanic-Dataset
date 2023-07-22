# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BghF5FF1rVUzHzPYAQANfEdw7XuvAUOQ
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from IPython.display import display , HTML
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

data = pd.read_csv('data.csv')
labels = data.pop('Survived')

data.describe()

data["Age"].fillna(data.Age.mean(), inplace = True)
data.describe()

data.drop(['Name','Ticket', 'PassengerId'],axis = 1, inplace = True)

def describe_categorical(data) :

    display(HTML(data[data.columns[data.dtypes == 'object']].describe().to_html()))
describe_categorical(data)

def clean_cabin(data):
    try:
        return data[0]
    except TypeError :
        return 'None'
data['Cabin'] = data.Cabin.apply(clean_cabin)

categorical_variables = ['Sex', 'Cabin', 'Embarked']

for variable in categorical_variables :
    #fill missing data with the word 'Missing' like it is a new class
    data[variable].fillna('Missing', inplace = True)
    #create an array of dummies
    dummies = pd.get_dummies(data[variable], prefix = variable)
    #update data to include dummies and drop the main variable
    data = pd.concat([data, dummies], axis= 1)
    data.drop([variable], axis=1, inplace = True)

"""# New Section"""

def printall(data, max_rows = 10):

    display(HTML(data.to_html(max_rows=max_rows)))
printall(data)

train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size = 0.325, random_state = 42)
train_data.to_csv('train.csv')
test_data.to_csv('test.csv')

model = RandomForestClassifier(n_estimators=  100, bootstrap = True, oob_score = True, random_state = 42)
model.fit(train_data, train_labels)

pred_test = model.predict(test_data)

print("   Accuracy: {}".format(metrics.accuracy_score(test_labels, pred_test)))

print(classification_report(test_labels,pred_test))

conf_matrix = confusion_matrix(test_labels,pred_test)

plt.figure(figsize=(8,5))
sns.heatmap(conf_matrix, annot=True)
plt.title('Confusion Matrix')
plt.tight_layout()

def add_predict(pred_test):
  aa = pd.read_csv("test.csv")
  aa.insert(2, column = "predict", value = pred_test)
  aa.head()

add_predict(pred_test)