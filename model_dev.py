#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 10:42:49 2021

@author: skm
"""
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import mean_absolute_error

base_df = pd.read_csv('gen6_stats.csv')
base_df = base_df.drop(columns = ['Unnamed: 0','S1','S2','S3','Pts','Laps','Led','Status','Rating','Team','track','Driver'])

dummy_cols='Make'
df = pd.concat([base_df,pd.get_dummies(base_df[dummy_cols],drop_first=False)], axis=1) #Create dummy variables, drop first to remove colinearity
df = df.drop(columns=dummy_cols)

target = 'Finish'
X = df[df.columns.difference([target])]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.05,
                                                    random_state=6)

model = XGBRegressor(n_jobs=-1,learning_rate=0.01,n_estimators=500)

model.fit(X_train,y_train)
y_hat = model.predict(X_test)
y_hat = list(map(int,y_hat))
cv_score = cross_val_score(model, X, y, cv=3,scoring='neg_mean_absolute_error')
m= mean_absolute_error(y_test,y_hat)

print(f'MAE: {m}')
print(f'CV MAE Score: {list(map(lambda x: x*-1,cv_score))}')
print(f'Average CV MAE Score: {np.mean(cv_score)*-1}')

pred_df = base_df
pred_df.insert(1,'Predicted Finishing Pos',pd.Series(y_hat,index=X_test.index))
pred_df = pred_df[pred_df['Predicted Finishing Pos']>0]





