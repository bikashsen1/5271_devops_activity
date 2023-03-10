# -*- coding: utf-8 -*-
"""BankNote.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12IYLQNQX2EHyyOkOpkNSqDNMr6FN3KTP
"""

#importing the required libraries 
import os
import numpy as np # importing for numeric operations
import pandas as pd # importing for data analysis

from sklearn.model_selection import train_test_split #for splitting the data into train and test

## for standardize and Encoding the data
from sklearn.preprocessing import StandardScaler

# for model Building 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# for evaluate the model performance
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, f1_score,classification_report

"""## Mounting the drive"""

from google.colab import drive
drive.mount('/content/drive')

import warnings
warnings.filterwarnings("ignore")

"""## Load the data"""

Bank_note =pd.read_csv("/content/drive/MyDrive/Turingminds/DevOps/Activity/BankNote_Authentication.csv")

"""## EDA"""

# checking the top 5 records
Bank_note.head()

# checking the bottom 5 records
Bank_note.tail()

# checking how many coloumns & rows are there in the data
Bank_note.shape

#checking the columns names
Bank_note.columns

# checking the data types of the each attributes
Bank_note.dtypes

# checking the summary statistics
Bank_note.describe()

# checking how many  unique data are present
Bank_note.nunique()

# checking the null values 
Bank_note.isnull().sum()

Bank_note['class'].value_counts(normalize=True)*100

"""## split the data into train & test """

X=Bank_note.drop(['class'],axis=1)
y=Bank_note['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=5271, stratify=y)

# Checking the shape of the train & test data
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# scaling the data
scaler =StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)

scores = pd.DataFrame(columns=['Model', 'Train_Accuracy', 'Train_Recall', 'Train_Precision', 'Train_F1_Score', 
                               'Test_Accuracy', 'Test_Recall', 'Test_Precision', 'Test_F1_Score'])

def get_metrics(train_actual, train_predicted, test_actual, test_predicted, model_description, dataframe):

    train_accuracy  = accuracy_score(train_actual, train_predicted)
    train_recall    = recall_score(train_actual, train_predicted, average="weighted")
    train_precision = precision_score(train_actual, train_predicted, average="weighted")
    train_f1score   = f1_score(train_actual, train_predicted, average="weighted")
    
    test_accuracy   = accuracy_score(test_actual, test_predicted)
    test_recall     = recall_score(test_actual, test_predicted, average="weighted")
    test_precision  = precision_score(test_actual, test_predicted, average="weighted")
    test_f1score    = f1_score(test_actual, test_predicted, average="weighted")

    dataframe       = dataframe.append(pd.Series([model_description, 
                                                  train_accuracy, train_recall, train_precision, train_f1score,
                                                  test_accuracy, test_recall, test_precision, test_f1score],
                                                 index=scores.columns ), 
                                       ignore_index=True)

    return(dataframe)

"""## Build the Models

## LogisticRegression
"""

model1 = LogisticRegression()
model1.fit(X_train,y_train)

train_pred = model1.predict(X_train)
test_pred = model1.predict(X_test)

scores = get_metrics(y_train, train_pred, y_test, test_pred, "LogisticRegression", scores)
scores

"""## RandomForest_classifier"""

model2 = RandomForestClassifier(n_estimators=30)
model2.fit(X_train,y_train)

train_pred = model2.predict(X_train)
test_pred = model2.predict(X_test)

scores = get_metrics(y_train, train_pred, y_test, test_pred, "RandomForest", scores)
scores

print(test_pred)

"""save as pickle file"""

import pickle
pickle_out = open("model1.pkl","wb")
pickle.dump(model1, pickle_out)
pickle_out.close()

