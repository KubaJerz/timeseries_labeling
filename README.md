This project is a Dash-based web application for visualizing and interacting with acceleration data. The app provides an interface to plot acceleration data from a CSV file and allows users to annotate specific time intervals on the graph. The annotations can be saved to a JSON file for later analysis.

Features
  Data Visualization: Plots acceleration data in x, y, and z dimensions over time.
  Theme Selection: Choose between different themes for the plot (plotly_dark, seaborn, plotly).
  Annotation: Add annotations to the graph by clicking on points.
  Save Annotations: Save the annotations to a JSON file.


Running the App
  Default Mode: Run the app with default settings: Assumes the acceleration.csv file is in the same directory.

    python plt_dash_prototype.py

  Custom CSV File: Run the app with a specified CSV file: Displays the graph for the specified CSV file and saves labels in the same directory.

    python plt_dash_prototype.py ./path/to/acceleration.csv


  Custom CSV File with Theme: Run the app with a specified CSV file and theme: 0: plotly_dark, 1: seaborn, 2: plotly

    python plt_dash_prototype.py ./path/to/acceleration.csv 1


Interaction with App

  Annotation Button: The top-left button cycles through different annotation options (left_water, left_listerine, right_water, right_listerine).
  Save Button: The top-right button saves the annotations to a JSON file.
  Adding Annotations: Click on the graph to mark start and end times for annotations. The same point must be clicked again after moving the cursor to record it.


Exiting the App
  Press (Ctrl + C) in the terminal to close the app.
