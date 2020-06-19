# Jerry Day
# Bzan 544
# 2/9/2020

# App to visualize movie schedules...

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import datetime

import os
import re
import plotly.figure_factory as ff
import CreateSchedules

# Run CreateSchedules here to make sure that all the necessary schedules are created.
CreateSchedules.ScheduleCheckAndMake()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Creates the schedule Dict for the dropdown... only for files that end in _Schedules.csv
schedules =  [ f.name for f in os.scandir("Schedules") if f.is_file() & bool(re.search(".*_Schedule\.csv$", f.name)) ]
scheduleNamesDict = [{'label' : re.search('^(.+?)_Schedule\.csv', sch).group(1), 'value': sch} for sch in schedules]

app.layout = html.Div(children =
    [html.H1('''Cinema Schedule Creator/Viewer'''
            ),
    html.P('by Dr. Jerry Day'),
    html.H3('Below is the list of schedules generated.'),       
    html.P(
        [html.Label('Choose a Schedule'),
         dcc.Dropdown(id = 'scheduleFileDropdown', options= scheduleNamesDict, multi = False, value = "TB_original_Schedule.csv")
        ],
        style = {'width': '400px'}
# Other paragraph style options.
#         style = {'width': '400px',
#                                     'fontSize' : '20px',
#                                     'padding-left' : '100px',
#                                     'display': 'inline-block'}
    ),
    dcc.Graph(
        id = "movieGantt"
    ) 

]
                     ) # end applayout definition...

@app.callback(
    Output('movieGantt', 'figure'),
    [Input('scheduleFileDropdown', 'value')])
def createFigure(filename):
    showit = []
    if filename:
        startTimesDF = pd.read_csv("Schedules/" + filename)
        showit = [dict(Task= row[1].theatre, Start= row[1].startTimeDate, Finish = row[1].endTimeDate, Resource = row[1].movie)  for row in startTimesDF.iterrows()] 
    fig = ff.create_gantt(showit, index_col='Resource', group_tasks=True, show_hover_fill = True)
    return fig
    
if __name__ == "__main__":
    app.run_server(debug=True)