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
        self.next_alarm_time = '7:00 PM'

        # Status Strings
        self.alarm_set_str =  'Alarm: OFF'
        self.brew_set_str =   'Brew:  OFF'
        self.lights_set_str = 'Light: OFF'

        # Status Booleans
        self.alarm_set =  True
        self.alarm_on =      False
        self.brew_set =   False
        self.lights_set = False

        # Alarm_tone list and current indext
        self.alarm_tones = ['buzzer.wav']
        self.alarm_tone = 0

        # Volume (0-50)
        self.volume = 25

    # Fucntion that gets the current time every 200ms and updates appropriate label
    def tick(self, clockLabel):
        # get the current local time from the PC
        self.next_time = time.strftime('%#I:%M %p') # %#I use if for windows, change to %-I when running on linux
        # if time string has changed, update it
        if self.next_time != self.current_time:
            self.current_time = self.next_time
            clockLabel.config(text=self.next_time)
        
        # check to see if an alarm is ready (add better logic here)
        if (self.current_time == self.next_alarm_time and self.alarm_set and not self.alarm):
            self.alarm_on = True  
            self.alarm()
        
        # recall function after 200 miliseconds
        clockLabel.after(200, self.tick, clockLabel)

    # Callback functions for updating gui status strings
    def update_alarm_set(self, statusLabel):
        if (self.alarm_set):
            self.alarm_set_str = 'Alarm: OFF'
        else:
            self.alarm_set_str = 'Alarm: ON'

        self.alarm_set= not self.alarm_set
        statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    def update_brew_set(self, statusLabel):
        if (self.brew_set):
            self.brew_set_str =  'Brew:  OFF'
        else:
            self.brew_set_str =  'Brew:  ON'

        self.brew_set = not self.brew_set    
        statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    def update_lights_set(self, statusLabel):
        if (self.lights_set): 
            self.lights_set_str = 'Light: OFF'
        else:
            self.lights_set_str = 'Light: ON'

        self.lights_set = not self.lights_set
        statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    # Sounds the alarm
    def alarm(self):
        # subprocess.call(bash command, shell=True)
        subprocess.call('omxplayer alarm_tones/' + self.alarm_tones[self.alarm_tone], shell=True)
        self.alarm_on = False 
        print('Alarm')

    
    # NOT IMPLEMENTED
    # Toggles coffee brewing
    def brew(self):
        print('starts brewing')

    # NOT IMPLEMENTED
    # Toggles lights
    def lights(self):
        print('turning on the lights')

    # NOT TESTED
    # Change the volume
    def set_volume(self, level):
        # subprocess.call(bash command, shell=True)
        # NOT TESTED
        subprocess.call('amixer set PCM -- ' + ((level/25)*100) + '%', shell=True)
        print('setting volume')

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

        self.statusLabel = Label(self,font=('times', 15, 'bold'),text=clock.alarm_set_str +
            '\n' + clock.brew_set_str + '\n' + clock.lights_set_str)
        self.statusLabel.pack()

        menuButton = Button(self, text='Settings', command=lambda: controller.show_frame(SettingsPage))
        menuButton.pack()

# settings page of the gui
class SettingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
        # Set up various labels for display
        self.alarmLabel = Label(self, font=('times', 15, 'bold'), text='Next alarm: ' + clock.next_alarm_time)
        self.alarmLabel.pack()

        self.volumeLabel = Label(self, font=('times', 15, 'bold'), text='Volume: ' + str(clock.volume))
        self.volumeLabel.pack()

        self.toneLabel = Label(self,font=('times', 15, 'bold'),text='Alarm tone: ' + clock.alarm_tones[clock.alarm_tone])
        self.toneLabel.pack()

        homeButton = Button(self, text='Home', command=lambda: controller.show_frame(ClockPage))
        homeButton.pack()


# Instantiate a clock and start ticking
# Instantiate a gui and start it up
clock = Clock()
gui = MainWindow()
clock.tick(gui.frames[ClockPage].clockLabel)
gui.mainloop()