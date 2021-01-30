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

times=[] #empty array for saving timestamps
voltage=[] #empty array for saving voltage outputs
tHist=[] #track all time values
vHist=[] #track all voltage values

plt.ion()
fig=plt.figure()
plt.xlabel('Time (s)')
plt.ylabel("Voltage (V)")

port=serial.Serial('COM6',9600)

port.close() #close to prevent errors in measurement
port.open()

#import data from Arduino to plot

while True: #quit when q key is pressed

    if int(currentTime)>timeFrame:
        i=int(1/timeStep) #remove all items from oldest second of time
        tHist.extend(times[0:i])
        del times[0:i]
        vHist.extend(voltage[0:i])
        del voltage[0:i]
        xmin+=1
        xmax+=1
        plt.clf() #refresh figure
        timeFrame+=1 #add another second to the timeframe

    currentVoltage=float(port.readline().decode()) #first line in arduino is voltage
    currentTime=float(port.readline().decode()) #time follows voltage in arduino program
    times.append(round(currentTime,2))
    voltage.append(currentVoltage)
    
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.plot(times,voltage,'m-')

    if key.is_pressed('q'): #stopkey pressed, exit loop
        #time.sleep(0.5)
        plt.clf()
        plt.close()
        break
    else:
        plt.show()
        plt.pause(.001) #update plot in sync with Arduino delay

port.close()

tHist.extend(times)
vHist.extend(voltage)

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
    writer.writerow(tHist)
    writer.writerow(["Voltages"])
    writer.writerow(vHist)

#CREATE, NAME, AND SAVE FIGURE FROM SESSION

plt.figure()
plt.xlim(0,tHist[-1]) #final recorded time value is max
plt.ylim(ymin,ymax)
plt.xlabel('Time (s)')
plt.ylabel("Voltage (V)")
plt.plot(tHist,vHist,'m-')

fileIndex=1
newFileName='testOutputPlot'+str(fileIndex)+'.jpeg'
if os.path.isfile(newFileName)==True: #fileExists, change name via incrementing index
    while os.path.isfile(newFileName)==True:
        fileIndex+=1
        newFileName='testOutputPlot'+str(fileIndex)+'.jpeg'

plt.savefig(newFileName)