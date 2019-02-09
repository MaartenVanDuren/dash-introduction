import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import os
import pandas as pd


print('PID '+str(os.getpid()))

df = pd.read_csv('stock-ticker.csv')
df = df[df['Stock'] == 'AAPL']

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
    dcc.Graph(
        config=plotly_config,
        figure={
            'data': [go.Scatter(
                x=df['Date'],
                y=df['Close'],
            )],
        })
])

if __name__ == '__main__':
    app.run_server(port=8053)
