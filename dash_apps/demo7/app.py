import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import os
import pandas as pd
import time


print('PID '+str(os.getpid()))

df = pd.read_csv('stock-ticker.csv')

plotly_config = {
    'showLink': False,
    'displayModeBar': True,
    'displaylogo': False,
    'scrollZoom': True,
    'modeBarButtonsToRemove': ['sendDataToCloud']
}

app = dash.Dash(__name__, static_folder='assets')
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Link(href='/assets/loading_callback.css', rel='stylesheet'),
    html.H1('Finance Explorer'),
    dcc.Tabs(id='tabs',
        children=[dcc.Tab(label='Annotations', value='Annotations'),
                  dcc.Tab(label='Stocks', value='Stocks')]),
    html.Div(id='tab_container')
])

@app.callback(Output('tab_container', 'children'),
    [Input('tabs', 'value')])
def tabs_changed(selected_tab):
    if selected_tab == 'Annotations':
        return html.P('TODO')
    elif selected_tab == 'Stocks':
        return html.Div([
            dcc.Dropdown(
                id='stock_ticker_input',
                options=[{'label': s, 'value': s} for s in df['Stock'].unique()],
            ),
            dcc.Checklist(
                id='graph_options',
                options=[{'label': 'With daily high', 'value': 'with_high'}, {'label': 'With daily low', 'value': 'with_low'}],
                values=[]
            ),
            html.Div(id='graph_container')
        ])
    else:
        return html.P('Something went wrong :(')

@app.callback(Output('graph_container', 'children'),
    [Input('stock_ticker_input', 'value')],
    [State('graph_options', 'values')])
def stock_ticker_dropdown_changed(stock_ticker, graph_options):
    if stock_ticker not in df['Stock'].unique():
        return html.P('Select valid stock ticker from the dropdown...')
    df_ticker = df[df['Stock'] == stock_ticker]
    return dcc.Graph(
        config=plotly_config,
        figure={
            'data': [
                go.Scatter(
                    x=df_ticker['Date'],
                    y=df_ticker['Close'],
                    name='Close',
                    ),
                go.Scatter(
                    x=df_ticker['Date'],
                    y=df_ticker['High'],
                    name='High',
                    visible='with_high' in graph_options
                ),
                go.Scatter(
                    x=df_ticker['Date'],
                    y=df_ticker['Low'],
                    name='Low',
                    visible='with_low' in graph_options
                ),
            ],
        })

if __name__ == '__main__':
    app.run_server(port=8057)
