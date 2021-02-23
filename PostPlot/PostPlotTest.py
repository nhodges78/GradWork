import serial
import matplotlib.pyplot as plt
import csv
import os
import keyboard as key

currentTime=0.0 #for x axis
xmin=0 #limiting x axis
ymin=0
ymax=3.3 #default max
stopPlot=False

times=[] #empty array for saving timestamps
voltages0, voltages1, voltages2, voltages3, voltages4 = [], [], [], [], [] #empty arrays for saving voltages outputs
voltages5, voltages6, voltages7, voltages8, voltages9 = [], [], [], [], []

plt.ion()
fig=plt.figure()
plt.xlabel('Time (s)')
plt.ylabel("Voltage (V)")

port=serial.Serial('COM5',115200) #change to match your system
port.close() #close to prevent errors in measurement
port.open()

#import data from Arduino to plot

while (stopPlot==False): #quit when q key is pressed

    currentVoltage0=float(port.readline().decode()) #first line in arduino is voltage
    currentVoltage1=float(port.readline().decode())
    currentVoltage2=float(port.readline().decode())
    currentVoltage3=float(port.readline().decode())
    currentVoltage4=float(port.readline().decode())
    currentVoltage5=float(port.readline().decode())
    currentVoltage6=float(port.readline().decode())
    currentVoltage7=float(port.readline().decode())
    currentVoltage8=float(port.readline().decode())
    currentVoltage9=float(port.readline().decode())
    currentTime=float(port.readline().decode()) #time follows voltages in arduino program
    times.append(round(currentTime,2))
    voltages0.append(currentVoltage0)
    voltages1.append(currentVoltage1)
    voltages2.append(currentVoltage2)
    voltages3.append(currentVoltage3)
    voltages4.append(currentVoltage4)
    voltages5.append(currentVoltage5)
    voltages6.append(currentVoltage6)
    voltages7.append(currentVoltage7)
    voltages8.append(currentVoltage8)
    voltages9.append(currentVoltage9)

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
    writer.writerow(["FSR0 Voltages"])
    writer.writerow(voltages0)
    writer.writerow(["FSR1 Voltages"])
    writer.writerow(voltages1)
    writer.writerow(["FSR2 Voltages"])
    writer.writerow(voltages2)
    writer.writerow(["FSR3 Voltages"])
    writer.writerow(voltages3)
    writer.writerow(["FSR4 Voltages"])
    writer.writerow(voltages4)
    writer.writerow(["FSR5 Voltages"])
    writer.writerow(voltages5)
    writer.writerow(["FSR6 Voltages"])
    writer.writerow(voltages6)
    writer.writerow(["FSR7 Voltages"])
    writer.writerow(voltages7)
    writer.writerow(["FSR8 Voltages"])
    writer.writerow(voltages8)
    writer.writerow(["FSR9 Voltages"])
    writer.writerow(voltages9)

#CREATE, NAME, AND SAVE FIGURE FROM SESSION

plt.figure()
plt.xlim(0,times[-1]) #final recorded time value is max
max0,max1=max(voltages0),max(voltages1)
max2,max3=max(voltages2),max(voltages3)
max4,max5=max(voltages4),max(voltages5)
max6,max7=max(voltages6),max(voltages7)
max8,max9=max(voltages8),max(voltages9)
newMax=max(max0,max1,max2,max3,max4,max5,max6,max7,max8,max9)
if(newMax!=ymax): #adjust vertical axis scale to fit the graph better
    ymax=newMax*1.1 #small amount of overhead for graph
plt.ylim(ymin,ymax)
plt.xlabel('Time (s)')
plt.ylabel("Voltage (V)")
plt.plot(times,voltages0, color='red',linestyle='solid', label='FSR0')
plt.plot(times,voltages1, color='pink',linestyle='solid', label='FSR1')
plt.plot(times,voltages2, color='orange',linestyle='solid', label='FSR2')
plt.plot(times,voltages3, color='yellow',linestyle='solid', label='FSR3')
plt.plot(times,voltages4, color='green',linestyle='solid', label='FSR4')
plt.plot(times,voltages5, color='lime',linestyle='solid', label='FSR5')
plt.plot(times,voltages6, color='blue',linestyle='solid', label='FSR6')
plt.plot(times,voltages7, color='cyan',linestyle='solid', label='FSR7')
plt.plot(times,voltages8, color='black',linestyle='solid', label='FSR8')
plt.plot(times,voltages9, color='purple',linestyle='solid', label='FSR9')
plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5,1.15))

fileIndex=1
newFileName='testOutputPlot'+str(fileIndex)+'.jpeg'
if os.path.isfile(newFileName)==True: #fileExists, change name via incrementing index
    while os.path.isfile(newFileName)==True:
        fileIndex+=1
        newFileName='testOutputPlot'+str(fileIndex)+'.jpeg'

plt.savefig(newFileName)