# use Tkinter to show a digital clock

from tkinter import *
import time

# Class that handles clock functionality
class Clock:
    def __init__(self): 
        # Alarm Strings
        self.currentTime = ''
        self.nextTime = ''
        self.nextAlarmTime = '22:56 pm'

        # Status Strings
        self.alarmStatusStr = 'Alarm: OFF'
        self.brewStatusStr =  'Brew:  OFF'
        self.lightStatusStr = 'Light: OFF'

        # Status Booleans (init all false)
        self.alarmStatus = True
        self.brewStatus =  False
        self.lightStatus = False

    # Fucntion that gets the current time every 200ms and updates appropriate label
    def tick(self, clockLabel):
        # global currentTime
        # get the current local time from the PC
        self.nextTime = time.strftime('%H:%M pm')
        # if time string has changed, update it
        if self.nextTime != self.currentTime:
            self.currentTime = self.nextTime
            clockLabel.config(text=self.nextTime)
        
        # check to see if an alarm is ready
        if (self.alarmStatus and self.currentTime == self.nextAlarmTime):
            self.alarm(clockLabel)

        clockLabel.after(200, self.tick, clockLabel)

    # Function that gets called when the alarm sounds
    def alarm(self, clockLabel):
        #sound the alarm
        clockLabel.config(text = 'ALARM')

    # Callback functions for updating gui status strings
    def updateAlarmStatus(self, statusLabel):
        if (self.alarmStatus == False):
            self.alarmStatusStr = 'Alarm: ON'
        else:
            self.alarmStatusStr = 'Alarm: OFF'

        self.alarmStatus = not self.alarmStatus
        statusLabel.config(text=self.alarmStatusStr + '\n' + self.brewStatusStr + '\n' + self.lightStatusStr)

    def updateBrewStatus(self, statusLabel):
        if (self.brewStatus == False):
            self.brewStatusStr =  'Brew:  ON'
        else:
            self.brewStatusStr =  'Brew:  OFF'

        self.brewStatus = not self.brewStatus    
        statusLabel.config(text=self.alarmStatusStr + '\n' + self.brewStatusStr + '\n' + self.lightStatusStr)

    def updateLightStatus(self, statusLabel):
        if (self.lightStatus == False):
            self.lightStatusStr = 'Light: ON'
        else:
            self.lightStatusStr = 'Light: OFF'

        self.lightStatus = not self.lightStatus
        statusLabel.config(text=self.alarmStatusStr + '\n' + self.brewStatusStr + '\n' + self.lightStatusStr)


# Instantiate a clock
clock = Clock()

# Set up the gui
gui = Tk()
gui.title('SITAC')
gui.minsize(800,600)

# Set up various labels for display
clockLabel = Label(gui, font=('times', 30, 'bold'))
clockLabel.pack()

nextAlarmLabel = Label(gui, font=('times', 15, 'bold'), text = 'Next alarm: ' + clock.nextAlarmTime)
nextAlarmLabel.pack()

statusLabel = Label(gui,font=('times', 15, 'bold'),text=clock.alarmStatusStr + '\n' + clock.brewStatusStr + '\n' + clock.lightStatusStr)
statusLabel.pack()


clock.tick(clockLabel)
gui.mainloop()