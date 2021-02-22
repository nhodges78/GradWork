import serial
import matplotlib.pyplot as plt
import csv
import os
import keyboard as key

timeStep=0.1 #match arduino delay ms
testTime=5 #how many seconds to run the experiment
currentTime=0.0 #for x axis
timeFrame=testTime #for adjusting time window on plot
maxLength=int(testTime/timeStep) #max to keep only 5 seconds of time visible on plot
xmin=0 #limiting x axis
xmax=testTime
ymin=0
ymax=5
stopPlot=False

times=[] #empty array for saving timestamps
voltagesR=[] #empty array for saving voltages outputs
voltagesL=[]

plt.ion()
fig=plt.figure()
plt.xlabel('Time (s)')
plt.ylabel("Voltage (V)")

port=serial.Serial('COM5',9600) #change to match your system
port.close() #close to prevent errors in measurement
port.open()

#import data from Arduino to plot

while (stopPlot==False): #quit when q key is pressed

    currentVoltageR=float(port.readline().decode()) #first line in arduino is voltage
    currentVoltageL=float(port.readline().decode())
    currentTime=float(port.readline().decode()) #time follows voltage in arduino program
    times.append(round(currentTime,2))
    voltagesR.append(currentVoltageR)
    voltagesL.append(currentVoltageL)

    if key.is_pressed('q'): #stopkey pressed, exit loop
        stopPlot=True

port.close()

#NAME AND SAVE THE CSV FILE

fileIndex=1
newFileName='testOutput'+str(fileIndex)+'.csv'
if os.path.isfile(newFileName)==True: #fileExists, change name via incrementing index
    while os.path.isfile(newFileName)==True:
        fileIndex+=1
        newFileName='testOutput'+str(fileIndex)+'.csv'

with open(newFileName,'w') as newFile:
    writer=csv.writer(newFile,quoting=csv.QUOTE_NONE)
    writer.writerow(["Times"])
    writer.writerow(times)
    writer.writerow(["R Voltages"])
    writer.writerow(voltagesR)
    writer.writerow(["L Voltages"])
    writer.writerow(voltagesL)

#CREATE, NAME, AND SAVE FIGURE FROM SESSION

plt.figure()
plt.xlim(0,times[-1]) #final recorded time value is max
plt.ylim(ymin,ymax)
plt.xlabel('Time (s)')
plt.ylabel("Voltage (V)")
plt.plot(times,voltagesR,'m-', label='Photoresistor R')
plt.plot(times,voltagesL,'b-', label='Photoresistor L')
plt.legend()

fileIndex=1
newFileName='testOutputPlot'+str(fileIndex)+'.jpeg'
if os.path.isfile(newFileName)==True: #fileExists, change name via incrementing index
    while os.path.isfile(newFileName)==True:
        fileIndex+=1
        newFileName='testOutputPlot'+str(fileIndex)+'.jpeg'

plt.savefig(newFileName)