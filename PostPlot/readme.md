# Post Plot 

This program is identical in functionality to the Live Plot program, but with some functionality changed (while I troubleshoot issues with live plotting on boards other than the Arduino Uno R3).

## Differences to Live Plot
  - Live plotting removed, only plots data after the session ends (stop key pressed)
  - Baud rate increased from 9600 to 115200 
  - Plot and CSV files contain data for multiple sensors (10 for the current design)

## Program Summary

This Python program is designed to pull sensor data via SPI over a shared COM port with an Arduino board to which the desired sensor is connected.
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
	- `currentTime` is a float value used to track the current time elapsed in seconds for adjusting the x-axis of the plot
	- `xmin` and `ymin` are the minimum values of the x and y axes of the active plot, respectively. Both are initialized to the origin (0). 
	- `ymax` is the limit of the y axis and is initialized to a dummy `3.3` because that is the maximum anticipated for the tests conducted with a 3.3V output from my Arduino Due board. `ymax` will be overwritten towards the end of the program to scale the graph down to whatever the maximum value during the test was, plus a little overhead. Note that the Due does have a 5V output pin, but the internal logic of the Due is 3.3V. Out of an abundance of caution (I don't own the board), I used 3.3V output from the Due so that the max voltage possible to input to the Due's analog pins is 3.3V, should anything go wrong with my circuits.
	- Several empty lists are declared
	- `stopPlot` is a boolean variable initialized to `False` and used to track when the stopkey is pressed in order to tell the program when to stop collecting data and plot what it has collected.
		1. `times` for storing time values for the duration of the test
		2. `voltages0` to `voltages9` for storing voltage values from each of the sensors connected to the Arduino board for the duration of the test.
		
3. Prep the serial communications
	- Interactive plot mode is activated and a figure is initialized with x-axis label *Time (s)* and y-axis label *Voltage (V)*
	- A serial communication port is activated with COM5 at 115200 baud. **Be sure the com port and baud rate for the Arduino board match what is declared for use in the Python program**
	- The serial port is closed immediately before opening it again. An online forum recommended this step to prevent serial data errors just in case the COM port is open for some reason.
	
4. Retrieve data from the Arduino board
	- `currentVoltage0` to `currentVoltage9` are assigned sequential values read from the serial communication line. The values correspond, in order, to each sensor's voltage output.
	- `currentTime` is assigned the final value read from the serial line which corresponds to the current time that has elapsed in the test. The value is rounded to 2 decimal places.
	- The time and voltage values are appended to their respective lists.
	- The keyboard is checked to see if the stop key "q" is pressed. If it is, `stopPlot` is set to `True` and the `while` loop is exited. If it is not, the loop iterates again to get the next group of voltage values.
	
5. Close serial communications and save session data
	- When the stop key is pressed and the `while` loop exits, the communication port is closed and the program starts the process of saving the voltage and time data to a CSV and figure.
	
6. Create a CSV file and save time, voltage data
	- `fileIndex` is initialized to `1`, used to interate the name of successive files if the current file (ex output1) exists in the directory already. `newFileName` is created as `testOutput[FILEINDEX].csv`. If `newFileName`
	matches a file in the current working directory (i.e. the file already exists), `fileIndex` is incremented by 1 and the file is renamed using it. The cycle repeats until `newFileName` does not match an existing file.
	- The new CSV file is opened in `write` mode, and the time and voltage values are written in their own rows (one row each) to it.
	
7. Create and save an image of plot (entire session's data)
	- A new figure is initialized with revised x limits. The x limits are `0,times[-1]` to get all time values for the entire session. The y limits are adjusted using two iterations of the `max` function. Since the voltage values are contained in lists, the first `max` has to be used on one list at a time to pick the highest value contained in that specific list. The max value of each list is stored in `max0` to `max9` for `voltages0` to `voltages9`. A second `max` is used on the group of maximums to find the highest value from the entire test session across all sensors used in the session. The maximum is increased by 10% to allow for a little overhead on the figure that gets plotted, and the new value (called `newMax`) is assigned to `ymax`.
	- Each set of voltages from `voltages0` to `voltages9` is plotted against `times` with its own color and label, and the legend is shifted to the top center, just outside the figure.
	- The same process for checking file names is duplicated after resetting `fileIndex` to `1`. Files are saved as jpeg images with the name `testOutputPlot[FILEINDEX].jpeg`.
