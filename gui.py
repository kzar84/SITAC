# use Tkinter to show a digital clock

from tkinter import *
import time

gui = Tk()
gui.title('SITAC')
gui.minsize(800,600)

# Alarm Strings
currentTime = ''
nextAlarmTime = 'Next alarm: 07:00 am'

# Status Strings
alarmStatusStr = 'Alarm: OFF'
brewStatusStr =  'Brew:  OFF'
lightStatusStr = 'Light: OFF'

# Status Booleans (init all false)
alarmStatus = False
brewStatus =  False
lightStatus = False

# Fucntion that gets the current time every 200ms and updates appropriate label
def tick():
    global currentTime
    # get the current local time from the PC
    nextTime = time.strftime('%H:%M pm')
    # if time string has changed, update it
    if nextTime != currentTime:
        currentTime = nextTime
        clockLabel.config(text=nextTime)

    clockLabel.after(200, tick)

# Callback functions for updating gui status strings
def updateAlarmStatus():
    global alarmStatus, alarmStatusStr

    if (alarmStatus == False):
        alarmStatus = 'Alarm: ON'
    else:
        alarmStatus = 'Alarm: OFF'

    alarmStatus = not alarmStatus
    statusLabel.config(text=alarmStatusStr + '\n' + brewStatusStr + '\n' + lightStatusStr)

def updateBrewStatus(flip):
    global brewStatus, brewStatusStr

    if (brewStatus == False):
        brewStatus =  'Brew:  ON'
    else:
        brewStatus =  'Brew:  OFF'

    brewStatus = not brewStatus    
    statusLabel.config(text=alarmStatusStr + '\n' + brewStatusStr + '\n' + lightStatusStr)

def updateLightStatus():
    global lightStatus, lightStatusStr

    if (lightStatus == False):
        lightStatus = 'Light: ON'
    else:
        lightStatus = 'Light: OFF'

    lightStatus = not lightStatus
    statusLabel.config(text=alarmStatusStr + '\n' + brewStatusStr + '\n' + lightStatusStr)


# Set up various labels for display
clockLabel = Label(gui, font=('times', 30, 'bold'))
clockLabel.pack()

nextAlarmLabel = Label(gui, font=('times', 15, 'bold'), text = nextAlarmTime)
nextAlarmLabel.pack()

statusLabel = Label(gui,font=('times', 15, 'bold'),text=alarmStatusStr + '\n' + brewStatusStr + '\n' + lightStatusStr)
statusLabel.pack()

tick()
gui.mainloop(  )
