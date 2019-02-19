# use Tkinter to show a digital clock

from tkinter import *
import time

# Class that handles clock functionality
class Clock:
    def __init__(self): 
        # Alarm Strings
        self.currentTime = ''
        self.nextTime = ''
        self.nextAlarmTime = '07:00 am'

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

# gui classes used for multiple page gui
class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('SITAC')
        self.minsize(800,600)

        # container contains all the pages
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {} # dictionary containing gui pages

        # create in individual pages and store them in frames
        for F in (ClockPage, SettingsPage):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(ClockPage)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

class ClockPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
        # Set up various labels for display
        self.clockLabel = Label(self, font=('times', 30, 'bold'))
        self.clockLabel.pack()

        self.nextAlarmLabel = Label(self, font=('times', 15, 'bold'), text='Next alarm: ' + clock.nextAlarmTime)
        self.nextAlarmLabel.pack()

        self.statusLabel = Label(self,font=('times', 15, 'bold'),text=clock.alarmStatusStr + '\n' + clock.brewStatusStr + '\n' + clock.lightStatusStr)
        self.statusLabel.pack()

        menuButton = Button(self, text='Settings', command=lambda: controller.show_frame(SettingsPage))
        menuButton.pack()

class SettingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
        # Set up various labels for display
        self.alarmLabel = Label(self, font=('times', 15, 'bold'), text='Alarm: 07:00 am')
        self.alarmLabel.pack()

        self.volumeLabel = Label(self, font=('times', 15, 'bold'), text='Volume: 15')
        self.volumeLabel.pack()

        self.toneLabel = Label(self,font=('times', 15, 'bold'),text='Piano')
        self.toneLabel.pack()

        homeButton = Button(self, text='Home', command=lambda: controller.show_frame(ClockPage))
        homeButton.pack()


# Instantiate a clock and start ticking
# Instantiate a gui and start it up
clock = Clock()
gui = MainWindow()
clock.tick(gui.frames[ClockPage].clockLabel)
gui.mainloop()