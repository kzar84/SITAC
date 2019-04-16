from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sitac_ui_gold_theme
import pygame
import time
import socket


class SITAC(QtWidgets.QMainWindow, sitac_ui_gold_theme.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        

        ################
        # CLASS FIELDS #
        ################
        # Time strings
        self.current_time = ''
        self.next_time = ''

        # Status Strings
        self.alarm_set_str =  'Alarm: OFF'
        self.brew_set_str =   'Brew: OFF'
        self.lights_set_str = 'Lights: OFF'

        # Status Booleans
        self.alarm_set =  False     # set true for testing purposes
        self.alarm_on =   False
        self.snoozing =   False
        self.brew_set =   False
        self.lights_set = False

        # alarm time list (initial time 7:00 AM)
        self.alarm_times = ['7:00 AM']
        self.next_alarm_time = 0
        self.snooze_time = ''
        self.brew_time = ''

        # alarm tones dictionaries (initial alarm buzzer)
        self.alarm_tones_file = {'Buzzer':'buzzer.wav', 'Police':'police.wav'}
        self.alarm_tones_name = ['Buzzer', 'Police']
        self.alarm_tone = 'Buzzer'

        # dictionary for gui pages
        self.page_names = {'ClockPage':0, 'SettingsPage':1, 'AlarmPage':2, 'SnoozePage':3}

        # Volume (0-50, must be between 0-1.0 when setting using pygame)
        self.volume = 25

        ##############################
        # CONNECT THE GUI COMPONENTS #
        ##############################
        # Clock page buttons
        self.settingsButton.clicked.connect(lambda: self.goToPage('SettingsPage'))
        # Settings page buttons
        self.homeButton.clicked.connect(lambda: self.goToPage('ClockPage'))
        # self.alarmOffButton.clicked.connect(lambda: self.unset_alarm())
        self.brewButton.clicked.connect(lambda: self.set_brew(self.delayTimeInput.time().toString('h:mm A')))
        self.lightsButton.clicked.connect(lambda: self.set_lights())
        self.setAlarmButton.clicked.connect(lambda: self.set_alarm(self.alarmTimeInput.time().toString('h:mm A')))
        # Set up the volume slider
        self.volumeSlider.valueChanged.connect(lambda: self.updateVolume(self.volumeSlider.value()))
        # Set up the alarm tone combo box
        self.tonesList.addItems(self.alarm_tones_name)
        self.tonesList.activated[str].connect(self.updateAlarmTone)
        # Alarm page buttons
        self.outButton.clicked.connect(lambda: self.alarm_off())
        self.snoozeButton.clicked.connect(lambda: self.snooze())
        # Snooze page buttons
        self.snoozeOffButton.clicked.connect(lambda: self.alarm_off())
        self.alarmTimeInput.dateTimeChanged.connect(lambda: self.update_alarm_time(self.alarmTimeInput.time().toString('h:mm A')))

        ################################
        # Set up a timer and call tick #
        ################################
        self.goToPage('ClockPage')
        timer = QtCore.QTimer(self) 
        timer.timeout.connect(self.tick) 
        timer.start(500) 
        self.tick()


    # Fucntion that gets the current time every 500ms, checks for an alarm
    def tick(self):
        # get the current local time from the PC
        self.next_time = time.strftime('%#I:%M %p') # %#I use if for windows, change to %-I when running on linux
        
        # if time string has changed, update it
        if self.next_time != self.current_time:
            self.current_time = self.next_time
            self.timeLabel.setText(self.next_time)
        
        # check to see if an alarm is ready (time matches, alarm is set, alarm is not currently playing, not currently snoozing)
        if ((self.current_time == self.alarm_times[self.next_alarm_time]) and self.alarm_set and not self.alarm_on and not self.snoozing): 
            self.alarm()
        
        # check to see if in snoozing state
        if ((self.current_time == self.snooze_time) and self.snoozing and not self.alarm_on):
            self.alarm()

        # Check to see if the brew is set
        if (self.brew_set and self.brew_time == self.current_time):
            self.brew()
    
    # Function that changes gui pages
    def goToPage(self, page_name):
        self.pages.setCurrentIndex(self.page_names[page_name])

    # Refreshes the clock page
    def refresh_clockPage(self):
        self.nextAlarmLabel.setText('Next alarm: ' + self.alarm_times[self.next_alarm_time])
        self.statusLabel.setText(self.alarm_set_str +
            '\n' + self.brew_set_str + '\n' + self.lights_set_str)

    # Refreshes the settings page
    def refresh_settingsPage(self):
        #self.nextAlarmLabel.setText('Alarm: ' + self.alarm_times[self.next_alarm_time])
        self.volumeLabel.setText('Volume: ' + str(self.volume))
        self.toneLabel.setText('Alarm tone: ' + self.alarm_tone)
        self.setAlarmButton.setText(self.alarm_set_str)
        self.brewButton.setText(self.brew_set_str)
        self.lightsButton.setText(self.lights_set_str)
        
    # Callback functions for updating gui status strings
    def update_alarm_time(self, time):
        if (self.alarm_set):
                    # set the new alarm index if its in the list
            try:
                self.next_alarm_time = self.alarm_times.index(time)
            # if its not in the list, add it, sort the list, set the index
            except:
                self.alarm_times.append(time)
                self.alarm_times.sort()
                self.next_alarm_time = self.alarm_times.index(time)

            self.update_alarm_set()

    
    def set_alarm(self, time):
        if (self.alarm_set):
            self.unset_alarm()
            return
        # set the new alarm index if its in the list
        try:
            self.next_alarm_time = self.alarm_times.index(time)
        # if its not in the list, add it, sort the list, set the index
        except:
            self.alarm_times.append(time)
            self.alarm_times.sort()
            self.next_alarm_time = self.alarm_times.index(time)
        # set alarm_set bool, and update the page
        self.alarm_set = True        
        self.update_alarm_set()

    def unset_alarm(self):
        self.alarm_set = False
        self.update_alarm_set()

    def set_brew(self, brew_time):
        self.brew_set = not self.brew_set
        if self.brew_set:
            self.brew_time = brew_time
        self.update_brew_set()

    def set_lights(self):
        self.lights_set = not self.lights_set
        self.update_lights_set()
    
    def update_alarm_set(self):
        if (self.alarm_set):
            self.alarm_set_str = 'Alarm: ON'
        else:
            self.alarm_set_str = 'Alarm: OFF'

        # update the alarm set string, next alarm string, and next alarm string for settings
        self.refresh_clockPage()   
        self.refresh_settingsPage()

    def update_brew_set(self):
        if (self.brew_set):
            self.brew_set_str =  'Brew: ON'
        else:
            self.brew_set_str =  'Brew: OFF'

        self.refresh_clockPage()   
        self.refresh_settingsPage()

    def update_lights_set(self):
        if (self.lights_set): 
            self.lights_set_str = 'Lights: ON'
        else:
            self.lights_set_str = 'Lights: OFF'

        self.refresh_clockPage()   
        self.refresh_settingsPage()

    # Sounds the alarm
    def alarm(self):
        # play selected alarm tone, show the alarm page, and turn on alarm_on bool
        pygame.mixer.music.load('alarm_tones/' + self.alarm_tones_file[self.alarm_tone])
        pygame.mixer.music.set_volume(self.volume/50)
        pygame.mixer.music.play()
        self.wakeUpLabel.setText('Rise and Shine\nThe current time is ' + time.strftime('%#I:%M %p'))
        self.goToPage('AlarmPage')
        
        if self.brew_set:
            self.brew()
        if self.lights_set:
            self.lights()

        self.alarm_on = True
            
    # implements snooze functionality
    # turn off lights/coffee?
    def snooze(self):
        # If the lights were set, turn them back off
        if self.lights_set:
            self.lights()
        # can add support for customizable snooze ammounts
        pygame.mixer.music.stop()
        self.snooze_time = self.add_minutes(time.strftime('%#I:%M %p'), 1)
        self.snoozeLabel.setText('Snoozing until ' + self.snooze_time)
        self.goToPage('SnoozePage') 
        self.alarm_on = False  
        self.snoozing = True

    # turn off the alarm
    def alarm_off(self):
        # Go back  to clockpage, turn off alarm_on/snoozing/alarm_set bool, stop audio play
        pygame.mixer.music.stop()
        self.alarm_set = False
        self.alarm_on = False
        self.snoozing = False
        self.update_alarm_set()
        self.goToPage('ClockPage')

    # Toggles coffee brewing
    def brew(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.timeout(1)
            # ip address is local to my network, will have to change when running on gtother
            # possibly set up esp8266 with host name and connect with that?
            s.connect(('192.168.1.37', 80))
            s.sendall(b'toggle')
            s.close()
        except:
            print("Could not connect to device")

    # Toggles lights
    def lights(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.timeout(1)
            # ip address is local to my network, will have to change when running on gtother
            s.connect(('192.168.1.36', 80))
            s.sendall(b'toggle')
            s.close()
        except:
            print("Could not connect to device")

    # Change the volume
    def updateVolume(self, v):
        self.volume = v
        self.refresh_settingsPage()

    # Change the alarm tone
    def updateAlarmTone(self):
        self.alarm_tone = self.tonesList.currentText()

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

        # Connect the buttons
    


def main():
    pygame.init()
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = SITAC()
    # set the window to frameless (no title bar), close app using Alt+F4, and hide the cursor                  
    flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowCloseButtonHint)
    form.setWindowFlags(flags)
    form.setCursor(QtCore.Qt.BlankCursor)
    form.showFullScreen()            # Show the form in fullscreen
    sys.exit(app.exec_())               # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()
