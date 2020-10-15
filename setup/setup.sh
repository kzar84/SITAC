#!/bin/bash
##################################################
# Script to install dependencies for sitac
#
# Author: CC
# Date:   10/15/2020
#
##################################################

# Check if script is being run as sudo
if [$(id -u) -ne "0"] then
    echo "Must be run as super user, run again using sudo"
    exit 1
fi


# Update/Upgrade the packages
apt-get update -y
apt-get upgrade -y

# Install dependencies
apt-get install -y python3
apt-get install -y python-pygame
apt-get install -y python3-pyqt5

# These are used for rung qt designer
apt-get install -y pyqt5-dev-tools
apt-get install -y qttools5-dev-tools
apt-get install -y qttools5-dev