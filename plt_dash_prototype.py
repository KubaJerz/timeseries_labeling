import dash
import json
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

# Initial button color and option
button_color = 'green'
options = ['left_water', 'left_listerine', 'right_water', 'right_listerine']
current_option_index = 0
current_option = options[current_option_index]
start_time = None
end_time = None

app.layout = html.Div([
    html.Button(id='btn', children=current_option, style={'backgroundColor': button_color, 'color': 'white'}),
    dcc.Graph(
        id='graph',
        figure=go.Figure(
            data=go.Scatter(
                x=np.random.randint(0, 255, 300),
                y=np.random.randint(0, 255, 300),
                mode='markers'
            ),
            layout={
                'xaxis': {'showspikes': True},
                'yaxis': {'showspikes': True},
                'width': 700,
                'height': 500
            }
        ),
        clear_on_unhover=True
    ),
    dcc.Store(id='current_option', data=current_option),
    dcc.Store(id='current_option_index', data=current_option_index),
    dcc.Store(id='start_time', data=None),
    dcc.Store(id='end_time', data=None),
])

@app.callback(
    Output('graph', 'figure'),
    Output('start_time', 'data'),
    Input('graph', 'clickData'),
    State('current_option', 'data'),
    State('start_time', 'data'),
    State('end_time', 'data'),
    prevent_initial_call=True
)
def update_json(click_data, current_option, start_time, end_time):
    if click_data:
        x_value = click_data['points'][0]['x']
        print(start_time,' ',end_time)
        if start_time is None:
            start_time = x_value
            print(start_time)
        else:
            end_time = x_value
            # Save the data to the JSON file
            data = {'start': start_time, 'end': end_time}
            with open('clicked_coordinates.json', 'a') as f:
                json.dump(data, f)
                f.write('\n')
            start_time = None
            end_time = None
    return dash.no_update, start_time

@app.callback(
    Output('btn', 'children'),
    Output('btn', 'style'),
    Output('current_option', 'data'),
    Output('current_option_index', 'data'),
    Input('btn', 'n_clicks'),
    State('current_option_index', 'data')
)
def change_button_color(n_clicks, current_option_index):
    global button_color, current_option
    if n_clicks:
        button_color = 'red' if button_color == 'green' else 'green'
        current_option_index = (current_option_index + 1) % len(options)
        current_option = options[current_option_index]
    return current_option, {'backgroundColor': button_color, 'color': 'white'}, current_option, current_option_index

if __name__ == '__main__':
    app.run_server(debug=True)
