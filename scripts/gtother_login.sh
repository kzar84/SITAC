# edit rc.local to run this script at boot
# sudo nano /etc/rc.local
# add "/home/pi/SITAC/gtother_login.sh" before exit 0
# chmod +x /home/pi/SITAC/gtother_login.sh
# reboot

#! /bin/bash/
wget -q -O - --post-data='username=your_username&password=your_password&iss=true&output=text' https://auth.lawn.gatech.edu/index.php