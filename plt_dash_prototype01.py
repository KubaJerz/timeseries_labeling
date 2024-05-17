import dash
import json
import pandas as pd
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
import time
from threading import Timer
'''
    1.
    if the file is run as such: python plt_dash_prototype.py
    it assumes that the accelatrion is in the same dir as the plt_dash_prototype.py fiel is in too

    2.
    if it is run as such: python plt_dash_prototype.py ./3_final/07/2024-02-07_11_39_39/acceleration.csv
    it will show u the graph for the givver acc csv and same the lables in the same dir as the acc cvs 

    3.
    if you do python plt_dash_prototype.py ./3_final/07/2024-02-07_11_39_39/acceleration.csv 1
    it does #3 but will choose theme seaborn; 0 = 'plotly_dark' 1 ='seaborn' 2 = 'plotly'

    *** 
        The top left color button will cycle you though adding point to left_water left_listerine ......
        The top right save btn will save the data to json. TO EXIT you much do "(contorl ^) C " to close

        note: if you press on the same point it will not "write it down" until you have moved your curesr no matter how many times you press
    ***



'''

app = dash.Dash(__name__)

themes = ['plotly_dark', 'seaborn', 'plotly']



if len(sys.argv) == 2:
    data_filename = sys.argv[1]
    theme = themes[0]
    backgroundcolor = 'black'
elif len(sys.argv) == 3:
    data_filename = sys.argv[1]
    theme = themes[int(sys.argv[2])]
    if sys.argv[2] != 0:
        backgroundcolor = 'white'
else:
    data_filename = 'acceleration.csv'
    theme = themes[0]
    backgroundcolor = 'black'




# Load CSV data
acc_data = pd.read_csv(data_filename, skiprows=1)
acc_data['timestamp'] = ((acc_data['timestamp'] - acc_data['timestamp'].iloc[0]) / 1e9)

# Initial button color and option
button_color = 'blue'
options = ['left_water', 'left_listerine', 'right_water', 'right_listerine']
current_option_index = 0
current_option = options[current_option_index]
start_time = None
end_time = None
last_clk_time = time.time()

# Initialize the data dictionary
data = {
    "left": {
        "water": [],
        "listerine": []
    },
    "right": {
        "water": [],
        "listerine": []
    }
}

app.layout = html.Div([
    html.Button(id='btn', children=current_option, style={'backgroundColor': button_color, 'color': 'white'}),
    html.Button(id='save_btn', children='save btn', style={'position': 'absolute', 'top': '8px', 'right': '50px'}),
    dcc.Graph(
        id='graph',
        figure=px.line(acc_data, x='timestamp', y='x', title=data_filename).update_layout(
            xaxis_title='Time (s)',
            yaxis_title='Acceleration (m/s²)'    
        ).add_trace(go.Scatter(x=acc_data['timestamp'], y=acc_data['y'], mode='lines', name='y'))
         .add_trace(go.Scatter(x=acc_data['timestamp'], y=acc_data['z'], mode='lines', name='z'))
         .update_layout(template=theme)
    ),
    dcc.Store(id='current_option', data=current_option),
    dcc.Store(id='current_option_index', data=current_option_index),
    dcc.Store(id='start_time', data=None),
    dcc.Store(id='end_time', data=None),
    dcc.Store(id='last_clk_time', data=last_clk_time),
], style={'backgroundColor': backgroundcolor})


# # Initialize the timer and last_click_time attributes
# on_click.timer = None
# on_click.last_click_time = 0
# on_click.single_click_processed = False

# @app.callback(
#     Output('graph', 'figure'),
#     Output('start_time', 'data'),
#     Output('end_time', 'data'),
#     Input('graph', 'clickData'),
#     State('current_option', 'data'),
#     State('start_time', 'data'),
#     State('end_time', 'data'),
#     State('graph', 'figure'),
#     prevent_initial_call=True
# )
# def on_click(click_data, current_option, start_time, end_time, figure):
#     def process_click(click_data, start_time, end_time):
#         on_click.single_click_processed = True
#         current_time = time.time()
#         on_click.last_click_time = current_time

#         x_value = click_data['points'][0]['x']
#         if start_time is None:
#             start_time = x_value
#         else:
#             end_time = x_value
#             # Update the data dictionary
#             option_parts = current_option.split('_')
#             side = option_parts[0]
#             drink = option_parts[1]
#             data[side][drink].append({'start': start_time, 'end': end_time})
#             start_time = None
#             end_time = None

#         # Create a Plotly Figure object from the figure dictionary
#         fig = go.Figure(figure)

#         # Add the vertical line to the figure
#         vline = go.layout.Shape(
#             type="line",
#             x0=x_value,
#             y0=0,
#             x1=x_value,
#             y1=1,
#             line=dict(
#                 color="Red",
#                 width=2,
#                 dash="dash",
#             )
#         )
#         fig.update_layout(shapes=[vline])

#         # Convert the updated figure back to a dictionary
#         figure = fig.to_dict()

#         return figure, start_time, end_time

#     if click_data:
#         current_time = time.time()
#         if (current_time - on_click.last_click_time) < 0.25:  # Double-click threshold (250ms)
#             if on_click.timer:
#                 on_click.timer.cancel()
#             on_click.single_click_processed = False
#             return figure, start_time, end_time
        
#         on_click.single_click_processed = False
#         on_click.timer = Timer(0.25, process_click, args=[click_data, start_time, end_time])
#         on_click.timer.start()

#     return figure, start_time, end_time








# @app.callback(
#     Output('graph', 'figure'),
#     Output('start_time', 'data'),
#     Output('end_time', 'data'),
#     Input('graph', 'clickData'),
#     State('current_option', 'data'),
#     State('start_time', 'data'),
#     State('end_time', 'data'),
#     State('graph', 'figure'),
#     prevent_initial_call=True
# )
# def on_click(click_data, current_option, start_time, end_time, figure):
#     def process_click(click_data, start_time, end_time, figure):
#         current_time = time.time()
#         if (current_time - on_click.last_click_time) < 0.25:  # Double-click threshold (250ms)
#             return figure, start_time, end_time

#         on_click.last_click_time = current_time

#         x_value = click_data['points'][0]['x']
#         if start_time is None:
#             start_time = x_value
#         else:
#             end_time = x_value
#             # Update the data dictionary
#             option_parts = current_option.split('_')
#             side = option_parts[0]
#             drink = option_parts[1]
#             data[side][drink].append({'start': start_time, 'end': end_time})
#             start_time = None
#             end_time = None

#         # Create a Plotly Figure object from the figure dictionary
#         fig = go.Figure(figure)

#         # Add the vertical line to the figure
#         vline = go.layout.Shape(
#             type="line",
#             x0=x_value,
#             y0=0,
#             x1=x_value,
#             y1=100,
#             line=dict(
#                 color="Red",
#                 width=2,
#                 dash="dash",
#             )
#         )
#         fig.update_layout(shapes=[vline])

#         # Convert the updated figure back to a dictionary
#         figure = fig.to_dict()

#         return figure, start_time, end_time

#     if click_data:
#         on_click.timer = Timer(0.1, process_click, args=[click_data, start_time, end_time, figure])
#         on_click.timer.start()

#     return figure, start_time, end_time

# # Initialize the timer and last_click_time attributes
# on_click.timer = None
# on_click.last_click_time = 0


# @app.callback(
#     Output('graph', 'figure'),
#     Output('start_time', 'data'),
#     Output('end_time', 'data'),
#     Input('graph', 'clickData'),
#     State('current_option', 'data'),
#     State('start_time', 'data'),
#     State('end_time', 'data'),
#     State('graph', 'figure'),
#     prevent_initial_call=True
# )
# def on_click(click_data, current_option, start_time, end_time, figure):
#     if click_data:

#         #TODO EXPLAIN THIS CODE seg
#         if click_data.get('points', [])[0].get('curveNumber', -1) == -1:
#             # If it's a doubleClick (zooming out), return without making any changes
#             print('doubel click')
#             return figure, start_time, end_time
        
    
#     process_clk()

#         # current_time = time.time()  # Get the current time in seconds
#         # print(current_time)
#         # print(last_clk_time)

#         # # was prev click was within the last 5 milliseconds
#         # print(current_time - last_clk_time)
#         # if (current_time - last_clk_time) < 3:
#         #     last_clk_time = current_time
#         #     return figure, start_time, end_time, last_clk_time

#         # last_clk_time = time.time()  # Update the previous click time


#         # x_value_clk = click_data['points'][0]['x'] #click data
#         # x_value_hov = hover_data['points'][0]['x'] #hover data 

#         # if x_value_clk != x_value_hov:
#         #     print(f'hover: {x_value_hov} clk: {x_value_clk}')
#         #     return figure, start_time, end_time
        
#         # x_value = x_value_clk
#         # if start_time is None:
#         #     start_time = x_value

        
 
@app.callback(
    Output('graph', 'figure'),
    Output('start_time', 'data'),
    Output('end_time', 'data'),
    Output('last_clk_time', 'data'),
    Input('graph', 'clickData'),
    State('current_option', 'data'),
    State('start_time', 'data'),
    State('end_time', 'data'),
    State('graph', 'figure'),
    State('last_clk_time', 'data'),
    prevent_initial_call=True
        
)
def process_clk(click_data, current_option, start_time, end_time, figure, last_clk_time):
    x_value = click_data['points'][0]['x']
    if start_time is None:
        start_time = x_value
    else:
        end_time = x_value
        # Update the data dictionary
        option_parts = current_option.split('_')
        side = option_parts[0]
        drink = option_parts[1]
        data[side][drink].append({'start': start_time, 'end': end_time})
        start_time = None
        end_time = None

    #this code adds the vertcal line
    fig = go.Figure(figure) #because figre is a dic we need it as a plty object
    fig.add_vline(x=x_value, line_width=2, line_dash="dash", line_color="green")
    figure = fig.to_dict() # convert the updated fig back to a dictionary

    return figure, start_time, end_time, last_clk_time


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
        button_color = 'green' if button_color == 'blue' else 'blue'
        current_option_index = (current_option_index + 1) % len(options)
        current_option = options[current_option_index]
    return current_option, {'backgroundColor': button_color, 'color': 'white'}, current_option, current_option_index



def write_data_to_file():
    if len(sys.argv) > 1:
        dir_path = os.path.dirname(sys.argv[1])
        new_file_path = os.path.join(dir_path,'labels.json')
        with open(new_file_path, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open('labels.json', 'w') as f:
            json.dump(data, f, indent=2)

#atexit.register(write_data_to_file)

@app.callback(
    Input('save_btn', 'n_clicks'),
    prevent_initial_call=True
)
def exit_app(n_clicks):
    if n_clicks:
        write_data_to_file()


if __name__ == '__main__':
    app.run_server(debug=True)