import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
# import plotly.graph_objs as go

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader.data import DataReader
import cPickle as pickle
from plotly.graph_objs import Scatter
import json


app = dash.Dash("Bank Distress")
server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.supress_callback_exceptions = True


"""
There are 87 unique PermID's in our dataset.
The colorlover scale provides upto 11 different colour scales, which can be extrapolated to hundreds of colours.
However, we don't want two graphs to be separated by "light yellow" and "less lighter yellow," for example. 
Hence, we will use different line types - solid, dash, dot, and dashdot.
This leaves us with figuring out the colour scheme for 22 colours. (87 // 4)
Using "alpha" value to differentiate is not recommended for the same reason as the above.

"""

"""
For the time being, we will limit the number of selection to 10 institutes.

"""
colorscale = cl.scales['9']['qual']['Paired']

def load_data():
	"""
	
	"""    
	permid_to_name_path = './data/permid_to_name.pkl'
	df_path = './data/data.pkl'
	
	permid_to_name = pickle.load(open(permid_to_name_path, 'rb'))
		
	df = pickle.load(open(df_path, 'rb'))
	return df, permid_to_name


## Load data
df, permid_to_name = load_data()

## The following line is temporary thing.
df = df[['date','permid','entity','headline','txt','sent_list','predictions', 'distress_signal', 'daily_max']]
df['date_converted'] = df.date.apply(lambda x: x.date())

## Create controls
name_options = [{'label': str(name), 'value': str(permid)} for permid, name in permid_to_name.items()]
name_options = sorted(name_options, key=lambda k: k['label']) 

### Plot
@app.callback(
	Output('clickable-graph','figure'),
	[Input('entity_dropdown', 'value')])
def plot_distress(permids):
	"""
	plot_distress() maps the distress signal of all selected permID's
	"""

	"""
	Instead of looping through each permid in the list of selected permids,
	we can do df_subset = df[df['permid'] in permids]
	and group according to the permid.
	"""

	traces = []

	count = 0

	for permid in permids:
		df_subset = df[df['permid'] == permid]

		trace = Scatter(x = df_subset.date_converted,
						y = df_subset['daily_max'],
						name = permid_to_name[permid],
						line = dict(color = colorscale[count]),
						opacity = 0.8)

		traces.append(trace)

		count += 1

	graphs = dict(data = traces,
				  layout = {'margin': {'b': 40, 'r': 40, 'l': 40, 't': 40},
				  			'xaxis' : {'title': 'Date'},
							'yaxis' : {'title': 'Distress Signal', 'range': [0, 1]},
                            'hovermode': 'closest'})

	return graphs

initial_permid = ['4295895317']
initial_headline = '' 
initial_content = ''

@app.callback(
    Output('headline_dropdown', 'options'),
    [Input('clickable-graph', 'clickData'),
     Input('entity_dropdown', 'value')])
def return_news_title(clickData, selected_permid):
    clicked_json = clickData
    clicked_date = clicked_json['points'][0]['x']
    clicked_distress = clicked_json['points'][0]['y']
    clicked_permid = selected_permid[clicked_json['points'][0]['curveNumber']]
    filtered_df = df[(df['date'] == clicked_date) & (df['daily_max'] == clicked_distress) & (df['permid'] == clicked_permid)]    
    headline_list = filtered_df['headline'].tolist()
    return [{'label': headline, 'value': ind} for ind, headline in enumerate(headline_list)]

@app.callback(
    Output('distress_signal_value', 'children'),
    [Input('clickable-graph', 'clickData'),
     Input('entity_dropdown', 'value'),
     Input('headline_dropdown', 'value')])
def display_distress_signal(clickData, selected_permid, title):
    clicked_json = clickData
    clicked_date = clicked_json['points'][0]['x']
    clicked_distress = clicked_json['points'][0]['y']
    clicked_permid = selected_permid[clicked_json['points'][0]['curveNumber']]
    filtered_df = df[(df['date'] == clicked_date) & (df['daily_max'] == clicked_distress) & (df['permid'] == clicked_permid)]    
    return "Distress Signal is: {}".format(filtered_df['distress_signal'].iloc[title])


@app.callback(
    Output('news_content', 'children'),
    [Input('clickable-graph', 'clickData'),
     Input('entity_dropdown', 'value'),
     Input('headline_dropdown', 'value')])
def display_new_content(clickData, selected_permid, title):
    clicked_json = clickData
    clicked_date = clicked_json['points'][0]['x']
    clicked_distress = clicked_json['points'][0]['y']
    clicked_permid = selected_permid[clicked_json['points'][0]['curveNumber']]
    filtered_df = df[(df['date'] == clicked_date) & (df['daily_max'] == clicked_distress) & (df['permid'] == clicked_permid)]    
    return filtered_df['txt'].iloc[title]


app.layout = html.Div([
    html.Div([
        html.H2('Bank Distress',
                style={
                        'position': 'relative',
                        'top': '0px',
                        'left': '10px',
                        'font-family': 'Dosis',
                        'display': 'inline',
                        'font-size': '6.0rem',
                        'color': '#4D637F'
                       })
    ], className='row twelve columns', style={'position': 'relative', 'right': '15px'}),

    html.Div([
        html.Div([
            html.Div([
                html.P('SELECT an institute in the dropdown menu.')
            ], style = {'margin-left': '10px'}),
            dcc.Dropdown(id = 'entity_dropdown',
                        multi = True,
                        value = initial_permid,
                        options = name_options),
            ], className = 'twelve columns' )
        ], className = 'row'),

    html.Div([
        html.Div([
            
            html.Br(),
            html.P('Select a news article for the chosen date and institute'),
            html.Div([dcc.Dropdown(id = 'headline_dropdown')]),
            html.Br(),
            html.Div([
                html.A(id = 'distress_signal_value',
                       style = dict(fontsize = '16px')),
                html.Br(),
                html.P(id = 'news_content',
                      style = dict(fontSize = '14px')),
            ], style = dict(height = '300px'))
        ], className = "twelve columns")
    ], className = 'row' ),

    html.Div([
            dcc.Graph(id = 'clickable-graph',
                #style = dict(width = '700px'),
                figure = dict(data = {},
                layout = {'margin': {'b': 40, 'r': 40, 'l': 40, 't': 40},
                        'xaxis' : {'title': 'Date'},
                        'yaxis' : {'title': 'Distress Signal', 'range': [0, 1]},
                        'hovermode': 'closest'}))
    ], className = 'row' )
], className = 'container')

if __name__ == '__main__':
    app.run_server(debug = True)
