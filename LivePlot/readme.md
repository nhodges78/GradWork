# Live Plot

*THIS PROGRAM HAS ONLY WORKED ON AN ARDUINO UNO R3 SO FAR*

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
	- `timeStep` is the current time step in seconds. **Be sure to match this with the ms delay value in the Arduino program**. I'm using 100 ms delay, so this is initialized to `0.1`.
	- `testTime` is the window of time to display on the active figure or, if desired, can be used to limit the length of the session by chaning the program's `while` loop to execute for `testTime`'s duration.
	It's initialized to `5` to plot the most recent 5 seconds of time.
	- `currentTime` is a float value used to track the current time in seconds for adjusting the x-axis of the active plot, especially if the active 5-second window is exceeded for plotting. Initialized to `0.0`.
	- `timeFrame` is used for maintaining the time frame dictated by `testTime` and thus is initialized to `testTime`. `testTime` is meant to be a constant, so `timeFrame` is used as an incrementable variable to represent
	the maximum time value of the current time frame displayed on the active plot before the plot needs to be updated with the most recent 5 seconds of time.
	- `maxLength` used to represent the number of time steps in the allowable amount of time and is initialized to the integer equivalent of the quotient `testTime`/`timeStep`.
	- `xmin` and `ymin` are the minimum values of the x and y axes of the active plot, respectively. Both are initialized to the origin (0). 
	- `xmax` and `ymax` are the limits of the x and y axes, respectively. `ymax` is initialized to `5` because that is the maximum anticipated for the tests conducted with a 5V output from my Arduino Uno board.
	`xmax` is initialized to `testTime` for two reasons. The first is that the x-axis represents time, and the second is that the initial time window to be displayed on the active plot is from 0 seconds to `testTime` seconds.
	- Four empty lists are declared
		1. `times` for storing active-window time values for the most recent 5 seconds of time
		2. `voltage` for storing active-window output voltage values from the sensor connected to the Arduino board for the most recent 5 seconds of time
		3. `tHist` for storing all time values from the entire session
		4. `vHist` for storing all output voltage values from the entire session
		
3. Prep the active plot and serial communications
	- Interactive plot mode is activated and a figure is initialized with x-axis label *Time (s)* and y-axis label *Voltage (V)*
	- A serial communication port is activated with COM6 at 9600 baud. **Be sure the com port for the Arduino board matches what is declared for use in the Python program**
	- The serial port is closed immediately before opening it again. An online forum recomended this step to prevent serial data errors just in case the COM port is open for some reason.
	
4. Retrieve data from the Arduino board to plot on screen
	- Data is retrieved in a continuous `while` loop. As mentioned before, the loop can be changed to match `testTime` conditions so that the session runs for a set amount of time, but the default is `while True` that runs
	until the stop key "q" is pressed on the user's keyboard
	- The loop begins with an `if` statement to check if the current time value (passed with the current voltage value from the Arduino via SPI) has exceeded the current `timeFrame`. If it has, the figure needs to be updated
	so that it displays the most recent 5-second window of time. To update the window, the `if` block determines how many time values are in the oldest second of time and removes that number of values from `times` and `voltage` while
	storing those values to `tHist` and `vHist`. `xmin` and `xmax` are incremented for the active plot, `timeFrame` is incremented by 1, and the active plot is cleared so that the oldest second of time is removed from it.
	The `if` block exits and the loop continues at the point where it would have started if the currect window of time is within `testTime` seconds.
	- After the `if` adjustments, the current voltage and time values are read from the Arduino through the serial connection, decoded, and assigned to `currentVoltage` and `currentTime` variables that are appended to the `voltage` and `times` lists.
	`currentTime` is rounded before doing do.
	- The x- and y-axis limits are assigned (in case x changed during the `if` block or y was initialized to another value) and a plot is drawn using the values in `times` for the x-axis and `voltage` for the y-axis.
	- The keyboard is checked to see if the stop key "q" is pressed. If it is, the figure is cleared, the active plot is closed, and the `while` loop is exited. If it is not, the updated plot is shown and paused briefly to allow updating in
	the next iteration of the loop. **If the plot is paused for a significant amount of time, the stop key sequence will not work as it will interrupt the plotting process while the plot is paused**. I chose 1 ms pause time.
	
5. Close serial communications and save session data
	- When the stop key is pressed and the `while` loop exits, the communication port is closed and the values of `times` and `voltage` are appended to the end of `tHist` and `vHist`, respectively.
	
6. Create a CSV file and save time, voltage data
	- `fileIndex` is initialized to `1`, used to interate the name of successive files if the current file (ex output1) exists in the directory already. `newFileName` is created as `testOutput[FILEINDEX].csv`. If `newFileName`
	matches a file in the current working directory (i.e. the file already exists), `fileIndex` is incremented by 1 and the file is renamed using it. The cycle repeats until `newFileName` does not match an existing file.
	- The new CSV file is opened in `write` mode, and `tHist` and `vHist` are written in their own rows (one row each) to it.
	
7. Create and save an image of plot (entire session's data)
	- A new figure is initialized with revised x limits. The x limits are `0,tHist[-1]` to get all time values for the entire session. The y limits and axis labels are unchanged.
	- `tHist` and `vHist` (contain data for the entire session) are used to create a plot
	- The same process for checking file names is duplicated after resetting `fileIndex` to `1`. Files are saved as jpeg images with the name `testOutputPlot[FILEINDEX].jpeg`.
