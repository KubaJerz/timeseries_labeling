import dash
import json
import pandas as pd
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import plotly
import sys
import os

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

# init dict
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

# init the stack
stack = []

app.layout = html.Div([
    html.Button(id='btn', children=current_option, style={'backgroundColor': button_color, 'color': 'white'}),
    html.Button(id='save_btn', children='save btn', style={'position': 'absolute', 'top': '8px', 'right': '50px'}),
    html.Button(id='undo_btn', children='undo', style={'position': 'absolute', 'top': '8px', 'right': '350px'}),
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
], style={'backgroundColor': backgroundcolor})

@app.callback(
    Output('graph', 'figure', allow_duplicate=True),
    Output('start_time', 'data'),
    Output('end_time', 'data'),
    Input('graph', 'clickData'),
    State('current_option', 'data'),
    State('start_time', 'data'),
    State('end_time', 'data'),
    State('graph', 'figure'),
    prevent_initial_call=True
)
def process_clk(click_data, current_option, start_time, end_time, figure):
    if click_data:
        print('clk')
        x_value = click_data['points'][0]['x']
        if start_time is None:
            option_parts = current_option.split('_')
            side = option_parts[0]
            action = option_parts[1]

            start_time = x_value
            stack.append([side, action])
        else:
            end_time = x_value
            # Update the data dictionary
            option_parts = current_option.split('_')
            side = option_parts[0]
            action = option_parts[1]
            stack.append([side, action])
            data[side][action].append({'start': start_time, 'end': end_time})
            start_time = None
            end_time = None

        # This code adds the vertical line
        fig = go.Figure(figure)  # because figure is a dict we need it as a plotly object
        fig.add_vline(x=x_value, line_width=2, line_dash="dash", line_color="green")
        figure = fig.to_dict()  # convert the updated fig back to a dictionary

    return figure, start_time, end_time

# Removes the vertical line at the given x-value from the provided Plotly figure.
# def remove_vline(fig, x_value):
#     shapes = fig.layout.shapes or []
#     print(len(shapes),' ',x_value)
#     if len(shapes) == 2 and shapes[0].x0 == x_value:
#         print('x_value')
#         # If there is only one shape left and it matches the x_value,
#         # clear the shapes list instead of creating an empty list
#         fig.update_layout(shapes=[])
#     else:
#         updated_shapes = [shape for shape in shapes if shape.x0 != x_value]
#         # print(updated_shapes)
#         fig.update_layout(shapes=updated_shapes)
#     return fig

# def remove_vline(fig, x_value):
#     shapes = fig.layout.shapes or []
#     print("Before removing, shapes length:", len(shapes), "x_value:", x_value)
#     if len(shapes) == 1 and shapes[0].x0 == x_value:
#         print('Removing the only shape')
#         fig.update_layout(shapes=[])
#     else:
#         updated_shapes = [shape for shape in shapes if shape.x0 != x_value]
#         print("Updated shapes length:", len(updated_shapes))
#         fig.update_layout(shapes=updated_shapes)
#     print("After removing, shapes length:", len(fig.layout.shapes))
#     return fig
def remove_vline(fig, x_value):
    shapes = fig.layout.shapes or []
    updated_shapes = [shape for shape in shapes if shape.x0 != x_value]
    if updated_shapes:
        fig.update_layout(shapes=updated_shapes)
    else:
        print('here')
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    return fig

@app.callback(
    Output('start_time', 'data', allow_duplicate=True),
    Output('graph', 'figure', allow_duplicate=True),
    Input('undo_btn', 'n_clicks'),
    State('start_time', 'data'),
    State('graph', 'figure'),
    prevent_initial_call=True
)
def undo_func(n_clicks, start_time, figure):
    if n_clicks:
        print('Undo function triggered')
        if start_time is not None:
            if stack:
                fig = go.Figure(figure)
                fig = remove_vline(fig, start_time)
                start_time = None
                figure = fig.to_dict()
            return start_time, figure
        else:
            if stack:
                element0 = stack.pop()
                element1 = stack.pop()
                vline0_corr = data[element0[0]][element0[1]][-1]['end']
                vline1_corr = data[element1[0]][element1[1]][-1]['start']
                fig = go.Figure(figure)
                fig = remove_vline(fig, vline0_corr)
                fig = remove_vline(fig, vline1_corr)
                del data[element0[0]][element0[1]][-1]
                figure = fig.to_dict()
            return start_time, figure

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
        new_file_path = os.path.join(dir_path, 'labels.json')
        with open(new_file_path, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open('labels.json', 'w') as f:
            json.dump(data, f, indent=2)

@app.callback(
    Input('save_btn', 'n_clicks'),
    prevent_initial_call=True
)
def exit_app(n_clicks):
    if n_clicks:
        write_data_to_file()

if __name__ == '__main__':
    app.run_server(debug=True)




# import dash
# import json
# import pandas as pd
# from dash import html, dcc, Input, Output, State
# import plotly.graph_objects as go
# import plotly.express as px
# import sys
# import os
# '''
#     1.
#     if the file is run as such: python plt_dash_prototype.py
#     it assumes that the accelatrion is in the same dir as the plt_dash_prototype.py fiel is in too

#     2.
#     if it is run as such: python plt_dash_prototype.py ./3_final/07/2024-02-07_11_39_39/acceleration.csv
#     it will show u the graph for the givver acc csv and same the lables in the same dir as the acc cvs 

#     3.
#     if you do python plt_dash_prototype.py ./3_final/07/2024-02-07_11_39_39/acceleration.csv 1
#     it does #3 but will choose theme seaborn; 0 = 'plotly_dark' 1 ='seaborn' 2 = 'plotly'

#     *** 
#         The top left color button will cycle you though adding point to left_water left_listerine ......
#         The top right save btn will save the data to json. TO EXIT you much do "(contorl ^) C " to close

#         note: if you press on the same point it will not "write it down" until you have moved your curesr no matter how many times you press
#     ***



# '''

# app = dash.Dash(__name__)

# themes = ['plotly_dark', 'seaborn', 'plotly']



# if len(sys.argv) == 2:
#     data_filename = sys.argv[1]
#     theme = themes[0]
#     backgroundcolor = 'black'
# elif len(sys.argv) == 3:
#     data_filename = sys.argv[1]
#     theme = themes[int(sys.argv[2])]
#     if sys.argv[2] != 0:
#         backgroundcolor = 'white'
# else:
#     data_filename = 'acceleration.csv'
#     theme = themes[0]
#     backgroundcolor = 'black'




# # Load CSV data
# acc_data = pd.read_csv(data_filename, skiprows=1)
# acc_data['timestamp'] = ((acc_data['timestamp'] - acc_data['timestamp'].iloc[0]) / 1e9)

# # Initial button color and option
# button_color = 'blue'
# options = ['left_water', 'left_listerine', 'right_water', 'right_listerine']
# current_option_index = 0
# current_option = options[current_option_index]
# start_time = None
# end_time = None

# # inti dic
# data = {
#     "left": {
#         "water": [],
#         "listerine": []
#     },
#     "right": {
#         "water": [],
#         "listerine": []
#     }
# }

# #inti the stack

# stack = []

# app.layout = html.Div([
#     html.Button(id='btn', children=current_option, style={'backgroundColor': button_color, 'color': 'white'}),
#     html.Button(id='save_btn', children='save btn', style={'position': 'absolute', 'top': '8px', 'right': '50px'}),
#     html.Button(id='undo_btn', children='undo', style={'position': 'absolute', 'top': '8px', 'right': '350px'}),
#     dcc.Graph(
#         id='graph',
#         figure=px.line(acc_data, x='timestamp', y='x', title=data_filename).update_layout(
#             xaxis_title='Time (s)',
#             yaxis_title='Acceleration (m/s²)'    
#         ).add_trace(go.Scatter(x=acc_data['timestamp'], y=acc_data['y'], mode='lines', name='y'))
#          .add_trace(go.Scatter(x=acc_data['timestamp'], y=acc_data['z'], mode='lines', name='z'))
#          .update_layout(template=theme)
#     ),
#     dcc.Store(id='current_option', data=current_option),
#     dcc.Store(id='current_option_index', data=current_option_index),
#     dcc.Store(id='start_time', data=None),
#     dcc.Store(id='end_time', data=None),
# ], style={'backgroundColor': backgroundcolor})
 
 
# @app.callback(
#     Output('graph', 'figure', allow_duplicate=True),
#     Output('start_time', 'data'),
#     Output('end_time', 'data'),
#     Input('graph', 'clickData'),
#     State('current_option', 'data'),
#     State('start_time', 'data'),
#     State('end_time', 'data'),
#     State('graph', 'figure'),
#     prevent_initial_call=True 
# )
# def process_clk(click_data, current_option, start_time, end_time, figure):
#     if click_data:
#         print('clk')
#         x_value = click_data['points'][0]['x']
#         if start_time is None:
#             option_parts = current_option.split('_')
#             side = option_parts[0]
#             action = option_parts[1]

#             start_time = x_value
#             stack.append([side,action])
#         else:
#             end_time = x_value
#             # Update the data dictionary
#             option_parts = current_option.split('_')
#             side = option_parts[0]
#             action = option_parts[1]
#             stack.append([side,action])
#             data[side][action].append({'start': start_time, 'end': end_time})
#             start_time = None
#             end_time = None

#         #this code adds the vertcal line
#         fig = go.Figure(figure) #because figre is a dic we need it as a plty object
#         fig.add_vline(x=x_value, line_width=2, line_dash="dash", line_color="green")
#         figure = fig.to_dict() # convert the updated fig back to a dictionary
#         #return figure, start_time, end_time, last_clk_time

#     return figure, start_time, end_time

# #Removes the vertical line at the given x-value from the provided Plotly figure.
# def remove_vline(fig, x_value):
#     shapes = fig.layout.shapes or []
#     updated_shapes = [shape for shape in shapes if shape.x0 != x_value]
#     fig.update_layout(shapes=updated_shapes)
#     return fig

# @app.callback(
#     Output('start_time', 'data', allow_duplicate=True),
#     Output('graph', 'figure', allow_duplicate=True),
#     Input('undo_btn','n_clicks'),
#     State('start_time', 'data'),
#     State('graph', 'figure'),
#     prevent_initial_call=True 
# )

# def undo_func(n_clicks, start_time, figure):
#     print('sdfgdfsg')
#     if n_clicks:
#         if start_time != None:
#             fig = go.Figure(figure)
#             fig = remove_vline(fig,start_time)
#             start_time = None
#             figure = fig.to_dict()
#             return start_time, figure
#         else:
#             element0 = stack.pop()
#             element1 = stack.pop()
#             vline0_corr = data[element0[0]][element0[1]][-1]['end']
#             vline1_corr = data[element1[0]][element1[1]][-1]['start']
#             fig = go.Figure(figure)
#             fig = remove_vline(fig,vline0_corr)
#             fig = remove_vline(fig,vline1_corr)
#             del data[element0[0]][element0[1]][-1]
#             start_time = None
#             figure = fig.to_dict()
#             return start_time, figure


# @app.callback(
#     Output('btn', 'children'),
#     Output('btn', 'style'),
#     Output('current_option', 'data'),
#     Output('current_option_index', 'data'),
#     Input('btn', 'n_clicks'),
#     State('current_option_index', 'data')
# )
# def change_button_color(n_clicks, current_option_index):
#     global button_color, current_option
#     if n_clicks:
#         button_color = 'green' if button_color == 'blue' else 'blue'
#         current_option_index = (current_option_index + 1) % len(options)
#         current_option = options[current_option_index]
#     return current_option, {'backgroundColor': button_color, 'color': 'white'}, current_option, current_option_index



# def write_data_to_file():
#     if len(sys.argv) > 1:
#         dir_path = os.path.dirname(sys.argv[1])
#         new_file_path = os.path.join(dir_path,'labels.json')
#         with open(new_file_path, 'w') as f:
#             json.dump(data, f, indent=2)
#     else:
#         with open('labels.json', 'w') as f:
#             json.dump(data, f, indent=2)

# #atexit.register(write_data_to_file)

# @app.callback(
#     Input('save_btn', 'n_clicks'),
#     prevent_initial_call=True
# )
# def exit_app(n_clicks):
#     if n_clicks:
#         write_data_to_file()


# if __name__ == '__main__':
#     app.run_server(debug=True)