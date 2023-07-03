#!/usr/bin/bash

echoNeedInstall()
{
   echo "########################################################################"
   echo " Installing $1"
   echo "########################################################################"
}

echoNeedInstall python3.10
sudo apt-get install -y python3.10 python3.10-dbg python3.10-dev python3.10-doc python3.10-minimal python3.10-venv

echoNeedInstall pip
sudo apt-get install -y python3-pip

echoNeedInstall virtualenv
sudo apt-get install -y python3-virtualenv

# clean, create and activate the virtual env
sudo rm -R venv
virtualenv --python=/usr/bin/python3.10 --system-site-packages venv
. venv/bin/activate

# install dependencies
pip install -r requirements.txt --force-reinstall
pip install flake8 --force-reinstall

# deactivate virtual env
deactivate
