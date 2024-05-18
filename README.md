# **Dash Acceleration Data Visualization**

This project is a Dash-based web application for visualizing and interacting with acceleration data. The app provides an interface to plot acceleration data from a CSV file and allows users to annotate specific time intervals on the graph. The annotations can be saved to a JSON file for later analysis.

### ***

## **Features**

- **Data Visualization**: Plots acceleration data in x, y, and z dimensions over time.
- **Theme Selection**: Choose between different themes for the plot (plotly_dark, seaborn, plotly).
- **Annotation**: Add annotations to the graph by clicking on points.
- **Save Annotations**: Save the annotations to a JSON file.

### ***

## **Running the App**

### ***Default Mode***

`python plt_dash_prototype.py`

Run the app with default settings: Assumes the acceleration.csv file is in the same directory and uses the default port (8050).

### ***Custom CSV File***

`python plt_dash_prototype.py ./path/to/acceleration.csv`

Run the app with a specified CSV file: Displays the graph for the specified CSV file and saves labels in the same directory, using the default port (8050).

### ***Custom CSV File with Custom Port or Custom Theme***

`python plt_dash_prototype.py ./path/to/acceleration.csv 8051`

Run the app with a specified CSV file, port(e.g., 8051).

`python plt_dash_prototype.py ./path/to/acceleration.csv 1`

Run the app with a specified CSV file and theme: 0: plotly_dark, 1: seaborn, 2: plotly, using the default port (8050).

### ***Custom CSV File, Port, and Theme***

`python plt_dash_prototype.py ./path/to/acceleration.csv 8051 1`

Run the app with a specified CSV file, port, and theme.

### ***Running Multiple Instances***

`python plt_dash_prototype.py ./0/path/to/acceleration.csv 8051 
python plt_dash_prototype.py ./1/path/to/acceleration.csv 8052 
python plt_dash_prototype.py ./2/path/to/acceleration.csv 8053`

You can run multiple instances of the app on different ports by specifying the port number as a command-line argument.

### ***

## **Interaction with App**

- **Annotation Button**: The top-left button cycles through different annotation options (left_water, left_listerine, right_water, right_listerine).
- **Save Button**: The top-right button saves the annotations to a JSON file.
- **Adding Annotations**: Click on the graph to mark start and end times for annotations. The same point must be clicked again after moving the cursor to record it.

### ***

## **Exiting the App**

Press (Ctrl + C) in the terminal to close the app.
