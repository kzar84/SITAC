# use Tkinter to show a digital clock

from tkinter import *
import time
import subprocess
import pygame

# Class that handles clock functionality
class Clock:
    def __init__(self): 
        # Time strings
        self.current_time = ''
        self.next_time = ''

        # Status Strings
        self.alarm_set_str =  'Alarm: ON'
        self.brew_set_str =   'Brew:  OFF'
        self.lights_set_str = 'Light: OFF'

        # Status Booleans
        self.alarm_on =   False
        self.alarm_set =  True     # set true for testing purposes
        self.snoozing =   False
        self.brew_set =   False
        self.lights_set = False

        # alarm tones list/alarm times list (initial index = 0)
        self.alarm_times = ['12:43 PM', 'add_more_alarms_here']
        self.alarm_tones = ['buzzer.wav', 'add_more_alarms_here.wav']
        self.next_alarm_time = 0
        self.alarm_tone = 0
        self.snooze_time = ''

        # Volume (0-50)
        self.volume = 25

    # Fucntion that gets the current time every 500ms and updates appropriate label
    def tick(self, gui):
        # get the current local time from the PC
        self.next_time = time.strftime('%-I:%M %p') # %#I use if for windows, change to %-I when running on linux
        
        # if time string has changed, update it
        if self.next_time != self.current_time:
            self.current_time = self.next_time
            gui.frames[ClockPage].clockLabel.config(text=self.next_time)
        
        # check to see if an alarm is ready
        if ((self.current_time == self.alarm_times[self.next_alarm_time]) and self.alarm_set and not self.alarm_on): 
            self.alarm(gui)
        
        # check to see if in snoozing state
        if ((self.current_time == self.snooze_time) and self.snoozing):
            self.alarm(gui)
        
        # recall function after 500 miliseconds
        gui.after(200, self.tick, gui)

    # Callback functions for updating gui status strings
    def set_alarm(self, time, gui):
        # set new status string, alarm time, and snooze time
        self.alarm_set = True
        self.next_alarm_time = time
        self.snooze_time = time          
        self.update_alarm_set(gui)

    def update_alarm_set(self, gui):
        if (self.alarm_set):
            self.alarm_set_str = 'Alarm: ON'
        else:
            self.alarm_set_str = 'Alarm: OFF'

        gui.frames[ClockPage].statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    def update_brew_set(self, statusLabel):
        if (self.brew_set):
            self.brew_set_str =  'Brew:   ON'
        else:
            self.brew_set_str =  'Brew:   OFF'

        statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    def update_lights_set(self, statusLabel):
        if (self.lights_set): 
            self.lights_set_str = 'Light:  ON'
        else:
            self.lights_set_str = 'Light:  OFF'

        statusLabel.config(text=self.alarm_set_str + '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    # subprocess is used in below functions for exectuing terminal commands in linux
    # subprocess.call(bash command, shell=True)

    # Sounds the alarm
    def alarm(self, gui):
        # turn on alarm_on bool, show the alarm page, and play selected alarm tone'
        self.alarm_on = True
        gui.show_frame(AlarmPage)
        # subprocess.call('omxplayer alarm_tones/' + self.alarm_tones[self.alarm_tone] + ' &', shell=True)
        pygame.mixer.music.load('alarm_tones/' + self.alarm_tones[self.alarm_tone])
        pygame.mixer.music.play()
            
    # implements snooze functionality
    def snooze(self, gui):
        # can add support for customizable snooze ammounts
        # subprocess.call('kill %1', shell=True)
        pygame.mixer.music.stop()
        self.snooze_time = self.add_minutes(time.strftime('%#I:%M %p'), 1)
        gui.frames[SnoozePage].snoozeLabel.config(text='Snoozing until ' + self.snooze_time)
        self.snoozing = True
        gui.show_frame(SnoozePage)     

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
        print('turning on the lights')sKater9421
        

    # NOT TESTED
    # Change the volume
    def set_volume(self, level):
        # subprocess.call(bash command, shell=True)
        # NOT TESTED
        subprocess.call('amixer set PCM -- ' + ((level/25)*100) + '%', shell=True)
        print('setting volume')

    # add minutes to a specified time
    # 7:00 AM vs 07:00 AM
    def add_minutes(self, stime, minutes):
        if (len(stime) > 7):
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
        else:
            new_minutes = int(stime[2:4]) + minutes
            new_hour = int(stime[0:1])
            new_m = stime[4:7]
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
            
        if (new_minutes > 10):
            stime = str(new_hour) + ':' + str(new_minutes) + new_m
        else:
            stime = str(new_hour) + ':0' + str(new_minutes) + new_m
        print(stime)
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
        self.clockLabel = Label(self, font=('times', 30, 'bold'))
        self.clockLabel.pack()

        self.nextAlarmLabel = Label(self, font=('times', 15, 'bold'), text='Next alarm: ' + clock.alarm_times[clock.next_alarm_time])
        self.nextAlarmLabel.pack()

        self.statusLabel = Label(self,font=('times', 15, 'bold'),text=clock.alarm_set_str +
            '\n' + clock.brew_set_str + '\n' + clock.lights_set_str)
        self.statusLabel.pack()

        menuButton = Button(self, text='Settings', command=lambda: controller.show_frame(SettingsPage))
        menuButton.pack()

        setAlarmButton = Button(self, text='Set Alarm', command=lambda: clock.set_alarm(clock.next_alarm_time, gui))
        setAlarmButton.pack()

# settings page of the gui
class SettingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
        # Set up various labels for display
        self.alarmLabel = Label(self, font=('times', 15, 'bold'), text='Next alarm: ' + clock.alarm_times[clock.next_alarm_time])
        self.alarmLabel.pack()

        self.volumeLabel = Label(self, font=('times', 15, 'bold'), text='Volume: ' + str(clock.volume))
        self.volumeLabel.pack()

        self.toneLabel = Label(self,font=('times', 15, 'bold'),text='Alarm tone: ' + clock.alarm_tones[clock.alarm_tone])
        self.toneLabel.pack()

        homeButton = Button(self, text='Home', command=lambda: controller.show_frame(ClockPage))
        homeButton.pack()

# settings page of the gui
class AlarmPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
        # Set up various labels for display
        self.wakeUpLabel = Label(self, font=('times', 30, 'bold'), text='Rise and Shine')
        self.wakeUpLabel.pack()

        snoozeButton = Button(self, text='Snooze', command=lambda: clock.snooze(controller))
        snoozeButton.pack()

        offButton = Button(self, text='Alarm off', command=lambda: clock.alarm_off(controller))
        offButton.pack()

# Add snoozing page (snoozing until: , with menu button)
class SnoozePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add page stuff
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
