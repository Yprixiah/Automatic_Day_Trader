import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import model as m


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Market Simulator", style={'text-align': 'center'}),

    html.Button('Run', id='Run', t=300),

    dcc.Graph(id='market simulator', figure={})

])

@app.callback(
    Output("market simulator", "figure"),
    [Input('Run', '')])

def update_graph (t):
    data = m.generate_dataset(t)
    df = data.copy()

    fig = px.line(df['CP'], x='CP', y='Round')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)