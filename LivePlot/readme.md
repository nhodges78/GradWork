# Live Plot

## Program Summary

This Python program is designed to pull real-time sensor data via SPI over a shared COM port with an Arduino board to which the desired sensor is connected.
The Arduino board has its own unique program designed to acquire the desired sensor data and process the data as required for the application.
The data is written to the serial monitor using the COM port through the Arduino program, and the Python program uses the same COM port to retrieve the same data.
The Python program outputs an evolving plot that plots the most recent 5 seconds of data from the Arduino-driven sensor. The plot window actively adjusts every second of time.
When the stop key "q" is pressed on the user's keyboard, plotting stops and the (time,output) data from the entire session is output as a CSV file with the raw data and a jpeg image with a graphical representation of the same data.

## Operational Description

1. Imported libraries
	- `serial` for communicating with the Arduino on COM6 at 9600 baud
	- `matplotlib.pyplot` for plotting and updating real-time figures of plotted data
	- `csv` for writing session data (times and output values) to CSV file
	- `os` for determining the name assigned to the session output files (CSV and jpeg)
	- `keyboard` for monitoring keyboard input for presses of the stop key

2. Initialize variables, special formulas, and lists
	- `timeStep`