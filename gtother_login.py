# waiting on response for request needed to autologin

# edit rc.local to run this script at boot
# sudo nano /etc/rc.local
# add "sudo python /home/pi/SITAC/gtother_login.py &" before exit 0
# reboot

from subprocess import call


