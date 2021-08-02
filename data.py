#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 16:15:03 2021

@author: skm
"""
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time

class Soup():
    def __init__(self):
        pass
    
    def get_soup(self,url):
        request = requests.get(url)
        soup = bs(request.text,'lxml')
        return soup
        

class Live(Soup):
    def __init__(self):
        pass
    
    def get_leaderboard(self):
        """get live leaderboard"""
        s = Soup()
        soup = s.get_soup('https://scores.nbcsports.com/racing/leaderboard.asp?series=NASCAR')
        table = soup.find('table',class_="shsTable shsBorderTable")
        df = pd.read_html(str(table))[0]
        
        
        new_header = df.iloc[2] #headers are on 3d row
        df = df[3:] #data begins 3rd row
        df.columns = new_header # set header names to original names
        
        #make all numeric columns so
        try:
            df['Pos'] = pd.to_numeric(df['Pos'])
        except ValueError: #means data has been removed for upcoming race, return df anyway
            return df.reset_index()
            
        df['Started']= pd.to_numeric(df['Started'])
        df['Car #']= pd.to_numeric(df['Car #'])
        df['Posiitons Gained'] = df['Started'] - df['Pos']
        
        df = df.reset_index()
        df.drop(columns='index',inplace=True)
        return df
    
class Gen_6(Soup):
    def __init__(self):
        pass
    
    def format_df(self,df):
        df.rename(columns={'#':'Car #'}, inplace=True)
        df = df[:-1]
        df = df[df['Finish']!='Finish'] 
        df['Car #'] = df['Car #'].apply(lambda x: x.strip('#'))
        df['Car #'] = list(map(int,df['Car #']))
        df['Start'] = list(map(int,df['Start']))
        df['Finish'] = list(map(int,df['Finish']))
        df = df.drop(columns='Unnamed: 0',errors='ignore')
        return df
    
    def get_links(self,start_year,end_year):
        s = Soup()
        for season in range(start_year,end_year+1):
            soup = s.get_soup(url=f'https://www.driveraverages.com/nascar/year.php?yr_id={season}')
            div = soup.find('div',class_='clearfix')
            hrefs = div.find_all('a',href=True)
            for r in hrefs:
                if 'race' in r['href']:
                    yield r['href']

    def get_stats(self,links):
        s = Soup()
        #main_df = pd.DataFrame()
        for l in list(links):
            soup_2 = s.get_soup(f'https://www.driveraverages.com/nascar/{l}')
            stats = soup_2.find('table',class_="sortable tabledata-nascar table-large") #race results table
            race = soup_2.find('table',class_='tabledata-wrapper') # getting track name from table
            track_name = race.find('th').text.split()[:-3] # get track name, ignore date
            track = ''.join(track_name) # join in case track is mulitple words
            df = pd.read_html(str(stats))[0]
            df['track'] = track
            #main_df = main_df.append(df)
            yield df
    
    def concat(self,df_list):
        dfs = list(df_list)
        df = pd.concat(dfs)
        return df
            
if __name__=='__main__':
    start = time.time()         
    gen = Gen_6()
    links = gen.get_links(2013,2021)
    season_dfs = gen.get_stats(links)
    hist_df = gen.concat(season_dfs)
    hist_df = gen.format_df(hist_df)
    hist_df.to_csv('gen6_stats_generators.csv')
    end = time.time()
    runtime = (end-start)/60
    print(f'runtime of {runtime} mins')