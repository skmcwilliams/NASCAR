#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 14:52:06 2021

@author: skm
"""
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from data import Live,Soup

def model(model_df):
    try:
        model_df['Pos'] = pd.to_numeric(model_df['Pos'])
    except ValueError: 
        """this should already be done, if it can't be done, then data for 
            future race is on website, so return dataframe without predictions"""
        return model_df
    
    train_df = pd.read_csv('gen6_stats.csv')
    train_df = train_df.rename(columns={'Start':'Started'})
    train_df = train_df.drop(columns = ['Unnamed: 0','Driver','S1','S2','S3','Pts','Laps','Led'
                        ,'Status','Rating','Team','track'])

    dummy_cols= 'Make'
    train_df = pd.concat([train_df,pd.get_dummies(train_df[dummy_cols],drop_first=False)], axis=1) #Create dummy variables, drop first to remove colinearity
    train_df = train_df.drop(columns=dummy_cols)
    
    X_train = train_df[train_df.columns.difference(['Finish'])]
    y_train = train_df['Finish']
    
    test_dummy = 'Make'
    model_df = pd.concat([model_df,pd.get_dummies(model_df[test_dummy],drop_first=False)], axis=1) #Create dummy variables, drop first to remove colinearity
    model_df = model_df.drop(columns=test_dummy)
    model_df = model_df.drop(columns='Driver')
    
    X_test = model_df[model_df.columns.difference(['Pos'])]
    model = XGBRegressor(n_jobs=-1,learning_rate=0.01,n_estimators=1000)
    
    model.fit(X_train,y_train)
    y_hat = model.predict(X_test)
    y_hat = list(map(int,y_hat))
    for n,i in enumerate(y_hat):
        if y_hat.count(i)>1:
            y_hat[n]= i-1
    
    pred_df = model_df
    pred_df.insert(1,'Predicted Finishing Pos',pd.Series(y_hat,index=X_test.index))
    pred_df.insert(1,'Driver',pd.Series(model_df['Driver'],index=X_test.index))
    pred_df.insert(2,'Current vs. Predicted',pred_df['Predicted Finishing Pos']-pred_df['Pos'])
    pred_df = pred_df.drop(columns=pred_df.columns[-3:])
    return pred_df

def clean_df(df):
    df = df.drop(columns=df.columns[4:])
    return df
    

