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
        return html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='annotations_container', children=[annotations_container()])
        ])
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
    global df_annotations
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
            'layout': {
                'annotations': [
                    {'text': annotation['Text'],
                     'x': annotation['Date'],
                     'y': df_ticker[df_ticker['Date'] == annotation['Date']]['Close'].values[0],
                     'showarrow': 'true'}
                    for _, annotation in df_annotations.iterrows()
                    if annotation['Ticker'] == stock_ticker
                ]
            }
        })

df_annotations = pd.DataFrame([
    {'id': 1, 'Ticker': 'AAPL', 'Date': '2016-04-01', 'Text': 'Bought 100 shares'},
    {'id': 2, 'Ticker': 'AAPL', 'Date': '2016-09-16', 'Text': 'Sold 68 shares'},
    {'id': 3, 'Ticker': 'TSLA', 'Date': '2016-09-23', 'Text': 'Bought 100 shares'},
    {'id': 4, 'Ticker': 'TSLA', 'Date': '2016-10-07', 'Text': 'Bought 20 shares'},
    {'id': 5, 'Ticker': 'TSLA', 'Date': '2017-01-25', 'Text': 'Sold 70 shares'}])

def annotations_container():
    global df_annotations
    return html.Div([
        html.Table(
            [html.Tr([html.Th(col) for col in ['Ticker', 'Date', 'Text', '']])] +
            [html.Tr([
                html.Td(row['Ticker']), html.Td(row['Date']), html.Td(row['Text']),
                html.Td(dcc.Link('Delete', href='/annotations/delete/' + str(row['id'])))
            ]) for _, row in df_annotations.iterrows()] +
            [html.Tr([
                html.Td([dcc.Input(id='annotation_ticker')]),
                html.Td([dcc.Input(id='annotation_date')]),
                html.Td([dcc.Input(id='annotation_text')]),
                html.Td([dcc.Link('Insert', href='/annotations/insert')]),
            ])]
        )
    ])

@app.callback(Output('annotations_container', 'children'),
    [Input('url', 'pathname')],
    [State('annotation_ticker', 'value'),
     State('annotation_date', 'value'),
     State('annotation_text', 'value')])
def annotations_container_action(path, annotation_ticker, annotation_date, annotation_text):
    global df_annotations
    if path.startswith('/annotations/delete/'):
        id_to_delete = int(path[20:])
        df_annotations = df_annotations[df_annotations['id'] != id_to_delete]
    if path.startswith('/annotations/insert'):
        df_annotations = df_annotations.append(
            {'id': int(max(df_annotations['id'])+1),
             'Ticker': annotation_ticker,
             'Date': annotation_date,
             'Text': annotation_text},
             ignore_index=True)
    return annotations_container()


if __name__ == '__main__':
    app.run_server(port=8058)
