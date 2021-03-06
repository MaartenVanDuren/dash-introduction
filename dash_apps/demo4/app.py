import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import os
import pandas as pd


print('PID '+str(os.getpid()))

df = pd.read_csv('stock-ticker.csv')

plotly_config = {
    'showLink': False,
    'displayModeBar': True,
    'displaylogo': False,
    'scrollZoom': True,
    'modeBarButtonsToRemove': ['sendDataToCloud']
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Finance Explorer'),
    dcc.Dropdown(
        id='stock_ticker_input',
        options=[{'label': s, 'value': s} for s in df['Stock'].unique()],
    ),
    html.Div(id='graph_container')
])

@app.callback(Output('graph_container', 'children'),
    [Input('stock_ticker_input', 'value')])
def stock_ticker_dropdown_changed(stock_ticker):
    if stock_ticker not in df['Stock'].unique():
        return html.P('Select valid stock ticker from the dropdown...')
    df_ticker = df[df['Stock'] == stock_ticker]
    return dcc.Graph(
        config=plotly_config,
        figure={
            'data': [go.Scatter(
                x=df_ticker['Date'],
                y=df_ticker['Close'],
            )],
        })

if __name__ == '__main__':
    app.run_server(port=8054)
