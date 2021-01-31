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
	- The `if` block exits and the loop continues at the point where it would have started if the currect window of time is within 5 seconds.