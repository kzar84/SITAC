# use Tkinter to show a digital clock

# add configuration file that stores the current settings. This will be used in the event of power loss and/or default settings

from tkinter import *
import pygame
import time
import subprocess

# Class that handles clock functionality
class Clock:
    def __init__(self): 
        # Time strings
        self.current_time = ''
        self.next_time = ''

        # Status Strings
        self.alarm_set_str =  'Alarm:  ON'
        self.brew_set_str =   'Brew:   OFF'
        self.lights_set_str = 'Lights: OFF'

        # Status Booleans
        self.alarm_set =  True     # set true for testing purposes
        self.alarm_on =   False
        self.snoozing =   False
        self.brew_set =   False
        self.lights_set = False

        # alarm time list (initial time 7:00 AM)
        self.alarm_times = ['7:00 AM']
        self.next_alarm_time = 0
        self.snooze_time = ''

        # alarm tones dictionaries (initial alarm buzzer)
        self.alarm_tones_file = {'Buzzer':'buzzer.wav', 'Police':'police.wav'}
        self.alarm_tones_name = ['Buzzer', 'Police']
        self.alarm_tone = 'Buzzer'

        # Volume (0-50, must be between 0-1.0 when setting using pygame)
        self.volume = 15

    # Fucntion that gets the current time every 500ms, checks for an alarm
    def tick(self, gui):
        # get the current local time from the PC
        self.next_time = time.strftime('%#I:%M %p') # %#I use if for windows, change to %-I when running on linux
        
        # if time string has changed, update it
        if self.next_time != self.current_time:
            self.current_time = self.next_time
            gui.frames[ClockPage].clockLabel.config(text=self.next_time)
        
        # check to see if an alarm is ready (time matches, alarm is set, alarm is not currently playing, not currently snoozing)
        if ((self.current_time == self.alarm_times[self.next_alarm_time]) and self.alarm_set and not self.alarm_on and not self.snoozing): 
            self.alarm(gui)
        
        # check to see if in snoozing state
        if ((self.current_time == self.snooze_time) and self.snoozing and not self.alarm_on):
            self.alarm(gui)
        
        # recall function after 500 miliseconds
        gui.after(200, self.tick, gui)

    # Callback functions for updating gui status strings
    def set_alarm(self, time, gui):
        # set the new alarm index if its in the list
        try:
            self.next_alarm_time = self.alarm_times.index(time)
        # if its not in the list, add it, sort the list, set the index
        except:
            self.alarm_times.append(time)
            self.alarm_times.sort()
            self.next_alarm_time = self.alarm_times.index(time)
        # set initial snooze time, alarm_set bool, and update the page
        self.snooze_time = time  
        self.alarm_set = True        
        self.update_alarm_set(gui)

    def update_alarm_set(self, gui):
        if (self.alarm_set):
            self.alarm_set_str = 'Alarm: ON'
        else:
            self.alarm_set_str = 'Alarm: OFF'

        # update the alarm set string, next alarm string, and next alarm string for settings
        gui.frames[ClockPage].refresh_page()   
        gui.frames[SettingsPage].refresh_page()

    def update_brew_set(self, statusLabel):
        if (self.brew_set):
            self.brew_set_str =  'Brew:   ON'
        else:
            self.brew_set_str =  'Brew:   OFF'

        statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    def update_lights_set(self, statusLabel):
        if (self.lights_set): 
            self.lights_set_str = 'Lights:  ON'
        else:
            self.lights_set_str = 'Lights:  OFF'

        statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)


    # Sounds the alarm
    def alarm(self, gui):
        # play selected alarm tone, show the alarm page, and turn on alarm_on bool
        pygame.mixer.music.load('alarm_tones/' + self.alarm_tones_file[self.alarm_tone])
        pygame.mixer.music.set_volume(self.volume/50)
        pygame.mixer.music.play()
        gui.show_frame(AlarmPage)
        self.alarm_on = True
            
    # implements snooze functionality
    def snooze(self, gui):
        # can add support for customizable snooze ammounts
        pygame.mixer.music.stop()
        self.snooze_time = self.add_minutes(time.strftime('%#I:%M %p'), 1)
        gui.frames[SnoozePage].snoozeLabel.config(text='Snoozing until ' + self.snooze_time)
        gui.show_frame(SnoozePage)   
        self.alarm_on = False  
        self.snoozing = True

    # turn off the alarm
    def alarm_off(self, gui):
        # Go back  to clockpage, turn off alarm_on/snoozing/alarm_set bool, stop audio play
        pygame.mixer.music.stop()
        self.alarm_set = False
        self.alarm_on = False
        self.snoozing = False
        self.update_alarm_set(gui)
        gui.show_frame(ClockPage)

    # NOT IMPLEMENTED
    # Toggles coffee brewing
    def brew(self):
        print('starts brewing')

    # NOT IMPLEMENTED
    # Toggles lights
    def lights(self):
        print('turning on the lights')

    # add minutes to a specified time
    def add_minutes(self, stime, minutes):
        # pad it with a 0 if its length is less than 7
        if (len(stime) < 8):
            stime = '0' + stime
        # Get the new time and adjust back to time format
        new_minutes = int(stime[3:5]) + minutes
        new_hour = int(stime[0:2])
        new_m = stime[5:8]
        # if the hour rolls over, update minutes, hour, and am/pm if necessary
        if (new_minutes >= 60):
            new_minutes -= 60
            new_hour += 1
            if (new_hour > 12):
                new_hour -= 12
                if (new_m == ' PM'):
                    new_m = ' AM'
                else:
                    new_m = ' PM'
        # if the new minutes are less than  10, pad it with a 0
        if (new_minutes > 10):
            stime = str(new_hour) + ':' + str(new_minutes) + new_m
        else:
            stime = str(new_hour) + ':0' + str(new_minutes) + new_m

        return stime

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
        for F in (ClockPage, SettingsPage, AlarmPage, SnoozePage):
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
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        # Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        Grid.rowconfigure(self, 2, weight=1)
        Grid.rowconfigure(self, 3, weight=1)

        self.clockLabel = Label(self, font=('times', 60, 'bold'))
        self.clockLabel.grid(row = 1, column = 0, columnspan = 2)
        self.clockLabel.grid(sticky=S+N+E+W)

        self.nextAlarmLabel = Label(self, font=('times', 15, 'bold'), text='Next alarm: ' + clock.alarm_times[clock.next_alarm_time])
        self.nextAlarmLabel.grid(row = 2, column = 0, columnspan = 2)
        self.nextAlarmLabel.grid(sticky=N)

        self.statusLabel = Label(self,font=('times', 18, 'bold'),text=clock.alarm_set_str +
            '\n' + clock.brew_set_str + '\n' + clock.lights_set_str)
        self.statusLabel.grid(row = 3, column = 0)
        self.statusLabel.grid(sticky=S+W)

        menuButton = Button(self, text='Settings', command=lambda: controller.show_frame(SettingsPage))
        menuButton.config(height = 5, width = 20)
        menuButton.grid(row = 3, column = 1)
        menuButton.grid(sticky=S+E)


    # resets all labels on the page
    def refresh_page(self):
        self.nextAlarmLabel.config(text='Next alarm: ' + clock.alarm_times[clock.next_alarm_time])
        self.statusLabel.config(text=clock.alarm_set_str +
            '\n' + clock.brew_set_str + '\n' + clock.lights_set_str)

# settings page of the gui
class SettingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Grid.rowconfigure(self, 0, weight=1)
        # Grid.columnconfigure(self, 0, weight=1)
        # Grid.rowconfigure(self, 1, weight=1)
        # Grid.columnconfigure(self, 1, weight=1)
        # Grid.rowconfigure(self, 2, weight=1)
        # Grid.columnconfigure(self, 2, weight=1)
        # Grid.rowconfigure(self, 3, weight=1)
        # Grid.columnconfigure(self, 3, weight=1)
        # Grid.rowconfigure(self, 4, weight=1)
        # Grid.rowconfigure(self, 5, weight=1)
        # Grid.rowconfigure(self, 6, weight=1)


        # Alarm settings
        self.alarmLabel = Label(self, font=('times', 15, 'bold'), text='Next alarm: ' + clock.alarm_times[clock.next_alarm_time])
        self.alarmLabel.grid(row=0, column=0, sticky=N+S+E+W)

        # set up dropdown menu for selecting hour
        self.hours = []
        for i in range(12):
            self.hours.append(str(i+1))
        self.hour = StringVar(self)
        self.hour.set(self.hours[0])
        self.hourMenu = OptionMenu(self, self.hour, *self.hours)
        
        self.hourMenu.grid(row=1, column=0, sticky=N+S+E+W)
        
        # set up dropdown menu for selecting minute
        self.minutes = []
        for i in range(12):
            self.minutes.append(str(i*5))
            # Pad the value with a 0 if the length is less than 2
            if (len(self.minutes[i]) < 2):
                self.minutes[i] =  '0' + self.minutes[i]
        self.minute = StringVar(self)
        self.minute.set(self.minutes[0])
        self.minuteMenu = OptionMenu(self, self.minute, *self.minutes)
        
        self.minuteMenu.grid(row=1, column=1, sticky=N+S+E+W)
        
        # set up dropdown menu for selecting AM/PM
        self.ms = ['AM', 'PM']
        self.m = StringVar(self)
        self.m.set(self.ms[0])
        self.mMenu = OptionMenu(self, self.m, *self.ms)
        
        self.mMenu.grid(row=1, column=2, sticky=N+S+E+W)

        # Volume setting
        self.volumeLabel = Label(self, font=('times', 15, 'bold'), text='Volume: ' + str(clock.volume))
        self.volumeLabel.grid(row=2, column=0, sticky=N+S+E+W)
        # Scale for setting the volume
        self.volumeScale = Scale(self, from_=0, to=30, orient=HORIZONTAL)
        self.volumeScale.grid(row=3, column=0, sticky=N+S+E+W)

        # Alarm tone setting
        self.toneLabel = Label(self,font=('times', 15, 'bold'), text='Alarm tone: ' + clock.alarm_tone)
        self.toneLabel.grid(row=4, column=0, sticky=N+S+E+W)
        # Drop down menu for selecting alarm tone
        self.tones = []
        for i in range(len(clock.alarm_tones_name)):
            self.tones.append(clock.alarm_tones_name[i])
        self.tone = StringVar(self)
        self.tone.set(self.tones[0])
        self.toneMenu = OptionMenu(self, self.tone, *self.tones)
        self.toneMenu.grid(row=5, column=0, sticky=N+S+E+W)

        
        # Button that sets new alarm according to input (peice hour/minute/m together to pass to set_alarm)
        self.setAlarmButton = Button(self, text="Set Alarm", command=lambda: 
            clock.set_alarm(self.hour.get() + ':' + self.minute.get() + ' ' + self.m.get(), controller))
        self.setAlarmButton.grid(row = 1, column = 3, sticky=N+S+E+W)

        # Updates the settings (volume and alarmtone) to the currently selected values
        self.updateSettingsButton = Button(self, text="Update Settings", command=lambda: self.update_settings(controller))
        self.updateSettingsButton.grid(row = 6, column = 0, sticky=N+S+E+W)
        # Returns to ClockPage
        homeButton = Button(self, text='Home', command=lambda: controller.show_frame(ClockPage))
        homeButton.grid(row = 6, column = 3, sticky=N+S+E+W)

    # Updates clock settings (volume and alarmtone)
    def update_settings(self, controller):
        clock.volume = self.volumeScale.get()
        clock.alarm_tone = self.tone.get()
        self.refresh_page()
   
        
    # resets all labels on the page
    def refresh_page(self):
        self.alarmLabel.config(text='Next alarm: ' + clock.alarm_times[clock.next_alarm_time])
        self.volumeLabel.config(text='Volume: ' + str(clock.volume))
        self.toneLabel.config(text='Alarm tone: ' + clock.alarm_tone)

# settings page of the gui
class AlarmPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Set up various labels for display
        self.wakeUpLabel = Label(self, font=('times', 30, 'bold'), text='Rise and Shine')
        self.wakeUpLabel.pack()

        self.snoozeButton = Button(self, text='Snooze', command=lambda: clock.snooze(controller))
        self.snoozeButton.pack()

        self.offButton = Button(self, text='Alarm off', command=lambda: clock.alarm_off(controller))
        self.offButton.pack()

# Add snoozing page (snoozing until: , with menu button)
class SnoozePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Set up various labels for display
        self.clockLabel = Label(self, font=('times', 30, 'bold'), text=clock.current_time)
        self.clockLabel.pack()
        
        self.snoozeLabel = Label(self, font=('times', 30, 'bold'))
        self.snoozeLabel.pack()

        self.offButton = Button(self, text='Alarm off', command=lambda: clock.alarm_off(controller))
        self.offButton.pack()

# Instantiate a clock and start ticking
# Instantiate a gui and start it up
pygame.init()
clock = Clock()
gui = MainWindow()
clock.tick(gui)
gui.mainloop()
