#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 14:39:24 2021

@author: skm
"""
import pandas as pd
from data import Live
from model import clean_df,model
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px


def generate_table(dataframe):
    max_rows=50
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

live = Live()
live_df = live.get_leaderboard()
live_df = clean_df(live_df)
model_df = model(live_df)

plot_df = pd.read_csv('gen6_stats.csv')
plot_df = base_df.drop(columns = ['Unnamed: 0','S1','S2','S3'])


# BAR CHART OF WINS/PODIUMS PER MAKE/TEAM/DRIVER
podiums = plot_df[plot_df['Finish']<4]
team_hist = px.histogram(podiums,x='Team',title='Team Podiums Throughout Gen 6 Era').update_xaxes(categoryorder='total descending')
make_hist = px.histogram(podiums,x='Make',title='Make Podiums Throughout Gen 6 Era').update_xaxes(categoryorder='total descending')
driver_hist = px.histogram(podiums,x='Driver',title='Driver Podiums Throughout Gen 6 Era').update_xaxes(categoryorder='total descending')
track = 'Pocono'
track_df = podiums[podiums['track']==f'{track}']
track_make_hist=px.histogram(track_df,x='Driver',title=f'Driver Podiums Throughout Gen 6 Era at {track}').update_xaxes(categoryorder='total descending')
# PODIUMS AT SELECTED TRACKS BY MAKE/TEAM/DRIVER

# stock language needed for Plotly Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Custom Dash app language
app.layout = html.Div(children=[
    
    html.Div([ # main header
        html.H1(children='NASCAR Gen 6 Stats and Race Prediction'),

        html.H3(children='''# add small descriptor to link to code and give credit to data
                Code can be found here: https://github.com/skmcwilliams/NASCAR
                Live data from nbcsports.com
                Gen 6 data from driveraverages.com
            '''),
        html.H2(children=f'Live Leaderboard For Race at f{track}'),
        html.H4(children='Predicted Finishing Posiiton Will Update at Start of Race'),
        generate_table(model_df),
        dcc.Graph(id='Gen 6 Stats and Race Stats for Current Race')
        """STOPPING HERE, ADD BAR CHARTS AND STUFF."""
         
        
        ])


