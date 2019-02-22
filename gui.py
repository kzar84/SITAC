# use Tkinter to show a digital clock

from tkinter import *
import time
import subprocess

# Class that handles clock functionality
class Clock:
    def __init__(self): 
        # Alarm Strings
        self.current_time = ''
        self.next_time = ''
        self.next_alarm_time = '7:00 am'

        # Status Strings
        self.alarm_status_str = 'Alarm: OFF'
        self.brew_status_str =  'Brew:  OFF'
        self.lights_status_str = 'Light: OFF'

        # Status Booleans
        self.alarm_status = True
        self.alarm_on = False
        self.brew_status =  False
        self.lights_status = False

        # Alarm_tone
        self.alarmTone = 'Loud_Alarm_Clock_Buzzer.wav'

    # Fucntion that gets the current time every 200ms and updates appropriate label
    def tick(self, clockLabel):
        # get the current local time from the PC
        self.next_time = time.strftime('%#I:%M %p') # %#I use if for windows, change to %-I when running on linux
        # if time string has changed, update it
        if self.next_time != self.current_time:
            self.current_time = self.next_time
            clockLabel.config(text=self.next_time)
        
        # check to see if an alarm is ready (add better logic here)
        if (self.alarm_status and self.current_time == self.next_alarm_time):
            self.alarm()
        
        # recall function after 200 miliseconds
        clockLabel.after(200, self.tick, clockLabel)

    # Callback functions for updating gui status strings
    def update_alarm_status(self, statusLabel):
        if (self.alarm_status):
            self.alarm_status_str = 'Alarm: OFF'
        else:
            self.alarm_status_str = 'Alarm: ON'

        self.alarm_status = not self.alarm_status
        statusLabel.config(text=self.alarm_status_str + '\n' + self.brew_status_str + '\n' + self.lights_status_str)

    def update_brew_status(self, statusLabel):
        if (self.brew_status):
            self.brew_status_str =  'Brew:  OFF'
        else:
            self.brew_status_str =  'Brew:  ON'

        self.brew_status = not self.brew_status    
        statusLabel.config(text=self.alarm_status_str + '\n' + self.brew_status_str + '\n' + self.lights_status_str)

    def update_lights_status(self, statusLabel):
        if (self.lights_status):
            self.lights_status_str = 'Light: OFF'
        else:
            self.lights_status_str = 'Light: ON'

        self.lights_status = not self.lights_status
        statusLabel.config(text=self.alarm_status_str + '\n' + self.brew_status_str + '\n' + self.lights_status_str)

    # Sounds the alarm
    def alarm(self):
        # bash command that opens and plays the current alarm tone
        subprocess.Popen('oxmplayer alarm_tones/' + self.alarmTone)
        print('Alarm')
    
    # Toggles coffee brewing
    def brew(self):
        print('starts brewing')

    # Toggles lights
    def lights(self):
        print('turning on the lights')

# Controller class for gui
class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('SITAC')
        self.minsize(800,480)

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

# gui homepage
class ClockPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
        # Set up various labels for display
        self.clockLabel = Label(self, font=('times', 30, 'bold'))
        self.clockLabel.pack()

        self.nextAlarmLabel = Label(self, font=('times', 15, 'bold'), text='Next alarm: ' + clock.next_alarm_time)
        self.nextAlarmLabel.pack()

        self.statusLabel = Label(self,font=('times', 15, 'bold'),text=clock.alarm_status_str + '\n' + clock.brew_status_str + '\n' + clock.lights_status_str)
        self.statusLabel.pack()

        menuButton = Button(self, text='Settings', command=lambda: controller.show_frame(SettingsPage))
        menuButton.pack()

# settings page of the gui
class SettingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
        # Set up various labels for display
        self.alarmLabel = Label(self, font=('times', 15, 'bold'), text='Alarm: 7:00 am')
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