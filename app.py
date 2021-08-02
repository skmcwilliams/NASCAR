#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 14:39:24 2021

@author: skm
"""
import pandas as pd
import numpy as np
from data import Live
from model import clean_df,model
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

live = Live()
live_df = live.get_leaderboard()
live_df = clean_df(live_df)
model_df = model(live_df)

fig = go.Figure(data=[go.Table(
    header=dict(values=list(model_df.columns),
                fill_color='silver',
                align='left'),
    cells=dict(values=[model_df[i] for i in model_df.columns],
               fill_color='lightblue',
               align='left'))
])

fig.show()

plot_df = pd.read_csv('gen6_stats.csv')
plot_df = plot_df.drop(columns = ['Unnamed: 0','S1','S2','S3'])


# BAR CHART OF WINS/PODIUMS PER MAKE/TEAM/DRIVER
podiums = plot_df[plot_df['Finish']<4]
make_hist = px.histogram(podiums,x='Make',title='Make Podiums Throughout Gen 6 Era').update_xaxes(categoryorder='total descending')
driver_hist = px.histogram(podiums,x='Driver',title='Driver Podiums Throughout Gen 6 Era').update_xaxes(categoryorder='total descending')
team_hist = px.histogram(podiums,x='Team',title='Team Podiums Throughout Gen 6 Era').update_xaxes(categoryorder='total descending')
make_hist.show()
driver_hist.show()
team_hist.show()

# BAR CHART OF WINS/PODIUMS PER MAKE/TEAM/DRIVER BASED ON SELECTED TRACK
track = input(f"Type Desired Track from {np.unique(podiums['track'])}: ")
track_df = podiums[podiums['track']==f'{track}']
track_make_hist=px.histogram(track_df,x='Make',title=f'Make Podiums Throughout Gen 6 Era at {track}').update_xaxes(categoryorder='total descending')
track_driver_hist = px.histogram(track_df,x='Driver',title=f'Driver Podiums Throughout Gen 6 Era at {track}').update_xaxes(categoryorder='total descending')
track_team_hist = px.histogram(track_df,x='Team',title=f'Team Podiums Throughout Gen 6 Era at {track}').update_xaxes(categoryorder='total descending')


track_make_hist.show()
track_driver_hist.show()
track_team_hist.show()
